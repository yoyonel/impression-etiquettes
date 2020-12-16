#!./venv/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
import os
import time

from PyQt5 import QtWidgets, QtCore  # module pour wrapper la GUI conçue en Qt5

from imprimeti.erreurs import InitialisationError
from imprimeti.fenetreprincipale import FenetrePrincipale
from imprimeti.fenetreparametres import FenetreParametres
from imprimeti.etiquetteperso import EtiquetteClient
from imprimeti.bradyip300.bradyip300 import BradyIp300
import imprimeti.constantes as const

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
    description_etiquette.creationFichierImpression(FICHIER_SORTIE)
    imprimante.lancementImpression(FICHIER_SORTIE)
    fenetre_principale.initialisation_ihm()
    fenetre_principale.ui.actionUnitaire.setEnabled(True)

if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    fenetre_principale = FenetrePrincipale()
    fenetre_parametres =  FenetreParametres()
    try:
        const.chargement_constantes_application()
        description_etiquette = EtiquetteClient(host=const.BDD_ADRESSE_SERVEUR, user=const.BDD_NOM_UTILISATEUR,
                                      passwd=const.BDD_MOT_DE_PASSE, database=const.BDD_NOM_BASE)
    except InitialisationError as erreur:
        QtWidgets.QMessageBox.critical(fenetre_principale,"Initialisation", erreur.message)  
    fenetre_principale.initialisation_ihm(description_etiquette)
    fenetre_principale.ui.actionQuitter.triggered.connect(fermer_appli_cb)
    fenetre_principale.ui.actionConfig.triggered.connect(afficher_fenetre_parametres_appli_cb)
    fenetre_principale.signalSaisieTerminee.connect(lancer_impression_cb)
    fenetre_principale.show()
    logger.info("Demarrage application")
    sys.exit(application.exec_())

    
