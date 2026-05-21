"""Code execution sandbox for safe agent code execution."""

import asyncio
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import json
import logging
import signal

from .logger import get_logger

logger = get_logger("alcos.executor")


class ExecutionResult:
    """Result of code execution."""

    def __init__(
        self,
        execution_id: str,
        success: bool,
        output: str = "",
        error: str = "",
        exit_code: int = 0,
        duration: float = 0.0,
        timestamp: Optional[datetime] = None,
    ):
        self.execution_id = execution_id
        self.success = success
        self.output = output
        self.error = error
        self.exit_code = exit_code
        self.duration = duration
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "execution_id": self.execution_id,
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "exit_code": self.exit_code,
            "duration": self.duration,
            "timestamp": self.timestamp.isoformat(),
        }


class CodeExecutor:
    """Executes code in isolated environments."""

    def __init__(
        self,
        timeout: int = 60,
        max_concurrent: int = 4,
        enable_docker: bool = False,
        temp_dir: Optional[Path] = None,
    ):
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.enable_docker = enable_docker
        self.temp_dir = temp_dir or Path(tempfile.gettempdir()) / "alcos_exec"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.active_executions: Dict[str, asyncio.Task] = {}
        self.execution_history: List[ExecutionResult] = []
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def execute_python(
        self,
        code: str,
        variables: Optional[Dict[str, Any]] = None,
        capture_output: bool = True,
    ) -> ExecutionResult:
        """Execute Python code safely."""
        execution_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            # Acquire semaphore to limit concurrent executions
            async with self.semaphore:
                result = await asyncio.wait_for(
                    self._execute_python_internal(
                        execution_id, code, variables, capture_output
                    ),
                    timeout=self.timeout,
                )
                result.duration = (datetime.now() - start_time).total_seconds()
                return result

        except asyncio.TimeoutError:
            logger.error(f"Execution {execution_id} timed out after {self.timeout}s")
            result = ExecutionResult(
                execution_id=execution_id,
                success=False,
                error=f"Execution timed out after {self.timeout} seconds",
                exit_code=124,
                duration=(datetime.now() - start_time).total_seconds(),
            )
            return result

        except Exception as e:
            logger.error(f"Execution {execution_id} failed: {e}", exc_info=True)
            result = ExecutionResult(
                execution_id=execution_id,
                success=False,
                error=str(e),
                exit_code=1,
                duration=(datetime.now() - start_time).total_seconds(),
            )
            return result

    async def _execute_python_internal(
        self,
        execution_id: str,
        code: str,
        variables: Optional[Dict[str, Any]],
        capture_output: bool,
    ) -> ExecutionResult:
        """Internal Python execution implementation."""
        # Create temporary script file
        script_file = self.temp_dir / f"{execution_id}.py"
        try:
            # Prepare execution environment
            env_code = ""
            if variables:
                for key, value in variables.items():
                    env_code += f"{key} = {repr(value)}\n"

            full_code = env_code + "\n" + code

            script_file.write_text(full_code)

            # Execute in subprocess
            loop = asyncio.get_event_loop()
            process = await loop.run_in_executor(
                None,
                self._run_process,
                ["python", str(script_file)],
                capture_output,
            )

            output, error = process

            return ExecutionResult(
                execution_id=execution_id,
                success=True if not error else False,
                output=output,
                error=error,
                exit_code=0 if not error else 1,
            )

        finally:
            # Clean up
            if script_file.exists():
                script_file.unlink()

    def _run_process(
        self, cmd: List[str], capture_output: bool
    ) -> Tuple[str, str]:
        """Run a process and capture output."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                timeout=self.timeout,
            )
            return result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return "", f"Process timed out after {self.timeout} seconds"
        except Exception as e:
            return "", str(e)

    async def execute_shell(self, command: str) -> ExecutionResult:
        """Execute shell command safely."""
        execution_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            async with self.semaphore:
                result = await asyncio.wait_for(
                    self._execute_shell_internal(execution_id, command),
                    timeout=self.timeout,
                )
                result.duration = (datetime.now() - start_time).total_seconds()
                return result

        except asyncio.TimeoutError:
            logger.error(f"Shell execution {execution_id} timed out")
            result = ExecutionResult(
                execution_id=execution_id,
                success=False,
                error=f"Command timed out after {self.timeout} seconds",
                exit_code=124,
                duration=(datetime.now() - start_time).total_seconds(),
            )
            return result

        except Exception as e:
            logger.error(f"Shell execution {execution_id} failed: {e}")
            result = ExecutionResult(
                execution_id=execution_id,
                success=False,
                error=str(e),
                exit_code=1,
                duration=(datetime.now() - start_time).total_seconds(),
            )
            return result

    async def _execute_shell_internal(
        self, execution_id: str, command: str
    ) -> ExecutionResult:
        """Internal shell execution implementation."""
        loop = asyncio.get_event_loop()
        output, error = await loop.run_in_executor(
            None, self._run_shell_process, command
        )

        return ExecutionResult(
            execution_id=execution_id,
            success=not error,
            output=output,
            error=error,
            exit_code=0 if not error else 1,
        )

    def _run_shell_process(self, command: str) -> Tuple[str, str]:
        """Run a shell process."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            return result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return "", f"Command timed out after {self.timeout} seconds"
        except Exception as e:
            return "", str(e)

    async def execute_in_docker(
        self,
        code: str,
        image: str = "python:3.11-slim",
        working_dir: str = "/app",
    ) -> ExecutionResult:
        """Execute code in Docker container."""
        if not self.enable_docker:
            return ExecutionResult(
                execution_id=str(uuid.uuid4()),
                success=False,
                error="Docker execution is not enabled",
                exit_code=1,
            )

        execution_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            async with self.semaphore:
                result = await asyncio.wait_for(
                    self._execute_docker_internal(
                        execution_id, code, image, working_dir
                    ),
                    timeout=self.timeout,
                )
                result.duration = (datetime.now() - start_time).total_seconds()
                return result

        except asyncio.TimeoutError:
            logger.error(f"Docker execution {execution_id} timed out")
            result = ExecutionResult(
                execution_id=execution_id,
                success=False,
                error=f"Docker execution timed out after {self.timeout} seconds",
                exit_code=124,
                duration=(datetime.now() - start_time).total_seconds(),
            )
            return result

        except Exception as e:
            logger.error(f"Docker execution {execution_id} failed: {e}")
            result = ExecutionResult(
                execution_id=execution_id,
                success=False,
                error=str(e),
                exit_code=1,
                duration=(datetime.now() - start_time).total_seconds(),
            )
            return result

    async def _execute_docker_internal(
        self,
        execution_id: str,
        code: str,
        image: str,
        working_dir: str,
    ) -> ExecutionResult:
        """Internal Docker execution implementation."""
        script_file = self.temp_dir / f"{execution_id}.py"
        container_name = f"alcos-exec-{execution_id}"

        try:
            script_file.write_text(code)

            loop = asyncio.get_event_loop()
            output, error = await loop.run_in_executor(
                None,
                self._run_docker_process,
                image,
                container_name,
                str(script_file),
                working_dir,
            )

            return ExecutionResult(
                execution_id=execution_id,
                success=not error,
                output=output,
                error=error,
                exit_code=0 if not error else 1,
            )

        finally:
            if script_file.exists():
                script_file.unlink()

    def _run_docker_process(
        self, image: str, container_name: str, script_path: str, working_dir: str
    ) -> Tuple[str, str]:
        """Run code in Docker container."""
        try:
            cmd = [
                "docker",
                "run",
                "--rm",
                "--name",
                container_name,
                "-v",
                f"{script_path}:/app/script.py",
                image,
                "python",
                "/app/script.py",
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            return result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            # Kill container if it's still running
            subprocess.run(
                ["docker", "kill", container_name],
                capture_output=True,
            )
            return "", f"Docker execution timed out after {self.timeout} seconds"
        except Exception as e:
            return "", str(e)

    def get_execution_status(self) -> Dict[str, Any]:
        """Get executor status."""
        return {
            "active_executions": len(self.active_executions),
            "max_concurrent": self.max_concurrent,
            "timeout": self.timeout,
            "total_executed": len(self.execution_history),
            "docker_enabled": self.enable_docker,
            "temp_dir": str(self.temp_dir),
        }

    def get_execution_history(
        self, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent execution history."""
        return [
            result.to_dict()
            for result in self.execution_history[-limit:]
        ]

    async def cleanup(self) -> None:
        """Cleanup executor resources."""
        # Cancel all active executions
        for task in self.active_executions.values():
            if not task.done():
                task.cancel()

        # Wait for all executions to complete or cancel
        if self.active_executions:
            await asyncio.gather(
                *self.active_executions.values(),
                return_exceptions=True,
            )

        # Clean up temporary files
        if self.temp_dir.exists():
            for file in self.temp_dir.glob("*.py"):
                try:
                    file.unlink()
                except Exception as e:
                    logger.warning(f"Failed to cleanup {file}: {e}")

        logger.info("Executor cleanup complete")


# Global executor instance
_executor: Optional[CodeExecutor] = None


def get_executor(
    timeout: int = 60,
    max_concurrent: int = 4,
    enable_docker: bool = False,
) -> CodeExecutor:
    """Get or create the executor instance."""
    global _executor
    if _executor is None:
        _executor = CodeExecutor(
            timeout=timeout,
            max_concurrent=max_concurrent,
            enable_docker=enable_docker,
        )
    return _executor
