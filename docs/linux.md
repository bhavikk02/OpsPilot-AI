# Linux Troubleshooting

## High CPU Usage

### Problem

A Linux server is experiencing consistently high CPU utilization.

### Common Causes

- A process is consuming excessive CPU.
- Too many processes are running.
- A runaway application or background job is consuming CPU.
- A service is stuck or repeatedly restarting.

### Troubleshooting

Check overall CPU and process usage:

```bash
top
```

List processes sorted by CPU usage:

```bash
ps aux --sort=-%cpu | head
```

Check the number of CPU cores:

```bash
nproc
```

Check system load:

```bash
uptime
```

### Resolution

Identify the process consuming excessive CPU and determine whether it is expected.

If a process needs to be stopped gracefully:

```bash
kill <PID>
```

If the process does not stop gracefully:

```bash
kill -9 <PID>
```

Before terminating a production process, verify the process and understand its impact.

---

## High Memory Usage

### Problem

A Linux server is running low on available memory or applications are experiencing out-of-memory conditions.

### Common Causes

- An application is consuming excessive memory.
- A process has a memory leak.
- Too many services are running.
- The server does not have sufficient memory for the workload.

### Troubleshooting

Check memory usage:

```bash
free -h
```

Check processes sorted by memory usage:

```bash
ps aux --sort=-%mem | head
```

Check running processes:

```bash
top
```

### Resolution

Identify the process consuming excessive memory and investigate the application or service.

Restarting a service may temporarily resolve the issue, but the underlying cause should be investigated to prevent recurrence.

---

## Disk Space Full

### Problem

A Linux server has little or no available disk space.

### Common Causes

- Application logs are growing continuously.
- Temporary files are not being removed.
- Old backups or artifacts are consuming storage.
- A filesystem has reached its inode limit.

### Troubleshooting

Check filesystem usage:

```bash
df -h
```

Check inode usage:

```bash
df -i
```

Find large directories:

```bash
du -sh /* 2>/dev/null
```

Find large files under `/var`:

```bash
find /var -type f -size +500M -exec ls -lh {} \;
```

### Resolution

Identify unnecessary files and clean them safely.

For logs, check whether log rotation is configured correctly.

Do not delete files blindly from production systems. Verify that files are safe to remove before cleanup.

---

## Service Not Running

### Problem

A Linux service is stopped, failed, or not responding.

### Common Causes

- Invalid configuration.
- Missing dependency.
- Permission problems.
- Port conflicts.
- Application startup failure.
- Insufficient system resources.

### Troubleshooting

Check service status:

```bash
systemctl status <service>
```

Start the service:

```bash
sudo systemctl start <service>
```

Restart the service:

```bash
sudo systemctl restart <service>
```

Enable the service at boot:

```bash
sudo systemctl enable <service>
```

Check recent service logs:

```bash
journalctl -u <service> --since "30 minutes ago"
```

### Resolution

Check the service status and logs first.

Identify the underlying configuration, dependency, permission, port, or resource issue before restarting the service.

---

## Process Troubleshooting

### Problem

A process is not behaving as expected or needs to be identified.

### Troubleshooting

List running processes:

```bash
ps aux
```

Search for a specific process:

```bash
ps aux | grep <process>
```

Find a process by name:

```bash
pgrep <process>
```

Get detailed information about a process:

```bash
ps -p <PID> -f
```

Check processes interactively:

```bash
top
```

### Resolution

Identify the process, understand what service or application owns it, and investigate its logs before terminating it.

Terminate a process gracefully only when required:

```bash
kill <PID>
```

Use a forceful termination only when a graceful termination does not work:

```bash
kill -9 <PID>
```

---

## File and Directory Permissions

### Problem

An application or user cannot read, write, or execute a file or directory.

### Common Causes

- Incorrect file ownership.
- Incorrect file permissions.
- The application is running under a different user.
- The user is not part of the required group.

### Troubleshooting

Check file permissions:

```bash
ls -l <file>
```

Check directory permissions:

```bash
ls -ld <directory>
```

Check the current user:

```bash
whoami
```

Check group membership:

```bash
groups
```

### Resolution

Change ownership when appropriate:

```bash
sudo chown <user>:<group> <file>
```

Change permissions when appropriate:

```bash
chmod <permissions> <file>
```

Verify the required access after making the change.

Avoid using overly permissive permissions such as `777` as a default solution.

---

## Network Connectivity Troubleshooting

### Problem

A Linux server cannot connect to another host or service.

### Common Causes

- DNS resolution failure.
- Incorrect routing.
- Firewall rules blocking traffic.
- The destination service is not listening.
- Incorrect hostname or port.

### Troubleshooting

Check basic connectivity:

```bash
ping <host>
```

Check DNS resolution:

```bash
nslookup <hostname>
```

or:

```bash
dig <hostname>
```

Check whether a remote port is reachable:

```bash
nc -zv <host> <port>
```

Check listening ports:

```bash
ss -tulnp
```

Check the routing table:

```bash
ip route
```

### Resolution

Determine whether the problem is related to DNS, routing, firewall rules, or the destination service.

Verify the hostname, port, network route, firewall configuration, and destination service.

---

## Log Troubleshooting

### Problem

An application or service is failing and logs need to be inspected.

### Troubleshooting

View system logs:

```bash
journalctl
```

View logs for a specific service:

```bash
journalctl -u <service>
```

Follow service logs in real time:

```bash
journalctl -u <service> -f
```

Search a log file for errors:

```bash
grep "ERROR" <logfile>
```

View the latest lines:

```bash
tail -n 100 <logfile>
```

Follow a log file:

```bash
tail -f <logfile>
```

### Resolution

Look for:

- Error messages.
- Timestamps.
- Repeated failures.
- Configuration errors.
- Dependency failures.
- Resource-related errors.

Correlate the logs with the time when the problem started.

---

## Linux Disk and File Investigation

### Problem

A server is experiencing unexpected disk usage and the source of the usage needs to be identified.

### Troubleshooting

Check filesystem usage:

```bash
df -h
```

Check directory sizes:

```bash
du -sh <directory>
```

Check the contents of a directory:

```bash
ls -lah <directory>
```

Find large files:

```bash
find <directory> -type f -size +100M -exec ls -lh {} \;
```

### Resolution

Identify which directory or files are consuming the storage.

Check whether the files are logs, temporary files, application data, backups, or other required resources before removing anything.

---

## Linux Port Troubleshooting

### Problem

An application cannot start because a required port may already be in use.

### Troubleshooting

Check listening ports:

```bash
ss -tulnp
```

Check a specific port:

```bash
ss -tulnp | grep <port>
```

Identify the process using a port:

```bash
lsof -i :<port>
```

### Common Causes

- Another application is already using the port.
- A previous instance of the application is still running.
- The application configuration uses an incorrect port.

### Resolution

Identify the process using the port and determine whether it should be running.

If the process is no longer required, stop it safely and restart the intended application.

---

## Linux Troubleshooting Workflow

When troubleshooting a Linux production issue:

1. Identify the affected server, application, or service.
2. Check CPU, memory, disk, and system load.
3. Check the affected service status.
4. Review application and system logs.
5. Check processes and resource consumption.
6. Check file permissions when access is failing.
7. Check network connectivity when the issue involves another service.
8. Check ports when an application cannot bind or connect.
9. Identify the root cause before applying a change.
10. Apply the smallest safe remediation.
11. Verify that the service and system have recovered.