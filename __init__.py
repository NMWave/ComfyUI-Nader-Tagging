from .nodes.text_nodes import *
from .nodes.lora_nodes import *
from .nodes.io_nodes import *
from .nodes.scheduler_nodes import *

NODE_CONFIG = {
    # Text Processing Nodes
    "Tag Duplicate Remover": {"class": TagDuplicateRemover, "name": "Tag Duplicate Remover"},
    "Tag Alternating Combiner": {"class": CombineAlternatingTags, "name": "Tag Alternating Combiner"},
    "Split Sentences": {"class": SplitSentences, "name": "Split Sentences"},
    "Split Tags": {"class": SplitTags, "name": "Split Tags"},
    "Token Counter": {"class": TokenCounter, "name": "Token Counter"},
    
    # LoRA Nodes
    "LoRA Extract and Save": {"class": LoraExtractAndSave, "name": "LoRA Extract and Save"},
    
    # I/O Nodes
    "Load Text List": {"class": LoadTextList, "name": "Load Text List"},
    
    # Scheduler Nodes
    "Wan22 Noise Scheduler": {"class": Wan22NoiseScheduler, "name": "Wan 2.2 Noise Scheduler"},
}

def generate_node_mappings(node_config):
    node_class_mappings = {}
    node_display_name_mappings = {}

    for node_name, node_info in node_config.items():
        node_class_mappings[node_name] = node_info["class"]
        node_display_name_mappings[node_name] = node_info.get("name", node_info["class"].__name__)

    return node_class_mappings, node_display_name_mappings

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = generate_node_mappings(NODE_CONFIG)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
