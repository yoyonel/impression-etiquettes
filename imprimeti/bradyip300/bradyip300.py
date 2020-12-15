# -*- coding: utf-8 -*-
from enum import Enum
import os 

class BradyIp300():
    """
        Module d'impression BRADY IP300 
    """
    def __init__(self, **kwargs):
        # Attributs liés à l'impression
        self.identifiant_peripherique = kwargs.get('chemin_imprimante', None)
        # Attributs liés à la mise en page
        self.pas_etiquette_mm = kwargs.get('pas_etiquette', None)
        self.decalage_x_mm = kwargs.get('decalage_x', None)
        self.decalage_y_mm = kwargs.get('decalage_y', None)

    def modifierOffsetImpressionFichier(self, nom_fichier_a_traiter):
        """Modifie les champs d'offset dans un fichier
        
        Raises:
            KeyError: si aucun champ offset trouvé dans le fichier
        
        Args:
            nom_fichier_a_traiter ([str]): chemin+nom du fichier à traiter
        """     
        def remplaceBaliseParValeur(balise, valeur):
            if balise in donnees_fichier_a_traiter :
                chaine_modifiee = donnees_fichier_a_traiter.replace(balise, str(valeur))
            else:
                raise KeyError("champ {} non trouvé dans le fichier {}".format(balise, nom_fichier_a_traiter))
            return chaine_modifiee

        with open(nom_fichier_a_traiter, "r") as fichier_a_traiter:
            donnees_fichier_a_traiter = fichier_a_traiter.read()

        donnees_fichier_a_traiter = remplaceBaliseParValeur("#offsetX#", self.decalage_x_mm)
        donnees_fichier_a_traiter = remplaceBaliseParValeur("#offsetY#", self.decalage_x_mm)
        donnees_fichier_a_traiter = remplaceBaliseParValeur("#stepLabel#", self.pas_etiquette_mm)

        with open(nom_fichier_a_traiter, "w") as fichier_a_traiter:
            fichier_a_traiter.write(donnees_etiquette)

    def lancementImpression(self, fichier_modele):
        """
        Lancement de l'impression via une commande terminal
        """
        self.modifierOffsetImpressionFichier(fichier_modele)
        # TODO : à remplacer par l'impression lorsque le debug sera terminé
        os.system("cat {}".format(fichier_modele))

    @property
    def identifiant_peripherique(self):
        if self.__identifiant_peripherique == None:
            raise ValueError("identifiant_peripherique non initialisé!")
        return self.__identifiant_peripherique

    @identifiant_peripherique.setter
    def identifiant_peripherique(self, val):
        if type(val) is not str:
            raise TypeError("identifiant_peripherique doit être de type <str>!")
        self.__identifiant_peripherique = val        
        
    @property
    def pas_etiquette_mm(self):
        if self.__pas_etiquette_mm == None:
            raise ValueError("pas_etiquette_mm non initialisé!")
        return self.__pas_etiquette_mm

    @pas_etiquette_mm.setter
    def pas_etiquette_mm(self, val):
        if type(val) is not int:
            raise TypeError("pas_etiquette_mm doit être de type <str>!")
        self.__pas_etiquette_mm = val        

    @property
    def decalage_x_mm(self):
        if self.__decalage_x_mm == None:
            raise ValueError("decalage_x_mm non initialisé!")
        return self.__decalage_x_mm

    @decalage_x_mm.setter
    def decalage_x_mm(self, val):
        if type(val) is not int:
            raise TypeError("decalage_x_mm doit être de type <str>!")
        self.__decalage_x_mm = val        

    @property
    def decalage_y_mm(self):
        if self.__decalage_y_mm == None:
            raise ValueError("decalage_y_mm non initialisé!")
        return self.__decalage_y_mm

    @decalage_y_mm.setter
    def decalage_y_mm(self, val):
        if type(val) is not int:
            raise TypeError("decalage_y_mm doit être de type <str>!")
        self.__decalage_y_mm = val     