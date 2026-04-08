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
->conda create -n jubilee26 python=3.9
->conda activate jubilee26

->conda install conda-forge::jupyterlab
->jupyter lab


Utilisation de l’outil seringue

Une fois les étapes de première connexion réalisées, l’utilisation de l’outil seringue se fait par la compilation du serveur qui envoie les données du capteur et reçoit l’instruction pour le moteur qui actionne la seringue.

Dans un terminal:
-> ssh jubilee@10.0.9.55
il est demandé le mot de passe : projet_indus
-> python serveur_pi.py

Dans un terminal (au niveau de science jubilee):
->conda activate jubilee26
->jupyter lab

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



