#!/usr/bin/env python3
import json
import sys
from collections import Counter

def analyze_logs(filepath):
    passwords = Counter()
    ips = Counter()
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line)
                    if event.get('eventid') == 'cowrie.login.failed':
                        passwords[event.get('password')] += 1
                        ips[event.get('src_ip')] += 1
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return

    print("=== Top 10 Passwords ===")
    for pwd, count in passwords.most_common(10):
        print(f"{count:4d} | {pwd}")

    print("\n=== Top 5 Attacker IPs ===")
    for ip, count in ips.most_common(5):
        print(f"{count:4d} | {ip}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python top_passwords.py <cowrie.json>")
        sys.exit(1)
    analyze_logs(sys.argv[1])
