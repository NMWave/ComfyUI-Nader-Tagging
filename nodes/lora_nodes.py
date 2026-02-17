import torch
import comfy.model_management
import comfy.utils
import folder_paths
import os
import logging
from enum import Enum
import time

CLAMP_QUANTILE = 0.99

def extract_lora(diff, rank, iterations):
    conv2d = (len(diff.shape) == 4)
    kernel_size = None
    
    if conv2d:
        kernel_size = diff.size()[2:4]
        out_dim, in_dim = diff.size()[0:2]
        diff = diff.reshape(out_dim, -1)
    else:
        out_dim, in_dim = diff.size()

    rank = min(rank, in_dim, out_dim)
    diff_float = diff.float()

    U, S, V = torch.svd_lowrank(diff_float, q=rank, niter=iterations)

    Vh = V.transpose(-1, -2)

    U = U @ torch.diag(S)

    dist = torch.cat([U.flatten(), Vh.flatten()])
    hi_val = torch.quantile(dist, CLAMP_QUANTILE)
    low_val = -hi_val
    U = U.clamp(low_val, hi_val)
    Vh = Vh.clamp(low_val, hi_val)

    if conv2d:
        U = U.reshape(out_dim, rank, 1, 1)
        Vh = Vh.reshape(rank, in_dim, kernel_size[0], kernel_size[1])
        
    return (U, Vh)

class LORAType(Enum):
    STANDARD = 0
    FULL_DIFF = 1

LORA_TYPES = {"standard": LORAType.STANDARD,
              "full_diff": LORAType.FULL_DIFF}

def calc_lora_model(model_diff, rank, iterations, prefix_model, prefix_lora, output_sd, lora_type, bias_diff=False):
    comfy.model_management.load_models_gpu([model_diff], force_patch_weights=True)
    sd = model_diff.model_state_dict(filter_prefix=prefix_model)

    logging.info(f"Analyzing model part with prefix '{prefix_model}'...")
    keys_to_process = [k for k in sd if k.endswith(".weight") or (bias_diff and k.endswith(".bias"))]
    total_keys = len(keys_to_process)

    if total_keys == 0:
        logging.info(f"No processable layers ('.weight' or '.bias') found for prefix '{prefix_model}'. Skipping.")
        return output_sd

    logging.info(f"Found {total_keys} layers to process. Starting LoRA extraction...")
    start_time = time.time()

    for i, k in enumerate(keys_to_process):
        progress_percent = (i + 1) / total_keys * 100
        
        weight_diff_info = sd[k]
        logging.info(f"[{progress_percent:5.1f}%] ({i+1}/{total_keys}) Processing layer: {k} (shape: {weight_diff_info.shape})")
        
        if k.endswith(".weight"):
            weight_diff = sd[k]
            if lora_type == LORAType.STANDARD:
                if weight_diff.ndim not in [2, 4]:
                    logging.warning(f"Skipping layer {k} as its weight is not 2D or 4D (convolutional). Shape is {weight_diff.shape}.")
                    if bias_diff:
                        output_sd["{}{}.diff".format(prefix_lora, k[len(prefix_model):-7])] = weight_diff.contiguous().half().cpu()
                    continue
                try:
                    out = extract_lora(weight_diff, rank, iterations)
                    output_sd["{}{}.lora_up.weight".format(prefix_lora, k[len(prefix_model):-7])] = out[0].contiguous().half().cpu()
                    output_sd["{}{}.lora_down.weight".format(prefix_lora, k[len(prefix_model):-7])] = out[1].contiguous().half().cpu()
                except Exception as e:
                    logging.warning(f"Could not generate lora weights for key {k}. Is the weight difference zero? Error: {e}")
            elif lora_type == LORAType.FULL_DIFF:
                output_sd["{}{}.diff".format(prefix_lora, k[len(prefix_model):-7])] = weight_diff.contiguous().half().cpu()

        elif bias_diff and k.endswith(".bias"):
            output_sd["{}{}.diff_b".format(prefix_lora, k[len(prefix_model):-5])] = sd[k].contiguous().half().cpu()
            
    end_time = time.time()
    logging.info(f"Finished processing {total_keys} layers for this model part in {end_time - start_time:.2f} seconds.")
    return output_sd

class LoraExtractAndSave:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"filename_prefix": ("STRING", {"default": "loras/ComfyUI_extracted_lora"}),
                              "rank": ("INT", {"default": 8, "min": 1, "max": 4096, "step": 1}),
                              "iterations": ("INT", {"default": 7, "min": 1, "max": 50, "step": 1}),
                              "lora_type": (tuple(LORA_TYPES.keys()),),
                              "bias_diff": ("BOOLEAN", {"default": True}),
                            },
                "optional": {"model_diff": ("MODEL", {"tooltip": "The ModelSubtract output to be converted to a lora."}),
                             "text_encoder_diff": ("CLIP", {"tooltip": "The CLIPSubtract output to be converted to a lora."})},
    }
    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True

    CATEGORY = "NMWave/lora"

    def save(self, filename_prefix, rank, iterations, lora_type, bias_diff, model_diff=None, text_encoder_diff=None):
        if model_diff is None and text_encoder_diff is None:
            logging.info("LoRA Extract and Save: No model or text encoder diff provided. Nothing to do.")
            return {}

        lora_type_enum = LORA_TYPES.get(lora_type)
        if lora_type_enum == LORAType.STANDARD:
            logging.info(f"Starting LoRA extraction with rank={rank} and iterations={iterations}. This may take a long time...")
        else:
            logging.info(f"Starting FULL_DIFF extraction. This will be fast but create a very large file.")

        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)

        output_sd = {}
        if model_diff is not None:
            logging.info("\n--- Processing UNet (diffusion_model) ---")
            output_sd = calc_lora_model(model_diff, rank, iterations, "diffusion_model.", "diffusion_model.", output_sd, lora_type_enum, bias_diff=bias_diff)
            
        if text_encoder_diff is not None:
            logging.info("\n--- Processing Text Encoders (CLIP) ---")
            output_sd = calc_lora_model(text_encoder_diff.patcher, rank, iterations, "text_model.", "text_model.", output_sd, lora_type_enum, bias_diff=bias_diff)

        logging.info("\nAll layers processed. Saving final file...")
        output_checkpoint = f"{filename}_{counter:05}_.safetensors"
        output_checkpoint = os.path.join(full_output_folder, output_checkpoint)

        comfy.utils.save_torch_file(output_sd, output_checkpoint, metadata=None)
        logging.info(f"✅ Successfully saved LoRA to: {output_checkpoint}")
        return {}