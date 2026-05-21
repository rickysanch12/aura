# Complete ALCOS & Projects Setup Guide

## ✅ Desktop Launcher Setup (Windows)

### Quick Setup - 2 Steps:

1. **Download & Run**:
   - Get `SETUP_ALCOS_DESKTOP.bat` from this repository
   - Double-click it to run (no admin rights needed on first run)
   - This automatically creates an "ALCOS" shortcut on your Windows desktop

2. **Launch ALCOS**:
   - Double-click the "ALCOS" icon on your desktop
   - First launch will check prerequisites and install dependencies
   - The system will start automatically

### What Happens on First Launch:

1. ✓ Verifies Python 3.10+ installation
2. ✓ Checks Node.js installation  
3. ✓ Creates Python virtual environment
4. ✓ Installs all dependencies (Python packages)
5. ✓ Installs Node.js dependencies
6. ✓ Starts backend API server (localhost:8000)
7. ✓ Starts frontend Electron app

### Advanced Setup - Manual Installation:

If you prefer manual control:

**Option A - PowerShell** (Windows 10+):
```powershell
# Run in PowerShell
cd path\to\aura
.\WINDOWS_DESKTOP_SETUP.ps1
```

**Option B - Command Prompt**:
```cmd
# Run in Command Prompt
cd path\to\aura
SETUP_ALCOS_DESKTOP.bat
```

---

## 📁 Project Structure

### Three Integrated Projects:

#### 1. **ALCOS** (aura/)
- **Purpose**: Elite local autonomous AI system
- **Components**: 
  - Backend: FastAPI + Ollama integration
  - Frontend: Electron + React
  - Agents: Specialized autonomous agents
  - Memory: Vector search with ChromaDB
  - Code Execution: Sandboxed Python/Shell execution
  
**Launch**: Double-click desktop shortcut OR run `scripts/alcos-launcher.bat`

#### 2. **Skills** (skills/)
- **Purpose**: Reusable Claude Code skill components
- **Contains**: 30+ skills including:
  - PDF, DOCX, XLSX manipulation
  - Canvas design tools
  - API client generation
  - Documentation tools
  - MCP server builder

**Usage**: Reference implementations for Claude Code integration

#### 3. **Desktop Tutorial** (desktop-tutorial/)
- **Purpose**: Desktop app development reference
- **Covers**: Electron patterns, UI design, system integration
- **Status**: Reference material repository

---

## 🚀 Core ALCOS Capabilities

### Agent System
- **Agents**: Planner, Coder, Debugger, Researcher, Monitor
- **Code Submission**: Agents submit code for user review
- **Code Generation**: Agents can propose and write code
- **Task Delegation**: Automatic distribution of work

### APIs Available

#### Agent Management
- `GET /agents` - List all agents
- `GET /agents/{agent_id}` - Get specific agent
- `POST /agents/{agent_id}/task` - Submit task
- `POST /agents/{agent_id}/submit_code` - Code submission

#### Code Management  
- `GET /code/submissions` - View all code submissions
- `POST /code/submissions/clear` - Clear history
- `POST /code/execute/{index}` - Execute submission

#### Models
- `GET /models` - List available models
- `POST /models/{model_id}/download` - Download from Ollama
- `POST /models/{model_id}/generate` - Text generation
- `POST /models/{model_id}/chat` - Chat interface

#### Execution
- `POST /execute/python` - Run Python code
- `POST /execute/shell` - Run shell commands
- `GET /execute/status` - Execution status

#### Memory
- `POST /memory` - Store information
- `GET /memory/search` - Vector search
- `GET /memory/stats` - Storage statistics

### WebSocket Support
- Real-time agent updates
- Live task monitoring
- Streaming model outputs
- Interactive debugging

---

## 📋 Installation Checklist

- [ ] Windows desktop launcher created (`SETUP_ALCOS_DESKTOP.bat` exists)
- [ ] Desktop shortcut installed (visible on desktop)
- [ ] ALCOS launched at least once
- [ ] Backend server running on port 8000
- [ ] Frontend Electron app opened
- [ ] All dependencies installed
- [ ] Agent system responsive
- [ ] Code submission working

---

## 🔧 Troubleshooting

### Issue: "Python not found"
**Solution**: Install Python 3.10+ from python.org, add to PATH

### Issue: "Node.js not found"  
**Solution**: Install Node.js 18+ from nodejs.org

### Issue: Port 8000 already in use
**Solution**: Change `API_PORT` in `.env` file or kill process using port 8000

### Issue: Electron app won't open
**Solution**: Check backend is running (look for console window), wait 5 seconds, try again

### Issue: Agents not responding
**Solution**: Restart ALCOS, check system resources (RAM, CPU)

---

## 📚 Key Files & Directories

```
aura/
├── SETUP_ALCOS_DESKTOP.bat       ← Run this to setup desktop launcher
├── WINDOWS_DESKTOP_SETUP.ps1     ← PowerShell alternative
├── alcos/                         ← Python backend
│   ├── agents/                   ← Agent implementations
│   ├── api/                      ← FastAPI endpoints
│   ├── models/                   ← Model management
│   ├── executor.py               ← Code execution sandbox
│   └── core.py                   ← Main orchestrator
├── frontend/                      ← Electron app
│   ├── src/
│   ├── public/
│   └── package.json
├── scripts/
│   ├── alcos-launcher.bat        ← Main launcher
│   └── alcos-launcher.ps1        ← PowerShell launcher
├── setup.py                       ← Python package config
├── docker-compose.yml             ← Docker setup
└── README.md                      ← Full documentation
```

---

## 🎯 Quick Start Commands

**Start ALCOS**:
```bash
./scripts/alcos-launcher.bat    # Windows Batch
./scripts/alcos-launcher.ps1    # Windows PowerShell
./scripts/launcher.sh           # Linux/Mac
```

**Access Web UI**:
- Backend API: http://localhost:8000
- WebSocket: ws://localhost:8000/ws
- Frontend: Electron window auto-opens

**Development**:
```bash
cd alcos && python -m pytest      # Run tests
cd frontend && npm start          # Dev server
```

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs in console window
3. Check `/memory/stats` for system health
4. Examine recent agent submissions at `/code/submissions`

---

## 🔐 Security Notes

- Code execution is sandboxed
- Ollama runs locally (no cloud)
- All agents operate on local machine
- Memory stored locally in ChromaDB
- No external API keys required

---

**Status**: ✅ All systems operational
**Last Updated**: 2026-05-21
**Version**: 1.0.0

