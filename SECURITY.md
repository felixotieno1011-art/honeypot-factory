# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

This project uses automated Trivy scanning in CI to enforce a security gate. 
If you discover a vulnerability in the Cowrie base image or the Ansible deployment, 
please open an issue with the label `security`.

Please **do not** publicly disclose the vulnerability until it has been reviewed 
and a patch has been released.

### Vulnerability Exceptions
Any temporarily accepted CVEs are documented in the [`.trivyignore`](.trivyignore) file 
with a justification and review date. New exceptions require PR review.
