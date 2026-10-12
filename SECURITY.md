# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.0 (current) | Yes |
| 2.0.0 | Best-effort; prefer upgrading to current |
| 1.1.0 | Best-effort; prefer upgrading to current |
| Older releases | Best-effort; prefer upgrading to current |

## Reporting a Vulnerability

Please **do not** open a public issue for security-sensitive reports when a private channel is available.

**Maintainer contact (email):** `wilgat.wong@gmail.com`

- Source of contact: product **author-email** SSOT in [`LICENSE.md`](./LICENSE.md) (Copyright line).
- Prefer email for vulnerability details, reproduction steps, and impact.
- You should receive an acknowledgment when the report is received and actionable.
- Do not include exploit weaponization guides in public channels.

## Security Design Principles (CIAO)

This project follows **[CIAO](https://github.com/cloudgen/ciao)** / **CIAO-Lite** defensive design. Security-relevant intent:

| Letter | Principle | Security application |
|--------|-----------|----------------------|
| **C** | **Caution** | Assume missing tools and hostile/unexpected media inputs. Fail closed when FFmpeg is missing or both join paths fail. Do not claim success on failed encode. |
| **I** | **Intentional** | FFmpeg is invoked with argument lists (not shell-interpolated free-form filter graphs from untrusted remote input). Publish of intermediates uses `shutil.move`. Source media is never the final output path. |
| **A** | **Anti-fragile** | Multi-mount publish (USB vs system temp) is designed via staging + `shutil.move`. Unique temps avoid fixed cwd race names. |
| **O** | **Over-protect** | Protection Zones on staging/publish helpers; least privilege day-to-day (user-level CLI; no root elevation product surface). |

Full principles: [CIAO Defensive Programming](https://github.com/cloudgen/ciao) · agent contract: [CIAO-Lite](https://github.com/cloudgen/ciao-lite).

This section describes **design posture**. It is **not** a claim of third-party certification.

## Scope notes

- VideoEditor is a **local** interactive CLI. It does **not** implement online install channels or companion `.sha256` download integrity.
- Prefer keeping untrusted media and scripts offline unless you trust their origin.
- Related product docs: [`README.md`](./README.md), [`LICENSE.md`](./LICENSE.md).
