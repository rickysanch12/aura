# Agentic Local Core OS

An elite, production-grade local autonomous AI operating system that brings together multiple models, agents, and infrastructure in a unified desktop experience.

## Overview

Agentic Local Core OS (ALCOS) is a fully-integrated local AI ecosystem designed to run entirely on your desktop with:

- **Multi-Model Orchestration**: OpenClaw, Hermes, Blackbox, and other local models
- **Autonomous Agents**: Specialized agents for planning, coding, debugging, research, and optimization
- **Long-Term Memory**: Vector database with semantic retrieval and project linking
- **Live GUI Dashboard**: Real-time monitoring of agents, models, memory, and tasks
- **Self-Improving Pipelines**: Autonomous optimization, failure analysis, and workflow refinement
- **Local Code Execution**: Sandboxed environments for testing, debugging, and deployment
- **Desktop Integration**: Auto-launch on boot, persistent services, system tray integration

## Quick Start

### Prerequisites
- Ubuntu 22.04+ (or WSL2) / Windows / macOS
- Python 3.10+
- Node.js 18+
- 16GB+ RAM (32GB+ recommended)
- NVIDIA GPU with CUDA 11.8+ (recommended) or AMD GPU with ROCm

### Installation

```bash
# Clone and navigate
cd aura

# Run automated installer
chmod +x ./scripts/install.sh
./scripts/install.sh

# Or use pip/npm directly
pip install -e .
cd frontend && npm install && npm run build
```

### Launch

```bash
# From anywhere
agentic-core-os

# Or directly
python -m alcos.core
```

The system will:
1. Initialize all services
2. Download required models
3. Start the backend server
4. Launch the Electron GUI
5. Begin listening for commands

## Architecture

```
Agentic Local Core OS
├── Backend (Python/FastAPI)
│   ├── Model Orchestration & Routing
│   ├── Agent Orchestration & Communication
│   ├── Memory Management & Vector DB
│   ├── Code Execution & Sandboxing
│   ├── Self-Improvement Systems
│   └── WebSocket Streaming
├── Frontend (Electron/React)
│   ├── Agent Dashboard
│   ├── Model Monitor
│   ├── Memory Browser
│   ├── Project Manager
│   ├── Terminal & Logs
│   └── Settings Manager
├── Models (Local)
│   ├── OpenClaw (Planning & Reasoning)
│   ├── Hermes (Code & Analysis)
│   ├── Blackbox (Code Gen)
│   └── Embeddings (Memory)
└── Infrastructure
    ├── Vector Memory (ChromaDB/Qdrant)
    ├── Project Management
    ├── Configuration
    └── Desktop Integration
```

## Key Features

### 1. Multi-Model Orchestration
- Automatic task routing to optimal models
- Concurrent inference with GPU management
- Model hot-swapping and fallback chains
- VRAM-aware scheduling

### 2. Autonomous Agents
- **Planner**: Strategic task decomposition
- **Coder**: Autonomous code generation and debugging
- **Architect**: System design and refactoring
- **Research**: Information gathering and analysis
- **Memory**: Knowledge management and retrieval
- **Monitor**: System health and performance
- **Optimizer**: Continuous improvement loops

### 3. Live Memory System
- Semantic vector embeddings
- Project-linked memory graphs
- Conversation threading
- Automatic summarization
- Multi-level retrieval

### 4. Self-Improvement
- Workflow optimization
- Prompt refinement
- Performance analytics
- Bottleneck detection
- Safe rollback mechanisms

### 5. Desktop Integration
- One-click launcher
- System tray support
- Auto-boot on login
- Desktop shortcuts
- CLI integration

## Development

### Build System

```bash
# Backend development
pip install -e ".[dev]"
python -m pytest tests/

# Frontend development
cd frontend
npm run dev  # Hot reload

# Full system
python scripts/build.py
```

### Project Structure

```
alcos/
├── core/                 # Main orchestration
├── agents/              # Agent implementations
├── models/              # Model routing & management
├── memory/              # Vector DB & retrieval
├── execution/           # Code execution sandbox
├── api/                 # FastAPI endpoints
├── config/              # Configuration management
└── utils/               # Utilities

frontend/
├── src/
│   ├── components/      # React components
│   ├── pages/          # Page layouts
│   ├── store/          # Redux state
│   ├── websocket/      # WebSocket client
│   └── styles/         # Tailwind CSS
├── electron/           # Electron main process
└── public/             # Static assets
```

## Configuration

### Environment Variables
```
ALCOS_HOME=~/.alcos
ALCOS_MODELS_PATH=~/.alcos/models
ALCOS_MEMORY_DB=chromadb
CUDA_VISIBLE_DEVICES=0
LOG_LEVEL=INFO
```

### Model Configuration
Edit `config/models.yaml` to:
- Add/remove models
- Adjust VRAM limits
- Set model priorities
- Configure fallback chains

### Agent Configuration
Edit `config/agents.yaml` to:
- Enable/disable agents
- Configure capabilities
- Set memory limits
- Define communication rules

## GPU Optimization

### NVIDIA CUDA
```bash
# Automatic detection and setup
python scripts/setup_gpu.py

# Manual config
export CUDA_VISIBLE_DEVICES=0
export CUDA_LAUNCH_BLOCKING=0
```

### AMD ROCm
```bash
python scripts/setup_gpu.py --rocm
export HSA_OVERRIDE_GFX_VERSION=gfx90a  # Adjust for your GPU
```

## Monitoring

### Dashboard Access
- Local: http://localhost:5173 (during dev)
- GUI: Electron app (production)

### Logs
```bash
# Stream logs
tail -f ~/.alcos/logs/alcos.log

# View by component
tail -f ~/.alcos/logs/agents.log
tail -f ~/.alcos/logs/models.log
tail -f ~/.alcos/logs/memory.log
```

### Performance Metrics
- GPU utilization
- Agent queue depth
- Model inference time
- Memory hit rates
- Task success rates

## CLI Commands

```bash
# System control
agentic-core-os start
agentic-core-os stop
agentic-core-os restart
agentic-core-os status

# Model management
agentic-core-os models list
agentic-core-os models pull openclaw
agentic-core-os models cache clear

# Agent control
agentic-core-os agents list
agentic-core-os agents enable planner
agentic-core-os agents stats

# Memory management
agentic-core-os memory search "query"
agentic-core-os memory compact
agentic-core-os memory export

# Project management
agentic-core-os project create myproject
agentic-core-os project load myproject
agentic-core-os project list
```

## Advanced Features

### Safe Self-Modification
- Sandboxed execution
- Automatic snapshots
- Rollback on failure
- Audit logging

### Autonomous Debugging
- Stack trace analysis
- Root cause detection
- Solution generation
- Automated repair

### Workflow Optimization
- Performance profiling
- Bottleneck identification
- Prompt refinement
- Routing optimization

## Troubleshooting

### Models Won't Load
```bash
# Check VRAM
nvidia-smi

# Download specific model
python -m alcos.models download openclaw --force

# Verify installation
python -m alcos.test.models
```

### Agents Not Responding
```bash
# Check service status
python -m alcos.health_check

# Restart service
agentic-core-os restart agents

# View logs
tail -f ~/.alcos/logs/agents.log
```

### Memory Issues
```bash
# Compact memory
agentic-core-os memory compact

# Clear cache
agentic-core-os memory cache clear

# Verify database
python -m alcos.verify_memory_db
```

## License

Proprietary - Elite Autonomous Systems

## Support

For issues, feature requests, or contributions, refer to the development documentation.

---

**Agentic Local Core OS**: Where autonomous AI meets elite desktop infrastructure.
