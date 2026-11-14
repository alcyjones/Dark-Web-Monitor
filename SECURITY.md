# Security Policy

## Supported versions

This repository is an educational security-monitoring prototype. No release is currently claimed to be production-hardened.

## Reporting a vulnerability

Please **do not** publish sensitive reproduction details or real leaked data in an issue. Contact the repository owner through a private channel or GitHub's private vulnerability reporting feature if enabled.

## Safe operating practices

- Run only against resources you own or are authorized to monitor.
- Keep the web interface bound to localhost or behind authentication and a controlled reverse proxy.
- Do not store real credentials, access tokens, personal data, or sensitive crawl findings in committed files.
- Run the crawler in an isolated environment and monitor network egress.
- Treat collected web content as untrusted input.
- Review the code and the existing SQLite file before using this repository with production information.

## Known hardening backlog

The current prototype contains a hard-coded Flask secret key, starts in debug mode when run directly, and includes a tracked SQLite database. These need remediation before any production deployment. See the repository's security hardening issue.
