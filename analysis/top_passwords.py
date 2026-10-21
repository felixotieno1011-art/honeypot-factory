#!/usr/bin/env python3
import json
import sys
from collections import Counter

def analyze_logs(filepath):
    passwords = Counter()
    ips = set()
    commands = set()
    total_attempts = 0
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line)
                    src_ip = event.get('src_ip')
                    if not src_ip: continue
                    
                    if event.get('eventid') == 'cowrie.login.failed':
                        passwords[event.get('password')] += 1
                        ips.add(src_ip)
                        total_attempts += 1
                    elif event.get('eventid') == 'cowrie.command.input':
                        commands.add((src_ip, event.get('input')))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return

    print("# 🕵️ Honeypot Telemetry Report\n")
    print("## Executive Summary")
    print(f"- **Total Login Attempts:** {total_attempts}")
    print(f"- **Unique IP Addresses:** {len(ips)}")
    
    print("\n## Most Common Passwords")
    for i, (pwd, count) in enumerate(passwords.most_common(5), 1):
        print(f"{i}. `{pwd}` ({count} attempts)")

    print("\n## Malicious Commands Captured")
    if not commands:
        print("- *No commands captured yet.*")
    for ip, cmd in commands:
        print(f"- `{cmd}` (from {ip})")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python top_passwords.py <cowrie.json>")
        sys.exit(1)
    analyze_logs(sys.argv[1])
