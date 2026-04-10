"""
API Matérielle - Contrôle Moteur et Capteur pour Jubilee
========================================================
Ce script transforme le Raspberry Pi en un serveur web local (API REST).
Il reçoit des requêtes HTTP depuis l'ordinateur maître (Jupyter) et les 
traduit en actions physiques :
- Pilotage d'un moteur DC via une carte L298N (PWM).
- Lecture d'un capteur analogique de niveau d'eau via une carte Arduino.

Auteur : Nicolas Durand (Projet étudiant - Sony CSL)
"""

from flask import Flask, request, jsonify
from gpiozero import Motor
import serial
import time

app = Flask(__name__)
print("Initialisation du matériel...")

# Configuration du Moteur
try:
    # Initialisation des broches GPIO pour la carte L298N
    moteur = Motor(forward=23, backward=24, enable=12)
    print("✅ Moteur prêt.")
except Exception as e:
    print(f"❌ Erreur Moteur : {e}")
    moteur = None

# Configuration de l'Arduino (Capteur)
try:
    # Connexion série via USB (Vérifiez bien le port ACM0 ou ACM1)
    arduino = serial.Serial('/dev/ttyACM1', 9600, timeout=1) 
    print("⏳ Attente de 2 secondes pour le réveil de l'Arduino...")
    time.sleep(2.0)
    arduino.reset_input_buffer() # Nettoie les données parasites de démarrage
    print("✅ Arduino connecté et réveillé sur /dev/ttyACM1.")
except Exception as e:
    print(f"❌ Erreur Arduino : {e}")
    arduino = None
   

@app.route('/moteur', methods=['POST'])
def controler_moteur():
    """
    Route : POST /moteur
    Pilote le moteur de la seringue (sens et vitesse).
    
    Attend un payload JSON au format :
    {
        "action": "forward" | "backward" | "stop",
        "speed": float (de 0.0 à 1.0)
    }

    Returns:
        JSON: Statut de la commande avec écho de l'action exécutée.
    """
    if moteur is None:
        return jsonify({"erreur": "Moteur non initialisé"}), 500
        
    data = request.json
    action = data.get('action')
    vitesse = data.get('speed', 1.0)
    
    if action == 'forward':
        moteur.forward(speed=vitesse)
    elif action == 'backward':
        moteur.backward(speed=vitesse)
    elif action == 'stop':
        moteur.stop()
        
    return jsonify({"status": "ok", "action": action, "speed": vitesse})


@app.route('/capteur', methods=['GET'])
def lire_capteur():
    """
    Route : GET /capteur
    Récupère la dernière valeur analogique lue par l'Arduino.
    
    La fonction vide le tampon série pour s'assurer de lire une valeur 
    récente (en temps réel) et convertit la valeur brute (0-1023) en Volts.

    Returns:
        JSON: Un dictionnaire contenant la 'tension' (V) et la valeur 'brute'.
    """
    if arduino is None:
        return jsonify({"erreur": "Arduino non connecté", "tension": 0.0}), 500
        
    try:
        # 1. On vide la "salle d'attente" USB pour éviter de lire de vieilles données
        arduino.reset_input_buffer()
        
        # 2. On laisse à l'Arduino le temps (50ms) d'envoyer sa nouvelle valeur
        time.sleep(0.05)
        
        # 3. Lecture et nettoyage de la ligne reçue
        ligne = arduino.readline().decode('utf-8', errors='ignore').rstrip()
        
        if ligne
