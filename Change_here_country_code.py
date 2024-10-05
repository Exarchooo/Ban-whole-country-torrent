import os
import urllib.request
import json
import ipaddress
from pathlib import Path

def fetch_ip_ranges_ripe(country_code):
    url = f"https://stat.ripe.net/data/country-resource-list/data.json?resource={country_code}"
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        ipv4_prefixes = data['data']['resources']['ipv4']
        return ipv4_prefixes
    except Exception as e:
        print(f"Error - RIPEstat API: {e}")
        return []

def fetch_ip_ranges_ipdeny(country_code):
    url = f"https://www.ipdeny.com/ipblocks/data/countries/{country_code.lower()}.zone"
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        ipv4_prefixes = data.strip().split('\n')
        return ipv4_prefixes
    except Exception as e:
        print(f"Error - ipdeny.com: {e}")
        return []

def load_existing_ips(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read().splitlines()
        return set(data)

def save_ips(file_path, ip_list):
    with open(file_path, 'w') as f:
        for ip in sorted(ip_list, key=lambda x: ipaddress.IPv4Address(x)):
            f.write(f"{ip}\n")

def expand_ip_ranges(ip_ranges):
    ips = set()
    for ip_range in ip_ranges:
        try:
            if '/' in ip_range:
                network = ipaddress.IPv4Network(ip_range, strict=False)
                for ip in network.hosts():
                    ips.add(str(ip))
            elif '-' in ip_range:
                start_ip_str, end_ip_str = ip_range.split('-')
                start_ip = int(ipaddress.IPv4Address(start_ip_str.strip()))
                end_ip = int(ipaddress.IPv4Address(end_ip_str.strip()))
                for ip_int in range(start_ip, end_ip + 1):
                    ips.add(str(ipaddress.IPv4Address(ip_int)))
            else:
                ips.add(ip_range.strip())
        except Exception as e:
            print(f"Fetching failed {ip_range}: {e}")
    return ips

def main():
    country_code = 'IL'  # Example, israel. Choose country ID from file country_list.txt. If you want ban more than one country then you must manually cut IP's from first file and paste to other .dat file and repeat process.

    ripe_ranges = fetch_ip_ranges_ripe(country_code)
    ipdeny_ranges = fetch_ip_ranges_ipdeny(country_code)

    all_ranges = set(ripe_ranges + ipdeny_ranges)

    all_ips = expand_ip_ranges(all_ranges)
    print(f"{len(all_ips)} IP's fetched")

    # Path to C/user/user_name
    home_dir = Path.home()
    file_path = home_dir / 'ips_list.dat'

    save_ips(file_path, all_ips)
    print(f"The list of IP addresses has been saved to {file_path}")

if __name__ == "__main__":
    main()
