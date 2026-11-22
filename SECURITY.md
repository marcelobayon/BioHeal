# Security Policy

BioHeal is an experimental recovery framework. Because its purpose is to take
automated corrective action, its safety boundaries are part of its design, not
an afterthought.

## Design safeguards (charter §7)

BioHeal must never become an uncontrolled agent with production write access.
The core is built to respect:

- Deny-by-default permissions and explicit action allowlists.
- No arbitrary package installation; no arbitrary shell commands from model output.
- No direct self-overwriting of production source files.
- Pinned, verified dependencies; sandboxed candidate execution.
- Secrets isolation and redaction — events and errors carry identifiers and safe
  diagnostics only, never secrets or stack traces.
- Human approval for high-impact actions; rollback and a kill switch.
- Verification before promotion; durable audit logs.
- A clear separation between *suggestions* and *executed actions*.

A language model may propose a diagnosis or candidate repair, but deterministic
policy enforcement and verification decide whether an action is allowed.

## Reporting a vulnerability

If you discover a security issue, please open a private report to the repository
owner rather than a public issue. Include reproduction steps and the affected
version. We aim to acknowledge reports promptly and will credit reporters who
wish to be named.

## Scope and expectations

This is alpha research software with no uptime or safety guarantees. Do not
deploy it against production systems without your own review, sandboxing, and
verification gates.
