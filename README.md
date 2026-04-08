# English readme below the French readme
# Projet industriel
Ce projet est un projet étudiant en lien avec l'entreprise Sony CSL

# Montage outil Seringue

L’outil Seringue a pour objectif de rendre la jubilee capable d'utiliser une seringue automatiquement, rendant notamment capable d'obtenir une quantité constante d’eau dans les puits d’une plaque multi-puits. Les problématiques de contamination des liquides ne sont pas prises en compte dans cette solution.

D’un point de vue mécanique nous avons une pièce support qui permet de fixer le moteur permettant un effort vertical sur la seringue. La deuxième pièce fixée à la première permet de fixer la partie extérieure de la seringue au support et de fixer le capteur de liquide.

Electronique : nous avons utilisé une rasbaerry pi connectée à un driver mjkdz pour alimenter et contrôler le moteur. Le capteur de liquide est directement connecté à une arduino (utilisé en tant que convertisseur analogique numérique).
Le MJDKZ motor driver module sert principalement à contrôler facilement la vitesse (permet d’augmenter ou diminuer la vitesse du moteur, d’avoir un contrôle souple et précis) et le sens d’un moteur DC (pont en h) à partir d’un microcontrôleur, tout en lui fournissant l’alimentation appropriée (externe à la arduino) et en le protégeant (des surtensions, pics de courant, parasites électriques).
Le capteur de niveau de liquide sert principalement à détecter la présence et mesurer la profondeur d'un fluide (jusqu'à 48 mm) à partir d'un microcontrôleur disposant d'une entrée analogique, tout en offrant une lecture continue (grâce à un circuit d'amplification par transistor générant une tension proportionnelle à l'immersion) utilisable pour concevoir facilement des systèmes d'alarme ou de surveillance de niveau.

Il est nécessaire d’acheter le moteur : 
https://www.amazon.fr/Actuator-electronic-controller-EKFBQBGW-5V-50mm-15N/dp/B0D9RP563V?th=1&psc=1

Il est nécessaire d’imprimer :  
1 : Piece_support_outil_seringue.stl  
2 : Piece_capteur_outil_seringue.stl  
3 : Piece_maintien_seringue.stl  
4 : Piece_moteur_outil_seringue.stl  

Les pièces sont également visible sur Printables :
https://www.printables.com/model/1675196-piece_support_outil_seringue

<img width="673" height="1214" alt="image" src="https://github.com/user-attachments/assets/8054e74d-f0c6-4af5-a28a-e74bae188ba3" />


# Test sur la seringue


L’objectif est ici de mesurer la différence de quantité d'eau déversée par l'outil seringue. Pour ce faire nous avons positionné la seringue à une hauteur qui restera constante durant toute la durée de l'expérience. Il nous a alors suffit d’utiliser la fonction remplissage de puits qui actionne le moteur jusqu’à ce que le sensor envoie une valeur supérieure à celle prédéfinie.  
<img width="368" height="449" alt="image" src="https://github.com/user-attachments/assets/5bbc1ea6-3e26-42da-b8cd-c36d9837d7f2" />


Il est important de noter que certains biais ont été remarqués comme une goutte d’eau qui serait restée au niveau de la seringue.  
<img width="346" height="438" alt="image" src="https://github.com/user-attachments/assets/6ed9ad59-a9c4-4399-a6fb-676b2aaf646a" />

<img width="926" height="682" alt="image" src="https://github.com/user-attachments/assets/37f06334-5e64-483d-9113-9adcc12cb953" />


# Code
Première utilisation de l’outil seringue 

-> allumer raspi + machine Jubilee  
-> connection au wifi : CSLToi  
-> dans la barre de recherche d’un navigateur : http://jubilee.local/ ou  http://10.0.9.6/  
-> Faire le homing pour vérifier que tout va bien (touche du tableau de bord “ Tout au Origines”)  

Cloner le repo https://github.com/corset-damien/science-jubilee  
 
Installer conda (plus propre avec le lien qu’avec une commande du terminal) :  
https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html  

-> se positionner dans le fichier science_jubilee  
-> conda create -n jubilee26 python=3.9  
-> conda activate jubilee26  

-> conda install conda-forge::jupyterlab  
-> jupyter lab  


Utilisation de l’outil seringue

Une fois les étapes de première connexion réalisées, l’utilisation de l’outil seringue se fait par la compilation du serveur qui envoie les données du capteur et reçoit l’instruction pour le moteur qui actionne la seringue.  

Dans un terminal:  
-> ssh jubilee@[adresse IP]
il est demandé le mot de passe : [mdp]  
-> python serveur_pi.py

Dans un terminal (au niveau de science jubilee):  
-> conda activate jubilee26  
-> jupyter lab  

Aller sur l’interface sur internet  
Se déplacer dans le répertoire science-jubilee/src/science_jubilee/a_netbookTest/test_ser.ipynb  


Modification d’un fichier de l’espace mémoire de la raspberry  

Dans le cas de modification du fichier il est conseillé d’utiliser vscode avec son extension   
remote - ssh la commande et le mots de passe pour se connecter reste identique. Il est alors facile d’ouvrir le dossier home/jubilee qui contient tous les codes qui sont dans l’espace mémoire de la raspberry et de les modifier.  


Utilisation du code test_ser.ipynb  

Seul deux fonctions sont réellement pour la manipulation de l’outil seringue  
-> tool1.remplir_seringue(temps_secondes=10.0)  
-> tool1.avancer_jusqu_au_seuil(seuil=1, timeout_sec=5)  
la première permet de remplir la seringue pendant le temps indiqué en paramètre (il y est fixé un temps de 4 secondes de vidage de la seringue au début de la fonction)  
la seconde permet de vider la seringue jusqu’à un certain niveau de seuil (valeur en volt facilement réglable avec le fichier “moniteur_capteur.py” il faut bien sur avoir lancer le serveur et être sur le wifi CSL toi)  


