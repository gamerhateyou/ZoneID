import requests
import getpass
import sys
import json

def get_zone_id(api_token, domain_name):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    url = f"https://api.cloudflare.com/client/v4/zones?name={domain_name}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Solleva un'eccezione per codici di stato HTTP non riusciti

        data = response.json()
        if data['success']:
            zones = data['result']
            if zones:
                return zones[0]['id']
            else:
                print(f"Nessuna zona trovata per il dominio {domain_name}")
                return None
        else:
            print("La richiesta non ha avuto successo. Dettagli dell'errore:")
            for error in data['errors']:
                print(f"- Codice: {error['code']}, Messaggio: {error['message']}")
            return None

    except requests.exceptions.HTTPError as errh:
        print(f"Errore HTTP: {errh}")
        print(f"Risposta del server: {response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Errore di connessione: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout della richiesta: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Errore durante la richiesta: {err}")
    except json.JSONDecodeError as jerr:
        print(f"Errore nel decodificare la risposta JSON: {jerr}")
        print(f"Risposta del server: {response.text}")
    return None

def main():
    print("Benvenuto nel tool per ottenere lo ZONE ID di Cloudflare!")
    
    while True:
        # Ottieni l'API token
        api_token = getpass.getpass("Inserisci il tuo Cloudflare API token (l'input sarà nascosto): ")
        
        # Ottieni il nome del dominio
        domain_name = input("Inserisci il nome del dominio (es. example.com): ")
        
        # Ottieni lo ZONE ID
        zone_id = get_zone_id(api_token, domain_name)
        
        if zone_id:
            print(f"\nLo ZONE ID per {domain_name} è: {zone_id}")
        else:
            print(f"\nNon è stato possibile ottenere lo ZONE ID per {domain_name}.")
        
        # Chiedi all'utente se vuole cercare un altro dominio
        retry = input("\nVuoi cercare un altro dominio? (s/n): ").lower()
        if retry != 's':
            break

    print("https://talk.homelabz.cc")

if __name__ == "__main__":
    main()