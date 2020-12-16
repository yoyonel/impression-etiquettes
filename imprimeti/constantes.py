#!./venv/bin/python
# -*- coding: utf-8 -*-

import json



from imprimeti.erreurs import InitialisationError
from imprimeti import connexion


FICHIER_PARAMETRES_APPLI = "settings.json"

# Constantes globales pour l'accès à la bdd de production
BDD_ADRESSE_SERVEUR = ''
BDD_NOM_UTILISATEUR = ''
BDD_MOT_DE_PASSE = ''
BDD_NOM_BASE = ''

# Constantes globales pour le paramétrage de la mise en page 
BRADY_CHEMIN_PERIPHERIQUE = ''
BRADY_PAS_ETIQUETTE_MM = 0
BRADY_DECALAGE_X_MM = 0
BRADY_DECALAGE_Y_MM = 0

DOSSIER_TEMPLATE = ""
FICHIER_SORTIE = ""


class TypeEtiquette():
    TYPE_OF = 0
    TYPE_ADDITIONNEL = 1
    TYPE_OPERATEUR_MONTAGE = 2


class ChampBdd():
    INDEX = 0
    # Les champs de la table etilot
    REFERENCE_PRODUIT = 1
    PRODUIT_SERIALISE = 2
    PRODUIT_VERSIONNE = 3
    FICHIER_MODELE_OF = 4
    FICHIER_MODELE_ADDITIONNEL = 5
    FICHIER_MODELE_MONTAGE = 6
    REFERENCE_CLIENT = 7
    NOM_CLIENT = 8
    PRODUIT_VALIDE = 9
    # Les champs de la table operateurs
    CODE_OPERATEUR = 1
    NOM_OPERATEUR = 2
    PRENOM_OPERATEUR = 3
    INITIALES_OPERATEUR = 4


def chargement_constantes_application():
    """ Chargement des constantes du projet depuis le fichier json
    """
    global BDD_ADRESSE_SERVEUR
    global BDD_NOM_UTILISATEUR
    global BDD_MOT_DE_PASSE
    global BDD_NOM_BASE
    global BRADY_CHEMIN_PERIPHERIQUE
    global BRADY_PAS_ETIQUETTE_MM
    global BRADY_DECALAGE_X_MM
    global BRADY_DECALAGE_Y_MM
    global DOSSIER_TEMPLATE
    global FICHIER_SORTIE

    try:
        with open(FICHIER_PARAMETRES_APPLI, "r") as fichier_parametres:
            parametres = json.load(fichier_parametres)

        BDD_ADRESSE_SERVEUR = parametres['basededonnees']['nom_hote']
        BDD_NOM_UTILISATEUR = parametres['basededonnees']['nom_utilisateur']
        BDD_MOT_DE_PASSE = parametres['basededonnees']['mot_de_passe']
        BDD_NOM_BASE = parametres['basededonnees']['nom_basededonnees']
        BRADY_CHEMIN_PERIPHERIQUE = parametres['bradyIP300']['port_usb']
        BRADY_PAS_ETIQUETTE_MM = parametres['bradyIP300']['pas_etiquette']
        BRADY_DECALAGE_X_MM = parametres['bradyIP300']['decalage_x']
        BRADY_DECALAGE_Y_MM = parametres['bradyIP300']['decalage_y']
        DOSSIER_TEMPLATE = parametres['application']['dossier_modele']
        FICHIER_SORTIE = parametres['application']['fichier_sortie']
    except KeyError as erreur:
        raise InitialisationError("Clé non présente dans le fichier JSON!")
    except FileNotFoundError as erreur :
        raise InitialisationError("Fichier JSON {} introuvable!".format(fichier_json))
    except Exception as erreur:
        raise InitialisationError("Erreur non répertorié-> {}".format(erreur))

    