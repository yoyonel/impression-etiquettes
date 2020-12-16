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

- Champ à renseigner :
    - Type d'étiquette
    - Nom de l'opérateur (Je prévois à terme de scanner un badge)
    - Date à indiquer sur l'étiquette
    - Numero OF (le lot)
    - Référence Produit
    - Quantité
    - Premier numéro de série du lot
    - Version du firmware



## Initialisation

- chargement paramètres appli issue d'un fichier JSON

# Fonctionnement

- Mode Production
    - l'Opérateur choisi dans une ComboBox le type d'étiquette qu'il souhaite imprimer
    - il scanne les informations ( les champs sont proposés en fonction de la nécessité)
    - l'application propose à l'opérateur d'imprimer
