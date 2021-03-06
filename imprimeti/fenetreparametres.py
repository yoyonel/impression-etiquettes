# -*- coding: utf-8 -*-
import logging
from logging import raiseExceptions

from PyQt5 import QtWidgets, QtCore, QtGui

from .etiquetteperso import EtiquetteClient
from .qt.setupwindow_ui import Ui_SetUpWindow
from . import constantes as const

logger = logging.getLogger(__name__)

class FenetreParametres(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_SetUpWindow()
        self.ui.setupUi(self)
   
    def show(self):
        QtWidgets.QMainWindow.show(self)

        self.ui.lineEditDatabaseName.setText(const.BDD_NOM_BASE)
        self.ui.lineEditPassword.setText(const.BDD_MOT_DE_PASSE)
        self.ui.lineEditUserName.setText(const.BDD_NOM_UTILISATEUR)
        self.ui.lineEditHostName.setText(const.BDD_ADRESSE_SERVEUR)

        self.ui.lineEditOutFilename.setText(const.FICHIER_SORTIE)
        self.ui.lineEditDeviceName.setText(const.BRADY_CHEMIN_PERIPHERIQUE)
    
        self.ui.pushButtonApply.setEnabled(False)

        self.ui.pushButtonApply.clicked.connect(self.appliquer_modifications)
        self.ui.pushButtonCancel.clicked.connect(self.fermer_fenetre)

    def appliquer_modifications(self):
        #TODO gérer l'enregistrement des modifications
        self.close()

    def fermer_fenetre(self):
        #TODO gérer la vérification si des modifs ont été effectué
        self.close()