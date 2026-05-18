# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository is in initialization phase with no existing codebase. This CLAUDE.md will serve as the foundation for documenting architecture and conventions as the project develops.

## Getting Started

When implementing the first features:

1. **Create a README.md** at the root with:
   - Project description and purpose
   - High-level architecture
   - How to build, test, and run the project
   - Development prerequisites

2. **Initialize project structure**:
   - Choose a primary language and set up the appropriate build/package configuration
   - Create a `.gitignore` appropriate for the language and tools
   - Set up linting and testing infrastructure early

3. **Update this CLAUDE.md** once the project structure is established with:
   - Key build and development commands
   - High-level architecture explaining the "big picture"
   - Language-specific conventions and patterns
   - How to run tests (individual and full suite)

## Development Branch Convention

All development occurs on the `claude/add-claude-documentation-fQosk` branch. Follow standard git practices:
- Create feature branches from main when appropriate
- Keep commits clear and descriptive
- Create pull requests as drafts before finalizing

## Next Steps

- Establish the core project type (web app, library, CLI, etc.)
- Define the tech stack
- Create initial project scaffolding
- Document architecture decisions in this file
