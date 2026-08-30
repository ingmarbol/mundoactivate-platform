# Security and publication checklist

## Never commit

- `.env` or real environment files.
- Passwords, tokens, API keys, SSH keys, or TLS private keys.
- Database dumps, Moodle data archives, or logs with user data.
- Private IP addresses, firewall exports, server inventories, or administrative URLs.
- Student, tutor, customer, or employee information.

## Host controls

- Patch Ubuntu, Docker, Nginx, Moodle, and MariaDB regularly.
- Use SSH keys, disable direct root login, and restrict administration sources.
- Apply a deny-by-default firewall policy.
- Expose only ports 80 and 443 publicly; restrict port 22.
- Monitor storage, certificate expiry, service health, authentication failures, and backup results.

## Container controls

- Pin reviewed image versions.
- Use `no-new-privileges` where compatible.
- Do not publish MariaDB ports.
- Do not mount the Docker socket into application containers.
- Review images for vulnerabilities before deployment.

## Git history

Removing a secret in a later commit does not remove it from Git history. If a secret is ever committed:

1. Revoke and rotate it immediately.
2. Remove it from history using an approved history-rewrite procedure.
3. Review access logs and downstream copies.
4. Document the incident without reproducing the secret.
