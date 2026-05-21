"""Command-line interface for ALCOS."""

import asyncio
import click
from pathlib import Path
import logging
from typing import Optional

from .core import get_core_os, AgenticCoreOS
from .config import get_config
from .logger import setup_logging
from .api.server import run_server


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option("--home", type=click.Path(), help="ALCOS home directory")
def cli(debug: bool, home: Optional[str]):
    """Agentic Local Core OS - Elite autonomous AI system."""
    if debug:
        setup_logging(level="DEBUG")
    if home:
        config = get_config()
        config.settings.home_dir = Path(home)


@cli.command()
def start():
    """Start ALCOS system."""
    async def _start():
        core_os = get_core_os()
        await core_os.initialize()
        await core_os.start()

        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            click.echo("\nShutting down...")
            await core_os.stop()

    asyncio.run(_start())


@cli.command()
def stop():
    """Stop ALCOS system."""
    async def _stop():
        core_os = get_core_os()
        await core_os.stop()

    asyncio.run(_stop())
    click.echo("ALCOS stopped")


@cli.command()
def status():
    """Get ALCOS status."""
    async def _status():
        core_os = get_core_os()
        status = await core_os.get_status()

        click.echo(f"Running: {status['running']}")
        click.echo(f"Initialized: {status['initialized']}")
        if status.get('uptime'):
            click.echo(f"Uptime: {status['uptime']:.0f}s")

        agents = status.get("agents", {})
        click.echo(f"Agents: {agents.get('total_agents', 0)} total")
        click.echo(f"  Active: {agents.get('active_agents', 0)}")

    asyncio.run(_status())


@cli.command()
def server():
    """Run API server."""
    click.echo("Starting ALCOS API server...")
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        click.echo("\nServer stopped")


@cli.group()
def models():
    """Model management commands."""
    pass


@models.command()
def list_models():
    """List available models."""
    async def _list():
        core_os = get_core_os()
        models = await core_os.get_available_models()

        click.echo(f"\nAvailable Models ({len(models)} total):")
        click.echo("-" * 70)

        for model in models:
            status = "✓ loaded" if model["is_loaded"] else (
                "↓ available" if model["is_downloaded"] else "⨯ not downloaded"
            )
            click.echo(
                f"  {model['id']:15} {model['name']:25} {status:15} "
                f"[{model['size']} | {model['type']}]"
            )

    asyncio.run(_list())


@models.command()
@click.argument("model_id")
def load(model_id: str):
    """Load a model."""
    async def _load():
        core_os = get_core_os()
        success = await core_os.model_manager.load_model(model_id)
        if success:
            click.echo(f"✓ Loaded {model_id}")
        else:
            click.echo(f"✗ Failed to load {model_id}")

    asyncio.run(_load())


@models.command()
@click.argument("model_id")
def unload(model_id: str):
    """Unload a model."""
    async def _unload():
        core_os = get_core_os()
        success = await core_os.model_manager.unload_model(model_id)
        if success:
            click.echo(f"✓ Unloaded {model_id}")
        else:
            click.echo(f"✗ Failed to unload {model_id}")

    asyncio.run(_unload())


@cli.group()
def agents():
    """Agent management commands."""
    pass


@agents.command()
def list_agents():
    """List agents."""
    async def _list():
        core_os = get_core_os()
        agents_list = await core_os.get_agents()

        click.echo(f"\nAgents ({len(agents_list)} total):")
        click.echo("-" * 70)

        for agent in agents_list:
            status = "🟢 active" if agent.get("is_active") else "⚫ inactive"
            click.echo(
                f"  {agent['name']:15} {agent['type']:15} {status}"
            )

    asyncio.run(_list())


@cli.group()
def memory():
    """Memory management commands."""
    pass


@memory.command()
@click.argument("query")
@click.option("-l", "--limit", type=int, default=5, help="Number of results")
def search(query: str, limit: int):
    """Search memory."""
    async def _search():
        core_os = get_core_os()
        results = await core_os.search_memory(query, limit)

        click.echo(f"\nSearch Results for: {query}")
        click.echo("-" * 70)

        for i, result in enumerate(results, 1):
            content = result.get("content", "")[:100]
            similarity = result.get("similarity", 0)
            click.echo(f"  {i}. [{similarity:.1%}] {content}")

    asyncio.run(_search())


@memory.command()
def stats():
    """Memory statistics."""
    async def _stats():
        core_os = get_core_os()
        stats = await core_os.memory_manager.get_memory_stats()

        click.echo(f"\nMemory Statistics:")
        click.echo("-" * 70)
        click.echo(f"  Total entries: {stats.get('total_entries', 0)}")
        click.echo(f"  Cache size: {stats.get('cache_size', 0)}")

    asyncio.run(_stats())


@cli.group()
def config():
    """Configuration commands."""
    pass


@config.command()
def show():
    """Show configuration."""
    conf = get_config()
    settings = conf.settings.model_dump()

    click.echo("\nConfiguration:")
    click.echo("-" * 70)

    for key, value in sorted(settings.items()):
        if not str(key).startswith("_"):
            click.echo(f"  {key:30} {value}")


def main():
    """Main entry point."""
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Exit(1)


if __name__ == "__main__":
    main()
