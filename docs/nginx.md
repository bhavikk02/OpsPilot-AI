# Nginx 502 Bad Gateway

## Problem

Nginx returns a 502 Bad Gateway error when it cannot successfully communicate with the upstream backend service.

## Common Causes

1. Backend application is down.
2. Nginx is configured with the wrong upstream host or port.
3. Backend service is restarting or unavailable.
4. Network connectivity exists between Nginx and the backend.
5. The upstream application is listening on a different port.

## Troubleshooting

### Check Nginx configuration

Run:

nginx -t

This verifies whether the Nginx configuration syntax is valid.

### Check backend service

Verify that the backend application or service is running.

For a systemd service:

systemctl status <service-name>

### Check listening ports

Run:

ss -lntp

This can be used to identify which processes are listening on which ports.

### Check Nginx logs

Run:

tail -f /var/log/nginx/error.log

The Nginx error log can provide information about upstream connection failures.

## Example

If Nginx is configured to forward traffic to:

http://127.0.0.1:8000

but the backend application is actually listening on:

http://127.0.0.1:8080

Nginx may return a 502 Bad Gateway response.

## Recommended Troubleshooting Order

1. Check Nginx configuration with nginx -t.
2. Check whether the backend service is running.
3. Verify the backend listening port.
4. Verify the Nginx upstream configuration.
5. Check Nginx error logs.
6. Test connectivity between Nginx and the backend.