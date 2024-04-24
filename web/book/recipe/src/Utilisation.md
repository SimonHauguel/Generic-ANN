# Utilisation

## Initialisation

Une fois les sources installées. Vous devrez lancer le webserver en éxecutant la ligne de commande suivante :
`> path\to\the\root\folder python3.11 .\web\python\server.py`. Note, inversez les `\` par des `/` sur Linux.
Rendez-vous par la suite, sur votre [localhost](http://127.0.0.1:5000), l'application se lance par défaut sur le port `5000`. Vous devriez voir apparaitre un `Formulaire d'envoi de fichier`. Cette interface vous permet de 
1. Récuperer les sources VHDL nécessaires.
2. Générer le code VHDL en fonction de vos matrices de poids, de biais, et de vos entrées. 

Nous y reviendrons plus en détails par la suite.

La prochaine étape sera de créer un nouveau projet sur Quartus. Nous avons, dans notre cas visé la carte de développement `DE0-CV` de Intel. Il vous est tout a fait possible de choisir un autre FPGA, notez simplement que le nom des ports peuvent ne pas correspondre, et qu'il vous faudra fournir une clock de 50Mhz. N'oubliez pas d'importer le pin planner, si nécessaire, pour votre carte.

## Importez vos matrices de coefficients

Le fichier à envoyer dans le formulaire est le fichier contenant toutes vos matrices de poids, de biais ainsi que vos entrées. Le fichier est formatté de cette manière : `[ [entrées], [matrice layer 1 -> 2], [vecteur de biais 1er layer], [matrice 2 -> 3], [vecteur de biais 2nd layer], ...]`. Vous trouverez un fichier fonctionel sous le nom de `wmatrix` à la racine des sources. Note, pour notre implémentation, nous travaillons sur des entiers `8bits` non signés.