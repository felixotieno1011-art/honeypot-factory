[![DevSecOps Deploy](https://github.com/felixotieno1011-art/honeypot-factory/actions/workflows/deploy-honeypot.yml/badge.svg)](https://github.com/felixotieno1011-art/honeypot-factory/actions/workflows/deploy-honeypot.yml)
[![Analyze Logs](https://github.com/felixotieno1011-art/honeypot-factory/actions/workflows/analyze-logs.yml/badge.svg)](https://github.com/felixotieno1011-art/honeypot-factory/actions/workflows/analyze-logs.yml)
![Security Gate](https://img.shields.io/badge/Security_Scan-Trivy_Enforced-blue)
![License](https://img.shields.io/badge/license-MIT-blue)


# DevSecOps Honeypot Factory

An Infrastructure-as-Code (IaC) deployment pipeline that spins up a Cowrie SSH honeypot, traps malicious login attempts, and analyzes the data.

## Architecture

[Termux / Phone] --(Push)--> [GitHub Actions]
                               |
      +------------------------+------------------------+
      |                                                 |
[Build Cowrie Image]                            [Run Ansible Playbook]
      |                                                 |
[Push to GHCR] --------------------------------> [Start Container]
                                                        |
                                               [Collect JSON Logs]
                                                        |
                                               [Python Analysis]
                                                        |
                                               [Upload Artifact]

## Project Structure

- ansible/ - IaC playbooks and inventory for deployment.
- honeypot/ - Dockerfile and Cowrie configuration.
- analysis/ - Python scripts to parse logs for passwords and geolocation.
- .github/workflows/ - CI/CD pipelines.
- scope.yaml - Legal network policy and authorization gate.
- dev.sh - Local Termux helper script.

## Security Controls

| Control | Implementation |
|---------|----------------|
| Legal Gate | scope.yaml defines passive listening mode and authorization. |
| Least Privilege | Docker container runs as the non-root cowrie user. |
| Secret Management | GHCR tokens handled via GitHub Actions secrets. |
| Log Isolation | Honeypot logs are mounted to a separate volume. |

## CI/CD Workflows

1. **Deploy Honeypot (deploy-honeypot.yml)**:
   - Triggers on push to main or manually.
   - Builds the Docker image and pushes it to GitHub Container Registry.
   - Installs Ansible and deploys the container locally on the runner.

2. **Analyze Logs (analyze-logs.yml)**:
   - Triggers every 6 hours or manually.
   - Runs the Python analysis scripts against the logs.
   - Uploads a report.txt artifact containing the top passwords and attacker countries.

## Local Development (Termux)

This project is built entirely on an Android device using Termux.

    # Run YAML and Python lints
    ./dev.sh lint

    # Test the analysis scripts with mock data
    ./dev.sh test

    # Trigger the GitHub Actions deployment
    ./dev.sh deploy

## Setup

1. Clone the repo: git clone https://github.com/felixotieno1011-art/honeypot-factory.git
2. Run ./dev.sh test to verify Python dependencies.
3. Push to main to trigger the CI/CD pipeline.

## Known Limitations & Production Roadmap

This project is a **pipeline demonstration**, not a production honeypot. Two limitations are acknowledged:

### 1. Ephemeral Deployment Target
The Ansible playbook currently targets `localhost` inside the GitHub Actions runner. The runner is destroyed at the end of the job, so the honeypot does not accumulate real telemetry across runs. The `data/mock_cowrie.json` file is synthetic demo data used to exercise the analysis scripts.

**Production fix:** Change `ansible/inventory/hosts.ini` to point at a persistent VM (VPS or on-prem host) reachable over SSH. Add `VM_HOST`, `VM_USER`, and `VM_SSH_KEY` as GitHub Secrets, and gate the `deploy-test` job on those secrets being present.

### 2. Trivy Runs in Report-Only Mode
The `security-scan` job uses `exit-code: '0'` so the pipeline can complete while demonstrating what Trivy finds. Real enforcement requires `exit-code: '1'` plus a `.trivyignore` file listing explicitly accepted CVEs with justification.

**Production fix:** Flip `exit-code` to `'1'`, add `.trivyignore`, and require PR review for any new entry.

### 3. Containment
The container runs with `capabilities: []`, `no-new-privileges:true`, and a 256M memory cap. A production deployment should additionally:
- Run on an isolated Docker network with no outbound egress by default
- Use a read-only root filesystem with a writable volume only for logs
- Forward logs to an external SIEM (Project 2) over a one-way channel
