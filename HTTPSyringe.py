import json
import logging
import os
import time
from itertools import dropwhile, takewhile
from typing import Iterator, List, Tuple, Union

import numpy as np
import requests

from science_jubilee.labware.Labware import Labware, Location, Well
from science_jubilee.tools.Tool import (
    Tool,
    ToolConfigurationError,
    ToolStateError,
    requires_active_tool,
)


class HTTPSyringe(Tool):
    def __init__(self, index, name, url, ip_raspberry="10.0.9.55"):
        """
        HTTP Syringe est un client pur : parle à Jubilee (url) et à notre serveur Pi.
        """
        self.name = name
        self.index = index
        self.url = url
        # ⚠ Port 5001 pour éviter le conflit avec OctoPrint
        self.url_materiel = f"http://{ip_raspberry}:5001"  

        # --- Initialisation HTTP standard de Jubilee ---
        config_r = requests.post(url + "/get_config", json={"name": name})
        config = config_r.json()
        super().__init__(index, **config, url=url)

        # Vérifie le serveur Pi
        self._init_gpio()

        # Status initial
        status_r = requests.post(url + "/get_status", json={"name": name})
        status = status_r.json()
        self.syringe_loaded = status.get("syringe_loaded", False)
        self.remaining_volume = status.get("remaining_volume", 0.0)

    def _init_gpio(self):
        """
        Initialise la connexion réseau avec le serveur matériel du Raspberry Pi.
        
        Cette fonction effectue un "ping" (requête GET) vers le Raspberry Pi pour 
        vérifier s'il est allumé et prêt à recevoir des commandes. Elle met à jour 
        l'attribut `self.gpio_disponible` en conséquence.

        Auteur : Nicolas Durand (Projet étudiant - Sony CSL)
        """
        if getattr(self, "gpio_disponible", False):
            return

        try:
            requests.get(f"{self.url_materiel}/capteur", timeout=2)
            self.gpio_disponible = True
            print(f"[{self.name}] ✅ Connecté au serveur matériel du Raspberry Pi.")
        except requests.exceptions.RequestException:
            self.gpio_disponible = False
            print(f"[{self.name}] ❌ ERREUR : Impossible de joindre le Pi sur {self.url_materiel}.")

    def lire_capteur(self):
        """
        Interroge le Raspberry Pi pour obtenir la valeur immédiate du capteur de liquide.
        
        Idéal pour le monitoring en direct ou pour tester le capteur sans activer le moteur.

        Returns:
            tuple: (tension en Volts, valeur_brute de 0 à 1023). 
                   Retourne (None, None) en cas d'échec de connexion.

        Auteur : Nicolas Durand (Projet étudiant - Sony CSL)
        """
        self._init_gpio()
        if not getattr(self, "gpio_disponible", False):
            return None, None
            
        try:
            req = requests.get(f"{self.url_materiel}/capteur", timeout=2)
            reponse = req.json()
            tension = reponse.get("tension", 0.0)
            brute = reponse.get("brute", 0)
            return tension, brute
        except Exception:
            return None, None

    @requires_active_tool
    def avancer_jusqu_au_seuil(self, seuil: float = 1.0, timeout_sec: int = 5):
        """
        Descend l'outil vers le réservoir jusqu'à la détection du liquide.
        
        Active le moteur en marche avant et interroge en boucle le capteur via le Pi.
        Dès que la tension lue est supérieure ou égale au seuil, le moteur s'arrête.
        Intègre une sécurité (timeout) pour éviter le crash physique de l'outil si 
        le capteur est défaillant ou le réservoir vide.

        Args:
            seuil (float): La tension cible (en Volts) confirmant la présence de liquide.
            timeout_sec (int): Temps maximum (en secondes) avant l'arrêt d'urgence.

        Raises:
            ToolStateError: Si le serveur Raspberry Pi est injoignable avant le mouvement.

        Auteur : Nicolas Durand (Projet étudiant - Sony CSL)
        """
        self._init_gpio()
        if not getattr(self, "gpio_disponible", False):
            raise ToolStateError("Le serveur Pi n'est pas joignable.")

        print(f"[{self.name}] Ordre au Pi : Moteur forward (Attente seuil >= {seuil}V)")
        requests.post(f"{self.url_materiel}/moteur", json={"action": "forward", "speed": 1.0})
        
        start_time = time.time()
        try:
            while True:
                try:
                    req = requests.get(f"{self.url_materiel}/capteur", timeout=1)
                    tension_actuelle = req.json().get("tension", 0.0)
                except Exception:
                    tension_actuelle = 0.0 

                if tension_actuelle >= seuil:
                    print(f"[{self.name}] Seuil atteint ({tension_actuelle:.2f}V).")
                    break
                    
                if (time.time() - start_time) > timeout_sec:
                    print(f"[{self.name}] Timeout atteint ({timeout_sec}s).")
                    break
                    
                time.sleep(0.1)
                
        finally:
            # Bloc "finally" garantissant l'arrêt du moteur même en cas de crash (Ctrl+C)
            requests.post(f"{self.url_materiel}/moteur", json={"action": "stop"})
            print(f"[{self.name}] Moteur arrêté.")

    @requires_active_tool
    def remplir_seringue(self, temps_secondes: float):
        """
        Exécute une séquence de purge et de remplissage automatisée de la seringue.
        
        1. Marche avant (4s) : Vide l'air ou le liquide résiduel dans le réservoir source.
        2. Marche arrière (variable) : Aspire le nouveau liquide.

        Args:
            temps_secondes (float): Durée d'activation du moteur en marche arrière pour l'aspiration.

        Auteur : Nicolas Durand (Projet étudiant - Sony CSL)
        """
        self._init_gpio()
        if not getattr(self, "gpio_disponible", False):
            raise ToolStateError("Le serveur Pi n'est pas joignable.")

        temps_vide = 4.0
        print(f"[{self.name}] Vidage en cours pour {temps_vide} sec...")
        requests.post(f"{self.url_materiel}/moteur", json={"action": "forward", "speed": 1.0})
        time.sleep(temps_vide)

        print(f"[{self.name}] Remplissage en cours pour {temps_secondes} sec...")
        requests.post(f"{self.url_materiel}/moteur", json={"action": "backward", "speed": 1.0})
        time.sleep(temps_secondes)

        requests.post(f"{self.url_materiel}/moteur", json={"action": "stop"})
        print(f"[{self.name}] Remplissage terminé.")

        if hasattr(self, 'capacity'):
            self.remaining_volume = self.capacity

    def cleanup_gpio(self):
        """
        Sécurité logicielle de fin d'utilisation.
        S'assure que le moteur ne reste pas bloqué en position de marche si le script 
        principal s'arrête brutalement. À appeler à la toute fin des expériences.

        Auteur : Nicolas Durand (Projet étudiant - Sony CSL)
        """
        if getattr(self, "gpio_disponible", False):
            try:
                requests.post(f"{self.url_materiel}/moteur", json={"action": "stop"})
            except:
                pass

    @classmethod
    def from_config(cls, index, fp):
        with open(fp) as f:
            kwargs = json.load(f)
        return cls(index, **kwargs)

    def status(self):
        r = requests.post(self.url + "/get_status", json={"name": self.name})
        status = r.json()
        self.syringe_loaded = status["syringe_loaded"]
        self.remaining_volume = status["remaining_volume"]
        return status

    def load_syringe(self, volume, pulsewidth):
        requests.post(self.url + "/load_syringe", json={"volume": volume, "pulsewidth": pulsewidth, "name": self.name})
        self.status()

    @requires_active_tool
    def _aspirate(self, vol, s):
        r = requests.post(self.url + "/aspirate", json={"volume": vol, "name": self.name, "speed": s})
        self.remaining_volume = requests.post(self.url + "/get_status", json={"name": self.name}).json()["remaining_volume"]

    @requires_active_tool
    def _dispense(self, vol, s):
        r = requests.post(self.url + "/dispense", json={"volume": vol, "name": self.name, "speed": s})
        self.remaining_volume = requests.post(self.url + "/get_status", json={"name": self.name}).json()["remaining_volume"]

    @requires_active_tool
    def dispense(self, vol: float, location: Union[Well, Tuple, Location], s: int = 100):
        x, y, z = Labware._getxyz(location)
        if isinstance(location, Well):
            self.current_well = location
            if z == location.z:
                z += 10
        elif isinstance(location, Location):
            self.current_well = location._labware
        self._machine.safe_z_movement()
        self._machine.move_to(x=x, y=y, wait=True)
        self._machine.move_to(z=z, wait=True)
        self._dispense(vol, s)

    @requires_active_tool
    def aspirate(self, vol: float, location: Union[Well, Tuple, Location], s: int = 100):
        x, y, z = Labware._getxyz(location)
        if isinstance(location, Well):
            self.current_well = location
        elif isinstance(location, Location):
            self.current_well = location._labware
        self._machine.safe_z_movement()
        self._machine.move_to(x=x, y=y, wait=True)
        self._machine.move_to(z=z, wait=True)
        self._aspirate(vol, s)

    @requires_active_tool
    def mix(self, vol: float, n_mix: int, location: Union[Well, Tuple, Location], t_hold: int = 1, s_aspirate: int = 100, s_dispense: int = 100):
        x, y, z = Labware._getxyz(location)
        self._machine.safe_z_movement()
        self._machine.move_to(x=x, y=y, wait=True)
        self._aspirate(500, s_aspirate)
        self._machine.move_to(z=z, wait=True)
        for _ in range(n_mix):
            self._aspirate(vol, s_aspirate)
            time.sleep(t_hold)
            self._dispense(vol, s_dispense)
            time.sleep(t_hold)
        self._dispense(500, s_dispense)

    def set_pulsewidth(self, pulsewidth: int, s: int = 100):
        requests.post(self.url + "/set_pulsewidth", json={"pulsewidth": pulsewidth, "name": self.name, "speed": s})
        self.status()
