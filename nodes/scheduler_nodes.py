import math

class Wan22NoiseScheduler:
    
    # Data from DataTable.csv - high noise steps for each scheduler at different shifts (for 20 steps)
    SCHEDULER_DATA = {
        0.5: {"beta": 3, "beta57": 2, "bong_tangent": 7, "ddim_uniform": 1, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 2, "sgm_uniform": 1, "simple": 1},
        1.0: {"beta": 4, "beta57": 3, "bong_tangent": 8, "ddim_uniform": 2, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 2, "sgm_uniform": 2, "simple": 2},
        1.5: {"beta": 5, "beta57": 3, "bong_tangent": 8, "ddim_uniform": 3, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 3, "sgm_uniform": 3, "simple": 3},
        2.0: {"beta": 6, "beta57": 4, "bong_tangent": 8, "ddim_uniform": 4, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 4, "sgm_uniform": 4, "simple": 4},
        2.5: {"beta": 6, "beta57": 5, "bong_tangent": 8, "ddim_uniform": 5, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 5, "sgm_uniform": 5, "simple": 5},
        3.0: {"beta": 7, "beta57": 5, "bong_tangent": 8, "ddim_uniform": 6, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 6, "sgm_uniform": 6, "simple": 6},
        3.5: {"beta": 8, "beta57": 6, "bong_tangent": 8, "ddim_uniform": 6, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 7, "sgm_uniform": 7, "simple": 7},
        4.0: {"beta": 8, "beta57": 6, "bong_tangent": 8, "ddim_uniform": 7, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 7, "sgm_uniform": 7, "simple": 7},
        4.5: {"beta": 9, "beta57": 7, "bong_tangent": 8, "ddim_uniform": 7, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 8, "sgm_uniform": 8, "simple": 8},
        5.0: {"beta": 9, "beta57": 7, "bong_tangent": 8, "ddim_uniform": 8, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 8, "sgm_uniform": 8, "simple": 8},
        5.5: {"beta": 9, "beta57": 7, "bong_tangent": 8, "ddim_uniform": 8, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 8, "sgm_uniform": 9, "simple": 9},
        6.0: {"beta": 10, "beta57": 7, "bong_tangent": 8, "ddim_uniform": 8, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 9, "sgm_uniform": 9, "simple": 9},
        6.5: {"beta": 10, "beta57": 8, "bong_tangent": 8, "ddim_uniform": 9, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 9, "sgm_uniform": 10, "simple": 10},
        7.0: {"beta": 10, "beta57": 8, "bong_tangent": 8, "ddim_uniform": 10, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 10, "sgm_uniform": 10, "simple": 10},
        7.5: {"beta": 10, "beta57": 8, "bong_tangent": 8, "ddim_uniform": 10, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 10, "sgm_uniform": 10, "simple": 10},
        8.0: {"beta": 11, "beta57": 8, "bong_tangent": 8, "ddim_uniform": 10, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 10, "sgm_uniform": 11, "simple": 11},
        8.5: {"beta": 11, "beta57": 9, "bong_tangent": 8, "ddim_uniform": 11, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 10, "sgm_uniform": 11, "simple": 11},
        9.0: {"beta": 11, "beta57": 9, "bong_tangent": 8, "ddim_uniform": 11, "exponential": 1, "karras": 1, "kl_optimal": 2, "linear_quadratic": 13, "normal": 10, "sgm_uniform": 11, "simple": 11}
    }
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "scheduler": (["normal", "beta", "beta57", "bong_tangent", "ddim_uniform", "exponential", "karras", "kl_optimal", "linear_quadratic", "sgm_uniform", "simple"],),
                "total_steps": ("INT", {"default": 20, "min": 1, "max": 1000, "step": 1}),
                "shift": ("FLOAT", {"default": 5.0, "min": 0.5, "max": 9.0, "step": 0.5})
            }
        }
    
    RETURN_TYPES = ("STRING", "INT", "INT")
    RETURN_NAMES = ("scheduler_name", "high_noise_steps", "low_noise_steps")

    FUNCTION = "calculate_steps"

    CATEGORY = "NMWave/scheduler"

    def calculate_steps(self, scheduler, total_steps, shift):
        # Get high noise steps for 20 steps from the data
        base_high_noise_steps = self.SCHEDULER_DATA[shift][scheduler]
        
        # Calculate ratio: high_noise_steps / 20
        ratio = base_high_noise_steps / 20.0
        
        # Calculate actual high noise steps for the desired total steps
        calculated_high_noise_steps = ratio * total_steps
        
        # Round up if it's a fraction (as per requirements)
        high_noise_steps = math.ceil(calculated_high_noise_steps)
        
        # Low noise steps is the remainder
        low_noise_steps = total_steps - high_noise_steps
        
        # Ensure we don't have negative low noise steps
        if low_noise_steps < 0:
            low_noise_steps = 0
            high_noise_steps = total_steps
        
        return (scheduler, high_noise_steps, low_noise_steps)