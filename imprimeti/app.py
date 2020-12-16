from dataclasses import dataclass, field

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication

import imprimeti.constantes as const
from imprimeti.bradyip300.bradyip300 import BradyIp300
from imprimeti.erreurs import InitialisationError
from imprimeti.etiquetteperso import EtiquetteClient
from imprimeti.fenetreparametres import FenetreParametres
from imprimeti.fenetreprincipale import FenetrePrincipale


@dataclass
class Imprimi(FenetrePrincipale):
    app: QApplication

    fenetre_parametres: FenetreParametres = field(init=False)
    description_etiquette: EtiquetteClient = field(init=False)

    def __post_init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fenetre_parametres = FenetreParametres()
        try:
            const.chargement_constantes_application()
            self.description_etiquette = EtiquetteClient()
        except InitialisationError as erreur:
            QtWidgets.QMessageBox.critical(self.fenetre_principale, "Initialisation", erreur.message)
        self.init_gui()

    def init_gui(self):
        self.initialiser_ihm(self.description_etiquette)
        self.ui.actionQuitter.triggered.connect(self.fermer_appli_cb)
        self.ui.actionConfig.triggered.connect(self.afficher_fenetre_parametres_appli_cb)
        self.signalSaisieTerminee.connect(self.lancer_impression_cb)

    # https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html#the-pyqtslot-decorator
    @pyqtSlot()
    def afficher_fenetre_parametres_appli_cb(self):
        self.fenetre_parametres.show()

    @pyqtSlot()
    def fermer_appli_cb(self):
        """Ferme l'application"""
        self.app.closeAllWindows()

    @pyqtSlot()
    def lancer_impression_cb(self):
        """Lance l'impression du fichier généré"""
        imprimante = BradyIp300(chemin_imprimante=const.BRADY_CHEMIN_PERIPHERIQUE,
                                pas_etiquette=const.BRADY_PAS_ETIQUETTE_MM,
                                decalage_x=const.BRADY_DECALAGE_X_MM,
                                decalage_y=const.BRADY_DECALAGE_Y_MM)
        self.description_etiquette.creer_fichier_impression(const.FICHIER_SORTIE)
        imprimante.lancer_impression_fichier(const.FICHIER_SORTIE)
        self.initialiser_ihm(self.description_etiquette)
        self.ui.actionUnitaire.setEnabled(True)
