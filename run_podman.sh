#!/bin/bash

# Build the Docker image using Podman
podman build -t mach .

# Run the Docker container using Podman
podman run -d --name mach-container -p 8000:8000 mach
