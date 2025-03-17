"""

"""
import json
import requests

URL = "url"
IPV6 = "ipv6"
COLON = ":"
LINE_BREAK = "\n"
CONFIG_FILE = "config.json"
CF_API_V4 = "https://api.cloudflare.com/client/v4"

def get_ip_list(urls_dict: dict):
    """
    Get ip list from list of dictionaries of urls
    """
    ip_list = []
    for url_dict in urls_dict:
        include_ipv6 = url_dict[IPV6]
        url = url_dict[URL]
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            preliminary = response.text.split(LINE_BREAK)
            ip_list += list(filter(lambda ip: COLON not in ip or include_ipv6,
                                   preliminary))
        except requests.exceptions.RequestException as e:
            print(f"Error getting ip list from {url}: {e}")
    return ip_list

def get_config(name: str):
    """
    Get configuration from config file
    """
    try:
        with open(name, "r", encoding="utf-8") as file:
            config = json.load(file)
    except FileNotFoundError:
        print(f"Error opening {name}: file not found")
        return None
    except json.JSONDecodeError:
        print(f"Error reading {name}: not a valid json file")
        return None
    return config

def get_virtual_networks(config: dict):
    """
    Get extent virtual networks on Cloudflare
    """
    account_id = config["account_id"]
    token = config["token"]
    extent_virtual_networks = []
    headers = {
        "Authorization": f"Bearer {token}"
    }
    path = f"/accounts/{account_id}/teamnet/virtual_networks"
    try:
        response = requests.get(f"{CF_API_V4}{path}",
                                headers=headers,
                                timeout=5)
        response.raise_for_status()
        extent_virtual_networks = response.json()["result"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting extent virtual networks: {e}")
    network_names = []
    for network in extent_virtual_networks:
        network_names.append(network["name"])
    return network_names, extent_virtual_networks

def get_id_by_name(network_name: str, virtual_networks: list[dict]):
    """
    Get virtual network id by name
    """
    for network in virtual_networks:
        if network["name"] == network_name:
            return network["id"]
    return None

def delete_network(config: dict, network_name: str, virtual_networks: list[dict]):
    """
    Delete virtual network by name
    """
    account_id = config["account_id"]
    token = config["token"]
    network_id = get_id_by_name(network_name, virtual_networks)
    headers = {
        "Authorization": f"Bearer {token}",
    }
    path = f"/accounts/{account_id}/teamnet/virtual_networks/{network_id}"
    try:
        response = requests.delete(f"{CF_API_V4}{path}",
                                headers=headers,
                                timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error deleting network {network_name}: {e}")

def create_network(config: dict, network_name: str, comment: str):
    """
    Create virtual network by name
    """
    account_id = config["account_id"]
    token = config["token"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    data = {
        "name": network_name,
        "comment": comment,
        "is_default": False
    },
    path = f"/accounts/{account_id}/teamnet/virtual_networks"
    try:
        response = requests.post(f"{CF_API_V4}{path}",
                                headers=headers,
                                data=json.dumps(data),
                                timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error creating network {network_name}: {e}")