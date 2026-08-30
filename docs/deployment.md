# Deployment guide

## 1. Prepare the host

Use a supported Ubuntu Server release. Apply security updates, create a non-root administrative user, configure SSH keys, and allow only required inbound ports.

Minimum public ports:

- `22/tcp` restricted to trusted administration sources.
- `80/tcp` for ACME validation and HTTPS redirection.
- `443/tcp` for the application.

Do not expose `3306/tcp` or `8080/tcp` publicly.

## 2. Install Docker

Install Docker Engine and the Compose plugin using Docker's supported Ubuntu repository. Verify:

```bash
docker version
docker compose version
```

## 3. Configure the project

```bash
git clone https://github.com/ingmarbol/mundoactivate-platform.git
cd mundoactivate-platform
cp .env.example .env
chmod 600 .env
```

Generate unique random secrets and replace every placeholder. Never reuse the database root password for the Moodle application user.

## 4. Validate and deploy

```bash
docker compose config
docker compose build --pull
docker compose up -d
docker compose ps
./scripts/health-check.sh
```

## 5. Configure Nginx and TLS

Copy `nginx/moodle.conf.example` to the host Nginx configuration, replace the example hostname, validate, and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Issue and renew TLS certificates with the host's approved ACME client.

## 6. Complete Moodle installation

Browse to the HTTPS hostname and complete the Moodle setup using:

- Database host: `mariadb`
- Database name and user: values from `.env`
- Moodle data directory: `/var/www/moodledata`

Do not paste production secrets into documentation or screenshots.
