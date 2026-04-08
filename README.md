# Projet_industriel
Ce projet est un projet étudiant en lien avec l'entreprise Sony CSL

Première utilisation de l’outil seringue 

-> allumer raspi + machine Jubilee
-> connection au wifi : CSLToi
-> dans la barre de recherche d’un navigateur : http://jubilee.local/ ou  http://10.0.9.6/
-> Faire le homing pour vérifier que tout va bien (touche du tableau de bord “ Tout au Origines”)

Cloner le repo https://github.com/corset-damien/science-jubilee
 
Installer conda (plus propre avec le liens qu’avec une commande du terminal) :
https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html

-> se positionner dans le fichier sciencejubilee
->conda create -n jubilee26 python=3.9
->conda activate jubilee26

->conda install conda-forge::jupyterlab
->jupyter lab


Utilisation de l’outil seringue

Une fois les étapes de première connexion réalisées, l’utilisation de l’outil seringue se fait par la compilation du serveur qui envoie les données capteur et reçoit l’instruction pour le moteur qui actionne la seringue.

Dans un terminal:
-> ssh jubilee@10.0.9.55
il est demandé le mots de passe : projet_indus
-> python serveur_pi.py

Dans un terminal (au niveau de science jubilee):
->conda activate jubilee26
->jupyter lab

Aller sur l’interface sur internet
Se déplacer dans le répertoire science-jubilee/src/science_jubilee/a_netbookTest/test_ser.ipynb 


Modification d’un fichier de l’espace mémoir de la raspberry

Dans le cas de modification du fichier il est conseillé d’utiliser vscode avec son extension 
remote - ssh la commande et le mots de passe pour se connecter reste identique. Il est alors facile d’ouvrir le dossier home/jubilee qui contient tous les codes qui sont dans l’espace mémoire de la raspberry et de les modifier.


Utilisation du code test_ser.ipynb

Seul deux fonctions sont réellement pour la manipulation de l’outil seringue
-> tool1.remplir_seringue(temps_secondes=10.0)
-> tool1.avancer_jusqu_au_seuil(seuil=1, timeout_sec=5)
la première permet de remplir la seringue pendant le temps indiqué en paramètre (il est fixé un temps de 4 secondes de vidage de la seringue au début de la fonction)
la seconde permet de vider la seringue jusqu’à un certain niveau de seuil (valeur en volt facilement réglable avec le fichier “python moniteur_capteur.py” il faut bien sur avoir lancer le serveur et être sur le wifi CSL toi)


Erreur dans l’utilisation du code test_ser.ipynb

En cas de difficulté dans les liens (les imports sont introuvables) faire : pip install -e dans un terminal au niveau de science jubilee



