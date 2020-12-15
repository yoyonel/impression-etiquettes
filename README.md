# LABEL PRINTER MANAGER


The source code is [available at GitHub](https://github.com/RomualdDugied/labelprintermanager).

## Presentation du projet

Logiciel de gestion des étiquettes pour la production.

Les étiquettes sont imprimés par une imprimante Brady IP300

## Arborescence
```
/.vscode
	launch.json
	settings.json
```
> *Dossier contenant la documentation du projet*
```
/docs
	synoptique.odg
		Synoptique des interactions entre les modules du projet
```
> Dossier contenant les sources python du projet
```
/labelprintermanager
	/bradyip300
		__init__.py
		bradyip300.py
			Module contenant les routines de pilotage de l’imprimante IP300
	/qt       /* Dossier contenant les ihm designer sous QtDesigner */
		icons_rc.py
			Module exporté par pyrcc5 contenant les images/icones
		mainwindow_ui.py
			Module exporté par pyuic5 contenant une fenêtre issue de QtDesigner
		setupwindow_ui.py
				Module exporté par pyuic5 contenant une fenêtre issue de QtDesigner
	__init__.py
	__main__.py
		Module principale du projet
	constants.py
		Module contenant les constantes du projet
	customerlabel.py
		Module contenant l’objet CustomerLabel permettant la définition des étiquettes
	mywindow.py
		Module contenant la fenêtre principale
```
> Dossier contenant les logs de l’application
```
/logs
```
> Dossier contenant les ressources de l'application (ui, icones, images)
```
/res
```       	
> Dossier contenant les fichiers gabarit des étiquettes

```
/modeles	
```
> Dossier de l’environnement virtuel
```
/venv

.flake8
	Fichier de config du controleur de code python flake
.gitignore
	Fichier de configuration de l'outil cvs
LICENSE
	Licence du projet
MANIFEST.in
	Fichier pour l'inclusion dans le paquet des fichiers annexes
README.md
	Ce fichier
settings.json
setup.py
	Fichier setup du package python
```

### Auteur(s)
Romu

