# -*- coding: utf-8 -*-
import mysql.connector as MC
import re
import sys
import os
import logging

from imprimeti.constantes import *

logger = logging.getLogger(__name__)

class EtiquetteClient():
    """  
        Objet EtiquetteClient
    """
    def __init__(self, **kwargs):
        """  """
        # Attributs liés au contenu de l'étiquette
        self.__type_etiquette = None
        self.__code_operateur = None
        self.__initiales_operateur = None
        self.__numero_of = None
        self.__reference_produit = None
        self.__reference_client = None
        self.__quantite = None
        self.__numero_serie = None
        self.__version_logicielle = None
        self.__chemin_fichier_modele = None        
        self.__date_garantie = None
        
        self.produit_serialise = False
        self.produit_versionne = False
        self.produit_valide = False
        self.essaiConnexionDatabase(**kwargs)

    def essaiConnexionDatabase(self, **kwargs):
        """Fonction permettant une tentative de connexion à la base de donnée

        Args:
            **kwargs ([dict]): paramètres de la connexion par mots clés

        Returns:
            [type]: [description]
        """            
        self.__parametres_bdd = kwargs
        try:
            mysql_connexion = MC.connect(**self.__parametres_bdd)
        except MC.Error as err:
            print(err)
        finally:
            if mysql_connexion.is_connected():
                mysql_connexion.close()

    def envoiRequeteDatabase(self, requete):
        try:
            mysql_connexion = MC.connect(**self.__parametres_bdd)
            mysql_curseur = mysql_connexion.cursor()
            mysql_curseur.execute(requete)
            return mysql_curseur.fetchall()
        except MC.Error as err:
            print(err)
        finally:
            if mysql_connexion.is_connected():
                mysql_connexion.close()
                
    def __str__(self):
        return ("type_etiquette = {}\n\
            code_operateur = {}\n\
            initiales_operateur = {}\n\
            numero_of = {}\n\
            reference_produit = {}\n\
            date_garantie= {}\n\
            quantite = {}\n\
            numero_serie = {}\n\
            version_logicielle = {}\n\
            ".format(self.type_etiquette, self.code_operateur, self.initiales_operateur, self.numero_of, self.reference_produit, self.date_garantie, self.quantite, self.numero_serie, self.version_logicielle))

    @property
    def type_etiquette(self):
        if self.__type_etiquette == None:
            raise ValueError("type_etiquette non initialisé!")
        return self.__type_etiquette

    @type_etiquette.setter
    def type_etiquette(self, valeur):
        if type(valeur) is not int:
            raise TypeError("type_etiquette doit être de type <int>!")
        if not (0 <= valeur <= 2):
            raise ValueError("type_etiquette doit être compris entre 0 et 2!")
        self.__type_etiquette = valeur
        logger.debug("type_etiquette = {}".format(valeur))

    @property
    def code_operateur(self):
        if self.__code_operateur == None:
            raise ValueError("code_operateur non initialisé!")
        return self.__code_operateur

    @code_operateur.setter
    def code_operateur(self, valeur):
        if type(valeur) is not str:
            raise TypeError("code_operateur doit être de type <str>!")
        if not valeur.isdigit():
            raise "code_operateur doit être un nombre!"
        valeur = int(valeur)
        if not (1 <= valeur <= 99):
            raise ValueError("code_operateur doit être compris entre 1 et 99!")
        self.__code_operateur = valeur
        logger.debug("code_operateur = {}".format(valeur))

    @property
    def initiales_operateur(self):
        if self.__initiales_operateur == None:
            raise ValueError("initiales_operateur non initialisé!")
        return self.__initiales_operateur

    @initiales_operateur.setter
    def initiales_operateur(self, valeur):
        if type(valeur) is not str:
            raise TypeError("initiales_operateur doit être de type <str>!")
        self.__initiales_operateur = valeur
        logger.debug("initiales_operateur = {}".format(valeur))

    @property
    def numero_of(self):
        if self.__numero_of == None:
            raise ValueError("numero_of non initialisé!")
        return self.__numero_of

    @numero_of.setter
    def numero_of(self, valeur):
        if type(valeur) is not str:
            raise TypeError("numero_of doit être de type <str>!")
        if not valeur.isdigit():
            raise ValueError("numero_of doit être un entier!")
        valeur = int(valeur)
        if not (10000 <= valeur <= 99999):
            raise ValueError("numero_of doit être compris entre 10000 et 99999!")
        self.__numero_of = valeur
        logger.debug("numero_of = {}".format(valeur))

    @property
    def reference_produit(self):
        if self.__reference_produit == None:
            raise ValueError("reference_produit non initialisé!")
        return self.__reference_produit

    @reference_produit.setter
    def reference_produit(self, valeur):
        if type(valeur) is not str:
            raise TypeError("reference_produit doit être de type <str>!")
        if not valeur.isalnum():
            raise ValueError("reference_produit doit être un alpha numérique")
        try:
            mysql_connexion = MC.connect(**self.__parametres_bdd)
            mysql_curseur = mysql_connexion.cursor()
            # Recherche du code produit dans la table etilot
            mysql_curseur.execute("""SELECT * FROM etilot WHERE CodeProduit="{}" """.format(valeur))
            enregistrements = mysql_curseur.fetchall()
            nombre_enregistrements = (len(enregistrements))
            if nombre_enregistrements == 0:
                raise ValueError("Référence produit {} non présent dans la base!".format(valeur))
            elif nombre_enregistrements == 1:
                if (self.type_etiquette == TypeEtiquette.TYPE_OF ):
                    self.chemin_fichier_modele = DOSSIER_TEMPLATE + str(enregistrements[0][ChampBdd.FICHIER_MODELE_OF])
                elif (self.type_etiquette == TypeEtiquette.TYPE_ADDITIONNEL ):
                    self.chemin_fichier_modele = DOSSIER_TEMPLATE + str(enregistrements[0][ChampBdd.FICHIER_MODELE_ADDITIONNEL])
                elif (self.type_etiquette == TypeEtiquette.TYPE_OPERATEUR_MONTAGE ):
                    self.chemin_fichier_modele = DOSSIER_TEMPLATE + str(enregistrements[0][ChampBdd.FICHIER_MODELE_MONTAGE])
                if (self.chemin_fichier_modele == DOSSIER_TEMPLATE):
                    raise Exception("Fichier modèle étiquette non renseigné dans la base")
                self.reference_client = str(enregistrements[0][ChampBdd.REFERENCE_CLIENT])
                self.produit_serialise = bool(enregistrements[0][ChampBdd.PRODUIT_SERIALISE])
                self.produit_versionne = bool(enregistrements[0][ChampBdd.PRODUIT_VERSIONNE])
                self.produit_valide = bool(enregistrements[0][ChampBdd.PRODUIT_VALIDE])
                if (not self.produit_valide):
                    raise Exception("Etiquette non validée techniquement ou changement de version en cours. Veuillez appeler un technicien!")
            else :
                raise ValueError("Doublons dans la base pour ce code produit!")
        except MC.Error as err:
            print(err)
        finally:
            if mysql_connexion.is_connected():
                mysql_connexion.close()

        self.__reference_produit = valeur
        logger.debug("reference_produit = {}".format(valeur))

    @property
    def reference_client(self):
        if self.__reference_client == None:
            raise ValueError("reference_client non initialisé!")
        return self.__reference_client

    @reference_produit.setter
    def reference_client(self, valeur):
        if type(valeur) is not str:
            raise TypeError("reference_produit doit être de type <str>!")
        self.__reference_client=valeur

    @property
    def quantite(self):
        if self.__quantite == None:
            raise ValueError("quantite non initialisé!")
        return self.__quantite

    @quantite.setter
    def quantite(self, valeur):
        if type(valeur) is not int:
            raise TypeError("quantite doit être de type <int>!")
        if (valeur < 1):
            raise ValueError("quantite doit être un nombre positif non nul!")
        self.__quantite = valeur

    @property
    def numero_serie(self):
        if self.__numero_serie == None:
            raise ValueError("numero_serie non initialisé!")
        return self.__numero_serie

    @numero_serie.setter
    def numero_serie(self, valeur):
        if type(valeur) is not int:
            raise TypeError("numero_serie doit être de type <int>!")
        if not (100001 <= valeur <= 999999):
            raise ValueError("numero_serie doit être compris entre 100001 à 999999!")
        self.__numero_serie = valeur

    @property
    def version_logicielle(self):
        if self.__version_logicielle == None:
            raise ValueError("version_logicielle non initialisé!")
        return self.__version_logicielle

    @version_logicielle.setter
    def version_logicielle(self, valeur):
        if type(valeur) is not str:
            raise TypeError("version_logicielle doit être de type <str>!")
        if not (4 <= len(valeur) <= 5):
            raise ValueError("longueur de version_logicielle non conforme")
        self.__version_logicielle = valeur

    @property
    def chemin_fichier_modele(self):
        if self.__chemin_fichier_modele == None:
            raise ValueError("chemin_fichier_modele non initialisé!")
        return self.__chemin_fichier_modele

    @chemin_fichier_modele.setter
    def chemin_fichier_modele(self, valeur):
        if type(valeur) is not str:
            raise TypeError("chemin_fichier_modele doit être de type <str>!")
        if not os.path.exists(valeur):
            raise IOError("{} Fichier introuvable !".format(valeur))
        self.__chemin_fichier_modele = valeur

    @property
    def date_garantie(self):
        if self.__date_garantie == None:
            raise ValueError("date_garantie non initialisé!")
        return self.__date_garantie

    @date_garantie.setter
    def date_garantie(self, valeur):
        if type(valeur) is not str:
            raise TypeError("date_garantie doit être de type <str>!")
        if (re.search("[0-9]{2}/[0-9]{2}/[0-9]{4}", valeur) is None):
            raise ValueError("date_garantie doit être au format dd/mm/yyyy!")
        self.__date_garantie = valeur

    def creationFichierImpression(self, fichier_sortie):
        """
            Fonction générant le fichier d'impression de l'étiquette
        """
        with open(self.chemin_fichier_modele, "r") as fichier_modele:
            specifications_etiquette = fichier_modele.read()

        if ("#referenceClient#" in specifications_etiquette):
            specifications_etiquette = specifications_etiquette.replace("#referenceClient#", self.reference_client)

        if ("#referenceHorizon#" in specifications_etiquette):
            specifications_etiquette = specifications_etiquette.replace("#referenceHorizon#", self.reference_produit)

        if ("#shortReferenceHorizon#" in specifications_etiquette):
            # ajout d'espace(s) si necessaire
            specifications_etiquette = specifications_etiquette.replace("#shortReferenceHorizon#", (self.reference_produit[5:]+"  ")[:6])

        if ("#codeOperateur#" in specifications_etiquette):
            specifications_etiquette = specifications_etiquette.replace("#codeOperateur#", str(self.code_operateur))

        if ('#initialesOperateur#' in specifications_etiquette):
            specifications_etiquette = specifications_etiquette.replace("#initialesOperateur#", self.initiales_operateur)

        if ("#numeroOf#" in specifications_etiquette):
            specifications_etiquette = specifications_etiquette.replace("#numeroOf#", str(self.numero_of))

        if ("#numeroSerie#" in specifications_etiquette):
            specifications_etiquette = specifications_etiquette.replace("#numeroSerie#", str(self.numero_serie))

        if ("#date#" in specifications_etiquette):
            specifications_etiquette = specifications_etiquette.replace("#date#", self.date_garantie)

        if ("#numeroVersion#" in specifications_etiquette):
            specifications_etiquette = specifications_etiquette.replace("#numeroVersion#", self.version_logicielle)

        if ("#nombreEtiquettes#" in specifications_etiquette):
            specifications_etiquette = specifications_etiquette.replace("#nombreEtiquettes#", str(self.quantite))

        with open(fichier_sortie, "w") as fichier:
            fichier.write(specifications_etiquette)
