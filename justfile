# List available commands
default:
    @just --list --unsorted

# Build the sandbox image
[group("ai sandbox")]
build-sandbox:
    docker build -f sandbox.Dockerfile -t sandbox-python-anything:latest .
    docker sandbox create -t sandbox-python-anything:latest opencode .

# Run the sandbox container
run-sandbox:
    docker sandbox run -t sandbox-python-anything:latest opencode .
