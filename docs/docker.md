# Docker Container Restarting

## Problem

A Docker container may repeatedly restart when the application inside the container exits or when the container is configured with an automatic restart policy.

## Common Causes

1. Application inside the container is crashing.
2. Incorrect environment variables.
3. Incorrect container command or entrypoint.
4. Missing configuration or dependencies.
5. Application is listening on the wrong port.
6. Container restart policy is enabled.

## Troubleshooting

### Check running containers

Run:

docker ps

This shows currently running Docker containers.

### Check all containers

Run:

docker ps -a

This shows running and stopped containers.

### Check container logs

Run:

docker logs <container-name>

Container logs can provide information about application startup or runtime failures.

### Inspect the container

Run:

docker inspect <container-name>

This provides detailed information about the container configuration.

### Check restart policy

Run:

docker inspect <container-name>

Inspect the restart policy to determine whether Docker is configured to automatically restart the container.

## Example

If an application inside a container starts and immediately exits because of a missing environment variable, Docker may repeatedly restart the container when an automatic restart policy is configured.

## Recommended Troubleshooting Order

1. Check containers with docker ps -a.
2. Check container logs with docker logs <container-name>.
3. Inspect the container configuration.
4. Verify environment variables and application configuration.
5. Verify the container command and entrypoint.
6. Check the restart policy.