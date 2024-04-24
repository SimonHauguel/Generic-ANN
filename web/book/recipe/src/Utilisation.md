# Utilisation

## Vue d'ensemble

Notre solution n'est pas un projet Quartus, mais une application web écrite en Python, qui va venir générer le `.vhd` en fonction de vos matrices de poids, de biais et de vos entrées. Le code VHDL généré travail sur des entiers 8bits non signés. Il vous sera nécessaire de recompiler votre projet si votre réseau de neuronnes vient à être modifié. 

## Initialisation

Une fois les sources installées. Vous devrez lancer le webserver en éxecutant la ligne de commande suivante :
`> path\to\the\root\folder python3.11 .\web\python\server.py`. Note, inversez les `\` par des `/` sur Linux.
Rendez-vous par la suite, sur votre [localhost](http://127.0.0.1:5000), l'application se lance par défaut sur le port `5000`. Vous devriez voir apparaitre un `Formulaire d'envoi de fichier`. Cette interface vous permet de 
1. Récuperer les sources VHDL nécessaires.
2. Générer le code VHDL en fonction de vos matrices de poids, de biais, et de vos entrées. 

Nous y reviendrons plus en détails par la suite.

La prochaine étape sera de créer un nouveau projet sur Quartus. Nous avons, dans notre cas visé la carte de développement `DE0-CV` de Intel. Il vous est tout a fait possible de choisir un autre FPGA, notez simplement que le nom des ports peuvent ne pas correspondre, et qu'il vous faudra fournir une clock de `50Mhz`. N'oubliez pas d'importer le pin planner, si nécessaire, pour votre carte.

## Importez vos matrices de coefficients

Le fichier à envoyer dans le formulaire est le fichier contenant toutes vos matrices de poids, de biais ainsi que vos entrées. Le fichier est formatté de cette manière : `[ [entrées], [matrice layer 1 -> 2], [vecteur de biais 1er layer], [matrice 2 -> 3], [vecteur de biais 2nd layer], ...]`. Vous trouverez un fichier fonctionel sous le nom de `wmatrix` à la racine des sources. Note, pour notre implémentation, nous travaillons sur des entiers `8bits` non signés.

Une fois le fichier téléchargé sur le serveur, vous pouvez spécifier le chemin d'accés de votre fichier `.vhd` top-level (celui qui sert de point d'entrée) de votre projet Quartus. Si vous le faites, l'application ira directement écrire le fichier généré dans le fichier cible **(attention, il effacera tout pour réecrire par dessus)**.

## Récuperer les dépendances VHDL

Deux fichiers sont nécessaires au bon fonctionnement du fichier généré. Le premier est l'implémentation des neurones. Le second est l'implémentation du protocol `UART`. Sur le site, vous pouvez les obtenir en cliquant sur, respectivement, `CODE NEURONE` et `CODE UART`. L'application ne peut pas vous les ajouter directement dans votre Quartus. Il vous est donc nécessaire de le faire à la main (copier-coller, changer de nom de l'architecture si besoin, et les ajouter au projet).

## Récuperer les résultats

Une fois vos matrices envoyées au serveur, les dépendances récuperées, et le code généré. Vous pouvez compiler votre projet. Si une erreur de taille de `STD_LOGIC_VECTOR` apparait, verifiez bien la consistance de votre fichier contenant les matrices de poids. Si une erreur de nom inconnu, assurez-vous bien que vous avez importez le code des neurones et de l'UART.

Vous pouvez finalement lancer le `Programmer`. Le FPGA enverra les resultats inférés en boucle en UART par paquets de `8bits`, bauds de `19200`, 1 bit de STOP, 1 bit de parité (`EVEN`). Branchez ainsi votre cable USB vers UART au FPGA, en sachant que le `TX` du FPGA est le port `GPIO_1(5)` (`B13` sur la carte `DE0-CV`). N'oubliez pas l'alimentation.

Ouvrez un logiciel vous permettant de regarder l'activite sur ports, tel que `HTERM`. En choisissant la bonne configuration (bon port + spécifications précedantes de l'UART), vous devriez voir un flux continu de réception. Un flag contenant la data `0` sert pour avertir que la prochaine donnée est le résultat du premier neurone du layer de sortie. Puis celui du second neurone du layer de sortie etc...