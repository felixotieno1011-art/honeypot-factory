#!/data/data/com.termux/files/usr/bin/bash

case "$1" in
  lint)
    echo "Linting YAML..."
    yamllint .github/workflows/ ansible/ scope.yaml || true
    echo "Checking Python..."
    python -m py_compile analysis/*.py && echo "Python OK"
    ;;
  test)
    echo "Running local analysis test..."
    python analysis/top_passwords.py data/mock_cowrie.json
    python analysis/geo_map.py data/mock_cowrie.json
    ;;
  deploy)
    echo "Triggering GitHub Actions deployment..."
    gh workflow run deploy-honeypot.yml
    sleep 3
    gh run watch
    ;;
  status)
    gh run list -L 5
    ;;
  *)
    echo "Usage: ./dev.sh {lint|test|deploy|status}"
    exit 1
    ;;
esac
