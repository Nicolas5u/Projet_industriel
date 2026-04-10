"""
Moniteur du Capteur de Liquide (Outil Client)
=============================================
Ce script est un outil d'affichage en temps réel (CLI) pour surveiller 
la valeur du capteur de liquide de la Jubilee. Il interroge régulièrement 
le serveur Flask du Raspberry Pi et génère une jauge visuelle dans le terminal.

Auteur : Nicolas Durand (Projet étudiant - Sony CSL)
"""

import requests
import time
import os

# CONFIGURATION RÉSEAU

IP_RASPBERRY = "10.0.9.55"
PORT = "5001"
URL_CAPTEUR = f"http://{IP_RASPBERRY}:{PORT}/capteur"


def effacer_ecran():
    """
    Efface le contenu de la console (terminal) pour simuler une interface dynamique.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


print(" Démarrage du moniteur de capteur...")
time.sleep(1)

try:
    # Boucle principale (tourne à l'infini jusqu'à ce qu'on fasse Ctrl+C)
    while True:
        try:
            # 1. On interroge l'API du Raspberry Pi pour avoir l'état du capteur
            # Les proxies sont désactivés pour forcer la requête sur le réseau local
            req = requests.get(URL_CAPTEUR, timeout=3, proxies={"http": None, "https": None})
            reponse = req.json()
            
            # 2. Extraction des données reçues (0.0 par défaut si la clé n'existe pas)
            tension = reponse.get("tension", 0.0)
            brute = reponse.get("brute", 0)
            erreur = reponse.get("erreur", "")

            # 3. Création d'une jauge visuelle (0 à 5V = 20 blocs)
            # On s'assure que la tension ne dépasse pas 5.0 ou ne soit pas sous 0.0
            tension_affichee = max(0, min(tension, 5.0)) 
            # Calcul du nombre de blocs pleins (règle de trois)
            nb_blocs = int((tension_affichee / 5.0) * 20)
            # Création de la chaîne de caractères (ex: ████████------------)
            barre = "█" * nb_blocs + "-" * (20 - nb_blocs)

            # 4. Affichage de l'interface dans le terminal
            effacer_ecran()
            print("================================")
            print(" MONITEUR DU CAPTEUR DE LIQUIDE")
            print("================================\n")
            print(f" Connecté à : {URL_CAPTEUR}\n")
            
            # Affichage de l'erreur si l'Arduino a eu un problème de lecture
            if erreur:
                print(f" Avertissement du Pi : {erreur}")
            else:
                print(f" Tension lue : {tension:.2f} V")
                print(f" Valeur brute: {brute} / 1023\n")
                print(f"Jauge visuelle : [{barre}]")
            
            print("\n(Appuyez sur Ctrl+C pour quitter)")

        except requests.exceptions.RequestException:
            # Gestion du cas où le Raspberry Pi est éteint, déconnecté du Wi-Fi, 
            # ou si le serveur Flask n'est pas lancé.
            effacer_ecran()
            print("================================")
            print(" MONITEUR DU CAPTEUR DE LIQUIDE")
            print("================================\n")
            print(f" ERREUR : Impossible de joindre le Pi sur {IP_RASPBERRY}")
            print("-> Vérifiez que 'serveur_pi.py' tourne bien sur le Raspberry.")
            print("-> Vérifiez que vous êtes sur le même Wi-Fi.")
            print("\n(Nouvelle tentative dans 2 secondes...)")
            
            # On attend un peu plus longtemps si le réseau est coupé pour ne pas spammer
            time.sleep(1.8) 

        # On attend 0.2s avant de rafraîchir l'écran (environ 5 images par seconde)
        time.sleep(0.2)

except KeyboardInterrupt:
    # Se déclenche proprement si l'utilisateur fait un Ctrl+C dans le terminal
    effacer_ecran()
    print("⏹️ Moniteur fermé. Bonne continuation ! (Nicolas Durand - Sony CSL)")
