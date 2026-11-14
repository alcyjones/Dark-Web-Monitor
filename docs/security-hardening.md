# Security hardening notes

This patch introduces a limited security baseline. It is **not** a full security review.

## Improvements in this change

- Flask secret key is read from `FLASK_SECRET_KEY` or generated randomly for each process. For persisted sessions across restarts, set a strong private value in the environment.
- Direct execution no longer enables Flask debugger.
- URL registration, text import, and traversal enforce strict HTTP(S) v3 `.onion` host syntax, rejecting misleading substrings in paths/domains and unsupported ports.
- Crawling does not automatically follow redirects, reducing the chance of redirecting out of the allowed network.
- URL list uploads are limited to 1 MiB.
- Offline unit tests exercise the new URL validation logic.

## Remaining risks (do not deploy publicly yet)

- The web UI still lacks authentication and CSRF protection; destructive operations include GET routes.
- The crawler's shared `visited_urls` state is not safe for concurrent jobs; implement bounded job queues.
- Stored snippets can contain sensitive information. Treat database files and logs as confidential.
- Existing `darkweb_monitor.db` is already tracked and should be reviewed privately before purging or replacing it with synthetic fixtures.
- The application needs stronger handling of outbound network constraints, URL redirects and connection limits before production exposure.
- A full onion v3 address checksum/version validation and hostname canonicalization are not yet implemented; this patch validates structure only.

## Local test command

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Never run these tests against live external resources; all current tests are offline.
