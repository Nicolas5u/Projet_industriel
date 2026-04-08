import requests
import time
import os

IP_RASPBERRY = "10.0.9.55"
PORT = "5001"
URL_CAPTEUR = f"http://{IP_RASPBERRY}:{PORT}/capteur"

def effacer_ecran():
    #Efface la console pour faire un affichage propre qui se met à jour
    os.system('cls' if os.name == 'nt' else 'clear')

print(" Démarrage du moniteur de capteur ")
time.sleep(1)

try:
    while True:
        try:
            # On interroge le Raspberry Pi
            req = requests.get(URL_CAPTEUR, timeout=3, proxies={"http": None, "https": None})
            reponse = req.json()
            
            tension = reponse.get("tension", 0.0)
            brute = reponse.get("brute", 0)
            erreur = reponse.get("erreur", "")

            # Création d'une jauge visuelle (0 à 5V = 20 blocs)
            # On limite la tension entre 0 et 5 pour l'affichage visuel
            tension_affichee = max(0, min(tension, 5.0)) 
            nb_blocs = int((tension_affichee / 5.0) * 20)
            barre = "█" * nb_blocs + "-" * (20 - nb_blocs)

            effacer_ecran()
            print("================================")
            print(" MONITEUR DU CAPTEUR DE LIQUIDE")
            print("================================\n")
            print(f"Connecté à : {URL_CAPTEUR}\n")
            
            if erreur:
                print(f"Avertissement du Pi : {erreur}")
            else:
                print(f"Tension lue : {tension:.2f} V")
                print(f"Valeur brute: {brute} / 1023\n")
                print(f"Jauge visuelle : [{barre}]")
            
            print("Ctrl+C pour quitter")

        except requests.exceptions.RequestException:
            effacer_ecran()
            print("================================")
            print(" MONITEUR DU CAPTEUR DE LIQUIDE ")
            print("=========================================\n")
            print(f"ERREUR : Impossible de joindre le Pi sur {IP_RASPBERRY}")
            print("-> Vérifiez que 'serveur_pi.py' tourne bien sur la Raspberry.")
            print("-> Vérifiez que vous êtes sur le même Wi-Fi.")
            print("\n(Nouvelle tentative dans 2 secondes...)")
            time.sleep(1.8) # On attend un peu plus longtemps si le réseau est coupé

        # On attend 0.2s avant de rafraîchir l'écran (5 images par seconde)
        time.sleep(0.2)

except KeyboardInterrupt:
    effacer_ecran()
    print("Moniteur fermé")

