# IMPRESSION-ETIQUETTES


The source code is [available at GitHub](https://github.com/RomualdDugied/labelprintermanager).

## Presentation du projet

Logiciel de gestion des étiquettes pour la production.

Les étiquettes sont imprimés par une imprimante Brady IP300

L'imprimante utilise un fichier de description pour le formatage et les données à imprimer.

## Environnement

- Une base de données MariaDB
    - Table "opérateurs"
        - code_operateur(INT) une sorte de n°badge
        - nom (VAR CHAR[255])
        - prenom (VAR CHAR[255])
        - initiales (VAR CHAR[6])
    - Table "etilot"  
        - CodeProduit (VAR CHAR[10]) reférence alphanumérique
        - Serialized (BOOL) si True un champ n° serie présent sur l'étiquette
        - Versioned (BOOL) si True un champ version firmware présent sur l'etiquette
        - TemplateLot (VAR CHAR[255]) nom du fichier modèle pour l'étiquette de lot
        - TemplateCraft (VAR CHAR[255]) nom du fichier modèle pour l'étiquette d'assemblage
        - ReferenceClient (VAR CHAR[255]) référence personnel du client
        - NomClient (VAR CHAR[255])
        - Enable (BOOL) si True l'étiquette est valide pour la production

- Un fichier JSON contenant les paramètres de l'application
    - Infos de connexion à la DATABASE
    - Infos concernant l'imprimante (Port, offset d'impression...)
    - Des paramètres de l'application (chemin du dossier des modèles, chemin fichier de sortie)

- Un lecteur CAB (en émulation clavier) pour la saisie des champs (une saisie manuel est autorisé)

## Descriptif des fenêtres Qt
### Fenetre Principale:

![GUI fenetre principale](https://raw.githubusercontent.com/RomualdDugied/impression-etiquettes/master/screenshots/ihm_rempli.png)


- Champs à renseigner :
    - Type d'étiquette
    - Nom de l'opérateur (Je prévois à terme de scanner un badge)
    - Date à indiquer sur l'étiquette
    - Numero OF (le lot)
    - Référence Produit
    - Quantité
    - Premier numéro de série du lot
    - Version du firmware

- Un bouton pour lancer la saisie des codes à barres

- Un panneau latéral
    - Bouton d'édition/visualisation des paramètres de l'application
    - Bouton de retour (utilisable lors de la saisie des codes à barres)
    - Bouton d'information sur l'appli
    - Bouton de re-impression unitaire
    - Bouton pour fermer l'appli

- Une status barre dont le rôle est de guider l'opérateur dans le déroulement du scénario de saisie

### Fenetre Paramètres:
![GUI fenetre principale](https://raw.githubusercontent.com/RomualdDugied/impression-etiquettes/master/screenshots/ihm_parametres.png)

- Paramètres généraux
    - Fichier de sortie qui sera généré par l'appli et envoyé à l'imprimante
    - Port où est branché de l'imprimante

- Paramètres liés à la base MariaDB
    - Adresse de la base
    - Utilisateur
    - Mot de passe
    - Nom de la base

- Paramètre de mise en page pour l'impression
    - Offset en X
    - Offser en Y
    - Pas Horizontal entre 2 étiquettes


## Initialisation

- chargement paramètres appli issue d'un fichier JSON

## Fonctionnement

- Mode Production
    - l'Opérateur choisi dans une ComboBox le type d'étiquette qu'il souhaite imprimer
    - il scanne les informations (les champs sont proposés en fonction de la nécessité)
    - impression des étiquettes

- Possibilité de revenir en arrière lors de la saisie avec le bouton de retour
- Possibilité re-imprimer une étiquette du dernier lot saisie, si il y a eu un défaut d'impression par exemple.

