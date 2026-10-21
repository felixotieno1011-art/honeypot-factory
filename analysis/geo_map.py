#!/usr/bin/env python3
import json
import sys
import urllib.request
import time
from collections import Counter

def get_country(ip):
    if ip.startswith(("127.", "10.", "192.168.", "172.")) or ip == "::1":
        return "Local/Private"
    try:
        url = f"http://ip-api.com/json/{ip}?fields=country"
        req = urllib.request.Request(url, headers={'User-Agent': 'HoneypotFactory/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get("country", "Unknown")
    except Exception:
        return "Lookup Failed"

def analyze_geo(filepath):
    ips = set()
    try:
        with open(filepath, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line)
                    if event.get('eventid') == 'cowrie.login.failed':
                        ips.add(event.get('src_ip'))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return

    print(f"\n## Top Attacker Countries")
    countries = Counter()

    for ip in ips:
        country = get_country(ip)
        countries[country] += 1
        if not ip.startswith(("127.", "10.", "192.168.", "172.")):
            time.sleep(1.5)

    for country, count in countries.most_common(10):
        print(f"- {country} ({count} attempts)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python geo_map.py <cowrie.json>")
        sys.exit(1)
    analyze_geo(sys.argv[1])