Erreur dans l’utilisation du code test_ser.ipynb  

En cas de difficulté dans les liens (les imports sont introuvables) faire : pip install -e dans un terminal au niveau de science jubilee  



# Industrial_project
This project is a student project in collaboration with the company Sony CSL

# Syringe tool assembly

The Syringe tool aims to make the Jubilee capable of using a syringe automatically, notably enabling it to obtain a constant amount of water in the wells of a multi-well plate. Liquid contamination issues are not taken into account in this solution.

From a mechanical point of view, we have a support part that allows the motor to be mounted, providing vertical force on the syringe. The second part, attached to the first one, allows the outer part of the syringe to be fixed to the support and to mount the liquid sensor.

Electronics: we used a Raspberry Pi connected to an mjkdz driver to power and control the motor. The liquid sensor is directly connected to an Arduino (used as an analog-to-digital converter).
The MJDKZ motor driver module is mainly used to easily control the speed (allows increasing or decreasing the motor speed, providing smooth and precise control) and the direction of a DC motor (H-bridge) from a microcontroller, while providing it with the appropriate power supply (external to the Arduino) and protecting it (from overvoltages, current spikes, and electrical noise).
The liquid level sensor is mainly used to detect the presence and measure the depth of a fluid (up to 48 mm) from a microcontroller with an analog input, while offering continuous reading (thanks to a transistor amplification circuit generating a voltage proportional to the immersion) usable to easily design alarm or level monitoring systems.

It is necessary to buy the motor: 
[https://www.amazon.fr/Actuator-electronic-controller-EKFBQBGW-5V-50mm-15N/dp/B0D9RP563V?th=1&psc=1](https://www.amazon.fr/Actuator-electronic-controller-EKFBQBGW-5V-50mm-15N/dp/B0D9RP563V?th=1&psc=1)

It is necessary to print:  
1 : Piece_support_outil_seringue.stl  
2 : Piece_capteur_outil_seringue.stl  
3 : Piece_maintien_seringue.stl  
4 : Piece_moteur_outil_seringue.stl  

The parts are also visible on Printables:
[https://www.printables.com/model/1675196-piece_support_outil_seringue](https://www.printables.com/model/1675196-piece_support_outil_seringue)

<img width="673" height="1214" alt="image" src="https://github.com/user-attachments/assets/8054e74d-f0c6-4af5-a28a-e74bae188ba3" />


# Syringe test


The objective here is to measure the difference in the amount of water dispensed by the syringe tool. To do this, we positioned the syringe at a height that will remain constant throughout the duration of the experiment. We then simply used the well-filling function, which activates the motor until the sensor sends a value higher than the predefined one.  
<img width="368" height="449" alt="image" src="https://github.com/user-attachments/assets/5bbc1ea6-3e26-42da-b8cd-c36d9837d7f2" />


It is important to note that some biases were noticed, such as a drop of water that might have stayed on the syringe tip.  
<img width="346" height="438" alt="image" src="https://github.com/user-attachments/assets/6ed9ad59-a9c4-4399-a6fb-676b2aaf646a" />

<img width="926" height="682" alt="image" src="https://github.com/user-attachments/assets/37f06334-5e64-483d-9113-9adcc12cb953" />




# Code
First use of the syringe tool 

-> turn on raspi + Jubilee machine
-> connect to wifi: CSLToi
-> in a browser's search bar: [http://jubilee.local/](http://jubilee.local/) or [http://10.0.9.6/](http://10.0.9.6/)
-> Home the machine to check that everything is fine (dashboard button "Home All" / "Tout aux origines")

Clone the repo [https://github.com/corset-damien/science-jubilee](https://github.com/corset-damien/science-jubilee)
 
Install conda (cleaner with the link than with a terminal command):
[https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html](https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html)

-> navigate into the sciencejubilee folder
->conda create -n jubilee26 python=3.9
->conda activate jubilee26

->conda install conda-forge::jupyterlab
->jupyter lab


Using the syringe tool

Once the initial connection steps are completed, the syringe tool is used by running the server which sends the sensor data and receives the instruction for the motor that actuates the syringe.

In a terminal:
-> ssh jubilee@10.0.9.55
the password is requested: projet_indus
-> python serveur_pi.py

In a terminal (at the science jubilee level):
->conda activate jubilee26
->jupyter lab

Go to the web interface
Navigate to the directory science-jubilee/src/science_jubilee/a_netbookTest/test_ser.ipynb 


Modifying a file in the Raspberry Pi's memory space

If modifying the file, it is recommended to use vscode with its remote - ssh extension. The command and password to connect remain the same. It is then easy to open the home/jubilee folder which contains all the codes that are in the Raspberry Pi's memory space and modify them.


Using the test_ser.ipynb code

Only two functions are actually for manipulating the syringe tool
-> tool1.remplir_seringue(temps_secondes=10.0)
-> tool1.avancer_jusqu_au_seuil(seuil=1, timeout_sec=5)
the first one allows filling the syringe for the time indicated in the parameter (a 4-second syringe emptying time is set at the beginning of the function)
the second one allows emptying the syringe up to a certain threshold level (voltage value easily adjustable with the "python moniteur_capteur.py" file, you must of course have launched the server and be on the CSLToi wifi)


Error when using the test_ser.ipynb code

In case of difficulty with the links (imports cannot be found) run: pip install -e in a terminal at the science jubilee level

