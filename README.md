# emmaus-nasa

Bienvenu

Un ordinateur avec python installé est nécessaire.

Pour télécharger le projet, créez un dossier puis ouvrez un terminal depuis sa racine. 
Dans le terminal, tapez :  
`git clone https://github.com/AlexSavinien/emmaus-nasa.git`

(dans visual studio code, il peut y avoir besoin de refresh l'éditeur. Pour cela ctrl + shift + P -> reload window)

Une fois le projet téléchargé, entrez dans le dossier "emmaus-nasa" :  
`cd emmaus-nasa/`

Activez l'environnement virtuel .venv :  
`source .venv/scripts/activate`

Pour lancer le serveur :  
`python manage.py runserver`

Vous pouvez à présent aller sur le site via l'url fournit dans le terminal. Elle devrait ressembler à cela :  
<http://127.0.0.1:8000/>
      
Le projet est organisé autour d'une app appelée 'nasa'.  
La majorité de la logique du projet se trouve dans  `nasa/views.py` où l'on trouve les deux fonctions view commentées.  

Pour le templating, on trouve dans `templates/` le container html et dans `nasa/templates/nasa/` les deux templates utilisés par les deux views.
