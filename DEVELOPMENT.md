# ALCOS Development Guide

This guide covers development setup, architecture, and workflows for contributing to ALCOS.

## Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- NVIDIA CUDA 11.8+ (recommended)
- Docker (for containerized development)
- Git

### Quick Setup

```bash
# Clone repository
git clone https://github.com/rickysanch12/aura.git
cd aura

# Run automated installer
chmod +x install.sh
./install.sh

# Activate virtual environment
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"
```

## Project Structure

```
aura/
├── alcos/                    # Python backend
│   ├── __init__.py
│   ├── core.py              # Main orchestration engine
│   ├── config.py            # Configuration management
│   ├── logger.py            # Logging setup
│   ├── cli.py               # CLI interface
│   ├── agents/              # Agent implementations
│   │   ├── base_agent.py
│   │   ├── agents.py
│   │   └── agent_manager.py
│   ├── models/              # Model management
│   │   ├── model_manager.py
│   │   ├── model_router.py
│   │   └── model_loader.py
│   ├── memory/              # Memory/vector database
│   │   ├── vector_store.py
│   │   ├── memory_manager.py
│   │   └── memory_retriever.py
│   ├── execution/           # Code execution (sandbox)
│   │   └── executor.py
│   └── api/                 # FastAPI endpoints
│       └── server.py
├── frontend/                # React/Electron frontend
│   ├── src/
│   │   ├── pages/           # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Agents.tsx
│   │   │   ├── Models.tsx
│   │   │   ├── Memory.tsx
│   │   │   └── Settings.tsx
│   │   ├── components/      # Reusable components
│   │   │   ├── Header.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── hooks/           # Custom React hooks
│   │   │   └── useWebSocket.ts
│   │   ├── store/           # Zustand state management
│   │   │   └── systemStore.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── electron/            # Electron main process
│   │   └── main.js
│   ├── package.json
│   └── vite.config.ts
├── scripts/                 # Utility scripts
│   ├── install.sh
│   ├── launcher.sh
│   ├── setup_gpu.py
│   └── install-windows.bat
├── docker-compose.yml       # Docker services
├── Dockerfile               # Docker image
├── setup.py                 # Python package setup
├── README.md
└── DEVELOPMENT.md
```

## Backend Development

### Running the Backend Server

```bash
# Development mode with auto-reload
python -m alcos.api.server --reload

# Or using uvicorn directly
uvicorn alcos.api.server:app --reload --host 0.0.0.0 --port 8000
```

### Key Backend Modules

#### Core Engine (`alcos/core.py`)
- Main orchestration of agents, models, and memory
- Implements the primary loop for processing tasks
- Manages system initialization and shutdown

#### Agent Management (`alcos/agents/`)
- `base_agent.py`: Abstract base class for all agents
- `agents.py`: Concrete implementations (Planner, Coder, Debugger, Researcher, Monitor)
- `agent_manager.py`: Lifecycle management and delegation

#### Model Routing (`alcos/models/`)
- `model_manager.py`: Load/unload models, track VRAM
- `model_router.py`: Intelligent task-to-model routing
- `model_loader.py`: Download and verify models

#### Memory System (`alcos/memory/`)
- `vector_store.py`: ChromaDB abstraction layer
- `memory_manager.py`: Add/search/update memory entries
- `memory_retriever.py`: Context retrieval and ranking

#### API Server (`alcos/api/server.py`)
- FastAPI endpoints for REST API
- WebSocket endpoint for real-time communication
- Health checks and status endpoints

### Code Style

Follow PEP 8 with these additions:
- Use type hints for all functions
- Maximum line length: 100 characters
- Use docstrings for classes and complex functions
- Prefer descriptive variable names

```python
from typing import Optional, List

def process_task(
    task_id: str,
    agent_id: str,
    priority: int = 0,
) -> Optional[Dict[str, Any]]:
    """
    Process a single task through an agent.
    
    Args:
        task_id: Unique task identifier
        agent_id: Agent to process task
        priority: Task priority (higher = more urgent)
        
    Returns:
        Task result dictionary or None if failed
    """
    pass
```

