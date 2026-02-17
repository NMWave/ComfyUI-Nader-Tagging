# ComfyUI Node Development Best Practices

## Professional Node Architecture Patterns

### 1. **Modular File Organization**
Professional ComfyUI projects should use organized structures that separate functionality:

```
ComfyUI-NodeProject/
├── __init__.py              # Central import hub
├── nodes/                   # All node implementations
│   ├── nodes.py            # Core/utility nodes
│   ├── image_nodes.py      # Image processing nodes
│   ├── lora_nodes.py       # LoRA-specific nodes
│   ├── mask_nodes.py       # Mask operations
│   ├── curve_nodes.py      # Curve/spline operations
│   └── [specialized].py    # Other specialized node categories
├── utility/                # Helper functions and utilities
│   ├── utility.py         # Core utility functions
│   ├── numerical.py       # Math/numerical utilities
│   └── [others].py        # Specific utilities
├── web/                   # Frontend JavaScript components
├── fonts/                 # Static assets
└── pyproject.toml         # Modern Python project configuration
```

### 2. **Advanced Node Configuration System**
Professional node projects should use a sophisticated configuration system in `__init__.py`:

```python
NODE_CONFIG = {
    "NodeInternalName": {
        "class": NodeClass, 
        "name": "Display Name"
    },
    # ... more nodes
}

def generate_node_mappings(node_config):
    # Auto-generates both CLASS and DISPLAY mappings
    # Reduces duplication and maintenance overhead
```

**Benefits:**
- Single source of truth for all node metadata
- Automatic generation of required ComfyUI mappings
- Easy to add new nodes without manual mapping updates
- Centralized display name management

### 3. **Sophisticated Category Organization**
Professional projects should use hierarchical categories:
- `NodeProject/constants` - Basic data type constants
- `NodeProject/masking` - Mask-related operations  
- `NodeProject/images` - Image processing
- `NodeProject/utility` - Helper nodes
- etc.

### 4. **Enhanced LoRA Implementation Patterns**
Professional LoRA implementations should include:
- Algorithm selection (`svd_lowrank` vs `torch.linalg.svd`)
- Configurable iteration parameters (`lowrank_iters`)
- Better error handling and progress tracking
- Support for different LoRA types and optimizations

### 5. **Utility Function Organization**
The `utility/` folder should contain reusable functions:
- `pil2tensor()`, `tensor2pil()` - Image format conversions
- Consistent type hints and documentation
- Modular imports for specific functionality

### 6. **Professional Project Structure**
- `pyproject.toml` instead of older `setup.py`
- Proper dependency management
- ComfyUI Registry integration metadata
- Semantic versioning

### 7. **Web Integration**
- Custom web routes for advanced functionality
- Static asset management
- JavaScript components for UI enhancements

## Project Implementation Status

### Current Structure
```
ComfyUI-NMWaveNodes/
├── __init__.py                    # Central NODE_CONFIG system
├── nodes/                         # Modular file organization
│   ├── text_nodes.py             # Tag processing, text utilities (5 nodes)
│   ├── lora_nodes.py             # LoRA extraction with configurable iterations
│   ├── io_nodes.py               # File loading operations (1 node)
│   └── scheduler_nodes.py        # Wan 2.2 noise scheduling (1 node)
├── utility/                       # Helper functions
├── pyproject.toml                 # Python project configuration
└── CLAUDE.md                      # Documentation
```

### Implemented Features

1. **NODE_CONFIG System**: Automated node mapping generation
2. **Hierarchical Categories**: `NMWave/text`, `NMWave/lora`, `NMWave/io`, `NMWave/scheduler`
3. **Enhanced LoRA Node**: Configurable iterations parameter (1-50, default: 7)
4. **Modular Organization**: Clean separation of concerns

### Node Inventory (8 Total)

**Text Processing (`NMWave/text`):**
- Tag Duplicate Remover
- Tag Alternating Combiner  
- Split Sentences
- Split Tags
- Token Counter

**LoRA Operations (`NMWave/lora`):**
- LoRA Extract and Save

**I/O Operations (`NMWave/io`):**
- Load Text List

**Scheduler Operations (`NMWave/scheduler`):**
- Wan 2.2 Noise Scheduler