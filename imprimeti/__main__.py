#!./venv/bin/python
# -*- coding: utf-8 -*-

import sys
import logging
import os
import time

from PyQt5 import QtWidgets, QtCore 

from .erreurs import InitialisationError
from .fenetreprincipale import FenetrePrincipale
from .fenetreparametres import FenetreParametres
from .etiquetteperso import EtiquetteClient
from .bradyip300.bradyip300 import BradyIp300
from . import constantes as const

logger = logging.getLogger(__name__)

def afficher_fenetre_parametres_appli_cb():
    """ Affiche la fenètre des paramètres de l'application
    """    
    fenetre_parametres.show()

def fermer_appli_cb():
    """ Ferme l'application
    """    
    application.closeAllWindows()

def lancer_impression_cb():
    """ Lance l'impression du fichier généré
    """    
    imprimante = BradyIp300(chemin_imprimante=const.BRADY_CHEMIN_PERIPHERIQUE,
                            pas_etiquette=const.BRADY_PAS_ETIQUETTE_MM,
                            decalage_x=const.BRADY_DECALAGE_X_MM,
                            decalage_y=const.BRADY_DECALAGE_Y_MM)
    description_etiquette.creer_fichier_impression(const.FICHIER_SORTIE)
    imprimante.lancer_impression_fichier(const.FICHIER_SORTIE)
    fenetre_principale.initialiser_ihm(description_etiquette)
    fenetre_principale.ui.actionUnitaire.setEnabled(True)

if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    fenetre_principale = FenetrePrincipale()
    fenetre_parametres =  FenetreParametres()
    try:
        const.chargement_constantes_application()
        description_etiquette = EtiquetteClient()
    except InitialisationError as erreur:
        QtWidgets.QMessageBox.critical(fenetre_principale,"Initialisation", erreur.message)  
    fenetre_principale.initialiser_ihm(description_etiquette)
    fenetre_principale.ui.actionQuitter.triggered.connect(fermer_appli_cb)
    fenetre_principale.ui.actionConfig.triggered.connect(afficher_fenetre_parametres_appli_cb)
    fenetre_principale.signalSaisieTerminee.connect(lancer_impression_cb)
    fenetre_principale.show()
    logger.info("Demarrage application")
    sys.exit(application.exec_())

    