## Frontend Development

### Running the Frontend

```bash
cd frontend

# Development with Vite
npm run dev

# Electron development
npm run electron-dev

# Build for production
npm run build
npm run electron-build
```

### Key Frontend Modules

#### Pages (`frontend/src/pages/`)
- `Dashboard.tsx`: System overview with stats and charts
- `Agents.tsx`: Agent management and monitoring
- `Models.tsx`: Model loading/unloading with VRAM tracking
- `Memory.tsx`: Memory search and semantic retrieval
- `Settings.tsx`: System configuration

#### State Management (`frontend/src/store/`)
- `systemStore.ts`: Zustand store for global state
- Tracks agents, models, and system status

#### Hooks (`frontend/src/hooks/`)
- `useWebSocket.ts`: WebSocket connection and message handling
- Auto-reconnect logic
- Message routing to store

### Code Style

- Use TypeScript for type safety
- Functional components with hooks
- Props interfaces for all components
- Tailwind CSS for styling
- ESLint configuration in `frontend/.eslintrc`

## Testing

### Backend Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=alcos tests/

# Run specific test
pytest tests/test_agents.py::test_agent_creation
```

### Frontend Testing

```bash
cd frontend

# Run tests with Vitest
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

## Building for Production

### Backend

```bash
# Build package
python setup.py sdist bdist_wheel

# Install locally
pip install dist/alcos-*.whl
```

### Frontend

```bash
cd frontend

# Build web version
npm run build
# Output: dist/

# Build Electron app
npm run electron-build
# Output: dist/alcos-setup-*.exe (Windows)
#        dist/ALCOS-*.dmg (macOS)
#        dist/alcos-*.AppImage (Linux)
```

### Docker

```bash
# Build image
docker build -t alcos:latest .

# Run container
docker-compose up -d

# Access services
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## Debugging

### Backend Debugging

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python -m alcos.api.server --reload

# Use Python debugger
python -m pdb -m alcos.api.server
```

### Frontend Debugging

```bash
# Electron DevTools
npm run electron-dev
# Press Ctrl+Shift+I to open DevTools

# Chrome DevTools in Electron
Press F12 in the Electron window
```

### WebSocket Debugging

```bash
# Using wscat
npm install -g wscat
wscat -c ws://localhost:8000/ws

# Send messages
{"type": "status"}
{"type": "task", "payload": {"agent_id": "planner", "task": "analyze code"}}
```

## Contributing

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "Add your feature"

# Push to remote
git push origin feature/your-feature

# Create pull request on GitHub
```

### Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] All tests pass
- [ ] No security vulnerabilities

## Performance Optimization

### Profiling

```bash
# Backend profiling
python -m cProfile -s cumulative -m alcos.api.server

# Frontend profiling
# Use Chrome DevTools Performance tab
```

### Memory Usage

```bash
# Check Python memory
python -m memory_profiler alcos/core.py

# GPU memory tracking
nvidia-smi dmon -s pucvmet
```

## Troubleshooting

### Common Issues

**WebSocket Connection Fails**
- Ensure backend is running on port 8000
- Check firewall settings
- Verify CORS configuration in `alcos/config.py`

**Models Won't Load**
- Check VRAM with `nvidia-smi`
- Verify model files exist in `~/.alcos/models/`
- Check `~/.alcos/logs/alcos.log` for errors

**Frontend Build Fails**
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear build cache: `rm -rf dist/`
- Check Node version: `node --version` (should be 18+)

## Documentation

- Keep README.md updated with user-facing changes
- Update DEVELOPMENT.md for developer-facing changes
- Add docstrings to all new functions
- Comment complex logic

## Release Process

```bash
# Tag release
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0

# Build distribution
python setup.py sdist bdist_wheel
cd frontend && npm run electron-build
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Electron Documentation](https://www.electronjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
