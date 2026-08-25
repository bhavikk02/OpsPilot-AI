# Kubernetes Pod CrashLoopBackOff

## Problem

Kubernetes reports CrashLoopBackOff when a container starts, crashes, and Kubernetes repeatedly attempts to restart it.

## Common Causes

1. Application inside the container is crashing.
2. Incorrect environment variables or configuration.
3. Missing configuration or secrets.
4. Container command or entrypoint is incorrect.
5. Application is unable to connect to a required dependency.
6. Resource limits are causing the container to be terminated.

## Troubleshooting

### Check pod status

Run:

kubectl get pods

This shows the current status of pods in the namespace.

### Check pod details

Run:

kubectl describe pod <pod-name>

This provides information about the pod, including events and container status.

### Check container logs

Run:

kubectl logs <pod-name>

The container logs can provide information about application startup failures.

### Check previous container logs

If the container has already restarted, run:

kubectl logs <pod-name> --previous

This can show logs from the previous container instance.

## Example

If a container starts an application that immediately crashes because of a missing environment variable, Kubernetes may repeatedly restart the container and eventually show CrashLoopBackOff.

## Recommended Troubleshooting Order

1. Check pod status with kubectl get pods.
2. Check pod events with kubectl describe pod <pod-name>.
3. Check current container logs with kubectl logs <pod-name>.
4. Check previous container logs with kubectl logs <pod-name> --previous.
5. Verify environment variables, configuration, and dependencies.