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
