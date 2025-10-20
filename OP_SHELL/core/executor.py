# op_shell/executor.py
import subprocess
import sys
from typing import Optional

def execute_in_sandbox(
    command: str,
    image: str = "op-shell-sandbox",
    timeout: int = 30
) -> Optional[str]:
    """
    Run a shell command inside a locked-down Docker container.
    Returns output on success, None on error.
    """
    full_cmd = ["sh", "-c", command]

    docker_cmd = [
        "docker", "run", "--rm",
        "--read-only",                     # Root filesystem read-only
        "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",  # Limited writable temp space
        "--cap-drop=ALL",                  # Drop all Linux capabilities
        "--security-opt=no-new-privileges:true",      # Prevent privilege escalation
        "--network=none",                  # Disable network
        "--pids-limit=64",                 # Max 64 processes
        "--memory=128m",                   # Memory limit
        "--cpus=0.5",                      # CPU limit
        "--user=1000:1000",                # Run as non-root user (UID 1000 = typical dev)
        "--security-opt=seccomp=unconfined",  # Optional: remove if you define a custom seccomp profile later
        image
    ] + full_cmd

    try:
        
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"⚠️  Command failed (exit {result.returncode})", file=sys.stderr)
            print(f"stderr: {result.stderr}", file=sys.stderr)
            return None
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("❌ 'docker' not found. Please install Docker.", file=sys.stderr)
        return None

def execute_on_host(command: str, timeout: int = 30) -> Optional[str]:
    """⚠️ DANGEROUS: Runs command directly on host. Use with extreme caution."""
    import subprocess, sys
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"⚠️  Host command failed (exit {result.returncode})", file=sys.stderr)
            print(f"stderr: {result.stderr}", file=sys.stderr)
            return None
    except subprocess.TimeoutExpired:
        print("⏰ Host command timed out", file=sys.stderr)
        return None
 
DANGEROUS_PATTERNS = [
    "rm -rf", "dd if=", "mkfs", "chmod 777", ":(){ :|:& };:", "sudo su"
]

def is_command_safe(cmd: str) -> bool:
    cmd_lower = cmd.lower()
    return not any(pattern in cmd_lower for pattern in DANGEROUS_PATTERNS)