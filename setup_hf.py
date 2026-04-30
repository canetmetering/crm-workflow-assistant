import subprocess

result = subprocess.run(
    "git add -A && git commit -m 'Add Docker setup and API server' && git push hf main",
    shell=True,
    capture_output=True,
    text=True
)
print(result.stdout)
print(result.stderr)
print(f"returncode: {result.returncode}")
