import requests
import getpass
import json

def get_zone_id(api_token, domain_name):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/zones?name={domain_name}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['success'] and data['result']:
            return data['result'][0]['id']
        else:
            print(f"Nessuna zona trovata per il dominio {domain_name}")
            return None
    except requests.exceptions.RequestException as err:
        print(f"Errore durante la richiesta: {err}")
        return None

def get_dns_record_id(api_token, zone_id, record_name, record_type):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type={record_type}&name={record_name}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['success'] and data['result']:
            return data['result'][0]['id']
        else:
            print(f"Nessun record DNS trovato per {record_name} di tipo {record_type}")
            return None
    except requests.exceptions.RequestException as err:
        print(f"Errore durante la richiesta: {err}")
        return None

def main():
    print("Benvenuto nel tool per ottenere l'ID del record DNS di Cloudflare!")
    
    while True:
        api_token = getpass.getpass("Inserisci il tuo Cloudflare API token (l'input sarà nascosto): ")
        domain_name = input("Inserisci il nome del dominio (es. example.com): ")
        
        zone_id = get_zone_id(api_token, domain_name)
        if not zone_id:
            print(f"Impossibile trovare la zona per {domain_name}")
            continue
        
        record_name = input("Inserisci il nome del record DNS (es. www.example.com): ")
        record_type = input("Inserisci il tipo di record DNS (es. A, CNAME, MX): ").upper()
        
        record_id = get_dns_record_id(api_token, zone_id, record_name, record_type)
        if record_id:
            print(f"\nL'ID del record DNS {record_name} di tipo {record_type} è: {record_id}")
        else:
            print(f"\nNon è stato possibile ottenere l'ID del record DNS per {record_name}")
        
        retry = input("\nVuoi cercare un altro record DNS? (s/n): ").lower()
        if retry != 's':
            break

    print("https://talk.homelabz.cc")

if __name__ == "__main__":
    main()