# -*- coding: utf-8 -*-
import logging

from PyQt5 import QtWidgets, QtCore, QtGui

from imprimeti.qt.mainwindow_ui import Ui_MainWindow
from imprimeti.etiquetteperso import EtiquetteClient
from imprimeti import connexion
import imprimeti.constantes as const


logger = logging.getLogger(__name__)

class FenetrePrincipale(QtWidgets.QMainWindow):

    signalSaisieTerminee = QtCore.pyqtSignal()
    '''
        Initialisation de la fenetre
        Entrees: objet étiquette, le parent de la fenetre
    '''
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.comboBoxTypeEtiquette.addItem("Etiquette de Lot")
        self.ui.comboBoxTypeEtiquette.addItem("Etiquette Additionnelle")
        self.ui.comboBoxTypeEtiquette.addItem("Etiquette Opérateur Montage")

        # Connexion de tous les signaux aux callback
        self.ui.actionUndo.triggered.connect(self.annuler_cb)
        self.ui.actionInfo.triggered.connect(self.afficher_fenetre_infos_cb)
        self.ui.comboBoxTypeEtiquette.currentIndexChanged.connect(self.selection_type_etiquette_cb)  
        self.ui.pushBoutonSaisie.clicked.connect(self.lancer_saisie_cb)
        self.ui.lineEditNumeroOf.returnPressed.connect(self.verif_champ_numero_of_cb)
        self.ui.lineEditRefProduit.returnPressed.connect(self.verif_champ_reference_produit_cb)
        self.ui.lineEditQuantite.returnPressed.connect(self.verif_champ_quantite_cb)
        self.ui.lineEditNumeroSerie.returnPressed.connect(self.verif_champ_numero_serie_cb)
        self.ui.lineEditVersion.returnPressed.connect(self.verif_champ_version_cb)
        self.ui.actionUnitaire.triggered.connect(self.imprimer_une_etiquette_cb)

    def initialisation_ihm(self, etiquette):
        """Initialisation de l'IHM

        Args:
            etiquette ([EtiquetteClient]): Objet permettant de définir l'étiquette a imprimer
        """        
        self._position_sequence_ihm = 0

        self.description_etiquette = etiquette

        self.ui.dateEditJour.setDate(QtCore.QDate.currentDate())

        self.ui.actionUnitaire.setEnabled(False)

        self._rempli_combobox_operateur()         

        self._ihm_attente_type_etiquette()

    def _rempli_combobox_operateur(self):
        """Chargement de la liste des opérateurs depuis la bdd et activation du signal
        """        
        enregistrements = connexion.envoi_requete_bdd("SELECT * FROM operateurs")
        for operateur in enregistrements:
            self.ui.comboBoxOperateur.addItem("{} - {} {} {}".format(*operateur[1:5]))

        self.ui.comboBoxOperateur.currentIndexChanged[str].connect(self.selection_operateur)         

    def chargement_sequence_ihm(self, index):
        """ Chargement de la sequence de l'ihm """
        if (index==0):
            self.sequence_ihm = [self._ihm_attente_type_etiquette,
                                self._ihm_attente_selection_operateur,
                                self._ihm_attente_lancement_saisie,
                                self._ihm_attente_saisie_numof,
                                self._ihm_attente_saisie_reference_produit,
                                self._ihm_attente_saisie_quantite,
                                self._ihm_attente_saisie_numero_serie,
                                self._ihm_attente_saisie_version_logicielle]
        elif (index==1):
            self.sequence_ihm = [self._ihm_attente_type_etiquette,
                                self._ihm_attente_selection_operateur,
                                self._ihm_attente_lancement_saisie,
                                self._ihm_attente_saisie_reference_produit,
                                self._ihm_attente_saisie_quantite]
        elif (index==2):
            self.sequence_ihm = [self._ihm_attente_type_etiquette,
                                self._ihm_attente_selection_operateur,
                                self._ihm_attente_lancement_saisie,
                                self._ihm_attente_saisie_reference_produit,
                                self._ihm_attente_saisie_quantite]
        elif (index==3):
            self.sequence_ihm = [self._ihm_attente_type_etiquette,
                                self._ihm_attente_saisie_numero_serie]
        else:
            raise Exception("Index de combobox inconnu")

    def avance_ihm(self):
        """ On avance dans la sequence IHM prédéfinie """
        if self._position_sequence_ihm==len(self.sequence_ihm)-1:
            self.signalSaisieTerminee.emit()            
        else:
            self._position_sequence_ihm += 1
            self.sequence_ihm[self._position_sequence_ihm]()        

    def recule_ihm(self):
        """ On recule dans la sequence IHM prédéfinie """
        self._position_sequence_ihm -= 1
        self.sequence_ihm[self._position_sequence_ihm]()    

    def imprimer_une_etiquette_cb(self):
        self.chargement_sequence_ihm(3)
        self._position_sequence_ihm = 0
        self.description_etiquette.quantite = 1
        self.avance_ihm()

    def _ihm_attente_type_etiquette(self):
        """ Mise à jour de l'IHM en mode attente nom de l'opérateur """    
        # Gestion des champs de saisie
        self.ui.lineEditNumeroOf.clear()
        self.ui.lineEditRefProduit.clear()
        self.ui.lineEditQuantite.clear()
        self.ui.lineEditNumeroSerie.clear()
        self.ui.lineEditVersion.clear()
        self.ui.lineEditNumeroOf.setEnabled(False)
        self.ui.lineEditRefProduit.setEnabled(False)
        self.ui.lineEditQuantite.setEnabled(False)
        self.ui.lineEditNumeroSerie.setEnabled(False)
        self.ui.lineEditVersion.setEnabled(False)
        # Gestion Bouton
        self.ui.pushBoutonSaisie.setEnabled(False)
        self.ui.actionUndo.setEnabled(False)
        # Gestion des comboBox
        self.ui.comboBoxTypeEtiquette.setEnabled(True)
        self.ui.comboBoxOperateur.setEnabled(False)        
        self.ui.dateEditJour.setEnabled(True)
        self.ui.comboBoxOperateur.setCurrentIndex(-1)
        self.ui.comboBoxTypeEtiquette.setCurrentIndex(-1)
        # Barre de status
        self.ui.statusbar.showMessage("Attente sélection du type d'étiquette")
        # Gère le focus
        self.ui.comboBoxTypeEtiquette.setFocus()
        # Interdire l'impression unitaire
        self.ui.actionUnitaire.setEnabled(False)

    def _ihm_attente_selection_operateur(self):
        """ Mise à jour de l'IHM en mode attente nom de l'opérateur """    
        # Gestion des champs de saisie
        self.ui.lineEditNumeroOf.clear()
        self.ui.lineEditRefProduit.clear()
        self.ui.lineEditQuantite.clear()
        self.ui.lineEditNumeroSerie.clear()
        self.ui.lineEditVersion.clear()
        self.ui.lineEditNumeroOf.setEnabled(False)
        self.ui.lineEditRefProduit.setEnabled(False)
        self.ui.lineEditQuantite.setEnabled(False)
        self.ui.lineEditNumeroSerie.setEnabled(False)
        self.ui.lineEditVersion.setEnabled(False)
        # Gestion Bouton
        self.ui.pushBoutonSaisie.setEnabled(False)
        self.ui.actionUndo.setEnabled(True)
        # Gestion des comboBox
        self.ui.comboBoxTypeEtiquette.setEnabled(False)
        self.ui.comboBoxOperateur.setEnabled(True)        
        self.ui.dateEditJour.setEnabled(True)
        self.ui.comboBoxOperateur.setCurrentIndex(-1)
        # Barre de status
        self.ui.statusbar.showMessage("Attente sélection du nom de l'opérateur")
        # Gère le focus
        self.ui.comboBoxOperateur.setFocus()

    def _ihm_attente_lancement_saisie(self):
        """ Mise à jour de l'IHM en mode attente lancement scan """    
        # Gestion des champs de saisie
        self.ui.lineEditNumeroOf.clear()
        self.ui.lineEditRefProduit.clear()
        self.ui.lineEditQuantite.clear()
        self.ui.lineEditNumeroSerie.clear()
        self.ui.lineEditVersion.clear()
        self.ui.lineEditNumeroOf.setEnabled(False)
        self.ui.lineEditRefProduit.setEnabled(False)
        self.ui.lineEditQuantite.setEnabled(False)
        self.ui.lineEditNumeroSerie.setEnabled(False)
        self.ui.lineEditVersion.setEnabled(False)
        # Gestion Bouton
        self.ui.pushBoutonSaisie.setEnabled(True)
        self.ui.actionUndo.setEnabled(True)
        # Gestion des comboBox
        self.ui.comboBoxTypeEtiquette.setEnabled(False)
        self.ui.comboBoxOperateur.setEnabled(False)        
        self.ui.dateEditJour.setEnabled(True)
        # Barre de status
        self.ui.statusbar.showMessage("Vous pouvez lancer la saisie")
        # Gère le focus
        self.ui.pushBoutonSaisie.setFocus()
    
    def _ihm_attente_saisie_numof(self):
        """ Mise à jour de l'IHM en mode attente numero OF """    
        # Gestion des champs de saisie
        self.ui.lineEditNumeroOf.clear()
        self.ui.lineEditRefProduit.clear()
        self.ui.lineEditQuantite.clear()
        self.ui.lineEditNumeroSerie.clear()
        self.ui.lineEditVersion.clear()
        self.ui.lineEditNumeroOf.setEnabled(True)
        self.ui.lineEditRefProduit.setEnabled(False)
        self.ui.lineEditQuantite.setEnabled(False)
        self.ui.lineEditNumeroSerie.setEnabled(False)
        self.ui.lineEditVersion.setEnabled(False)
        # Gestion Bouton
        self.ui.pushBoutonSaisie.setEnabled(False)
        self.ui.actionUndo.setEnabled(True)
        # Gestion des comboBox
        self.ui.comboBoxOperateur.setEnabled(False)
        self.ui.comboBoxTypeEtiquette.setEnabled(False)
        self.ui.dateEditJour.setEnabled(False)
        # Barre de status
        self.ui.statusbar.showMessage("Attente scan Numero OF")
        # Gère le focus
        self.ui.lineEditNumeroOf.setFocus()
       
    def _ihm_attente_saisie_reference_produit(self):
        """ Mise à jour de l'IHM en mode attente reference produit """    
        # Gestion des champs de saisie
        self.ui.lineEditRefProduit.clear()
        self.ui.lineEditQuantite.clear()
        self.ui.lineEditNumeroSerie.clear()
        self.ui.lineEditVersion.clear()
        self.ui.lineEditNumeroOf.setEnabled(False)
        self.ui.lineEditRefProduit.setEnabled(True)
        self.ui.lineEditQuantite.setEnabled(False)
        self.ui.lineEditNumeroSerie.setEnabled(False)
        self.ui.lineEditVersion.setEnabled(False)
        # Gestion Bouton
        self.ui.pushBoutonSaisie.setEnabled(False)
        self.ui.actionUndo.setEnabled(True)
        # Gestion des comboBox
        self.ui.comboBoxOperateur.setEnabled(False)
        self.ui.comboBoxTypeEtiquette.setEnabled(False)
        self.ui.dateEditJour.setEnabled(False)
        # Barre de status
        self.ui.statusbar.showMessage("Attente scan Reference Produit")
        # Gère le focus
        self.ui.lineEditRefProduit.setFocus()       

    def _ihm_attente_saisie_quantite(self):
        """ Mise à jour de l'IHM en mode attente quantite """    
        # Gestion des champs de saisie
        self.ui.lineEditQuantite.clear()
        self.ui.lineEditNumeroSerie.clear()
        self.ui.lineEditVersion.clear()
        self.ui.lineEditNumeroOf.setEnabled(False)
        self.ui.lineEditRefProduit.setEnabled(False)
        self.ui.lineEditQuantite.setEnabled(True)
        self.ui.lineEditNumeroSerie.setEnabled(False)
        self.ui.lineEditVersion.setEnabled(False)
        # Gestion Bouton
        self.ui.pushBoutonSaisie.setEnabled(False)
        self.ui.actionUndo.setEnabled(True)
        # Gestion des comboBox
        self.ui.comboBoxOperateur.setEnabled(False)
        self.ui.comboBoxTypeEtiquette.setEnabled(False)
        self.ui.dateEditJour.setEnabled(False)
        # Barre de status
        self.ui.statusbar.showMessage("Attente scan Quantité sur OF")
        # Gère le focus
        self.ui.lineEditQuantite.setFocus()   

    def _ihm_attente_saisie_numero_serie(self):
        """ Mise à jour de l'IHM en mode attente numéro de série """    
        # Gestion des champs de saisie
        self.ui.lineEditNumeroSerie.clear()
        self.ui.lineEditVersion.clear()
        self.ui.lineEditNumeroOf.setEnabled(False)
        self.ui.lineEditRefProduit.setEnabled(False)
        self.ui.lineEditQuantite.setEnabled(False)
        self.ui.lineEditNumeroSerie.setEnabled(True)
        self.ui.lineEditVersion.setEnabled(False)
        # Gestion Bouton
        self.ui.pushBoutonSaisie.setEnabled(False)
        self.ui.actionUndo.setEnabled(True)
        # Gestion des comboBox
        self.ui.comboBoxOperateur.setEnabled(False)
        self.ui.comboBoxTypeEtiquette.setEnabled(False)
        self.ui.dateEditJour.setEnabled(False)
        # Barre de status
        self.ui.statusbar.showMessage("Attente scan Quantité sur OF")
        # Gère le focus
        self.ui.lineEditNumeroSerie.setFocus()   

    def _ihm_attente_saisie_version_logicielle(self):
        """ Mise à jour de l'IHM en mode attente version logiciel """    
        # Gestion des champs de saisie
        self.ui.lineEditVersion.clear()
        self.ui.lineEditNumeroOf.setEnabled(False)
        self.ui.lineEditRefProduit.setEnabled(False)
        self.ui.lineEditQuantite.setEnabled(False)
        self.ui.lineEditNumeroSerie.setEnabled(False)
        self.ui.lineEditVersion.setEnabled(True)
        # Gestion Bouton
        self.ui.pushBoutonSaisie.setEnabled(False)
        self.ui.actionUndo.setEnabled(True)
        # Gestion des comboBox
        self.ui.comboBoxOperateur.setEnabled(False)
        self.ui.comboBoxTypeEtiquette.setEnabled(False)
        self.ui.dateEditJour.setEnabled(False)
        # Barre de status
        self.ui.statusbar.showMessage("Attente scan Version Logicielle")
        # Gère le focus
        self.ui.lineEditVersion.setFocus()   

    def annuler_cb(self):
        """  """
        self.recule_ihm()
        
    def afficher_fenetre_infos_cb(self):
        """ Permet d'afficher une fenetre d'information pour l'opérateur """
        QtWidgets.QMessageBox.information(self, "A propos", "Logiciel Impression Etiquettes Produits\rR.DUGIED\r10/07/2020")

    def selection_type_etiquette_cb(self, index):
        """  """
        if index!=-1 :
            self.description_etiquette.type_etiquette = index
            self.chargement_sequence_ihm(index)
            self.avance_ihm()

    def selection_operateur(self, selected_line):
        """  """
        try:
            if selected_line!="":
                self.description_etiquette.code_operateur = selected_line.split()[0]
                self.description_etiquette.initiales_operateur = selected_line.split()[4]
                self.avance_ihm()
        except Exception as erreur:
            QtWidgets.QMessageBox.warning(self, "Erreur", "{}".format(erreur))
            logger.warning(erreur)

    def lancer_saisie_cb(self):
        """ Lance la saisie avec lecteur code à barre et renseigne la date dans l'objet Etiquette """
        try:
            self.description_etiquette.date_garantie = self.ui.dateEditJour.date().toString(QtCore.Qt.DateFormat.DefaultLocaleShortDate)
            self.avance_ihm()
        except Exception as erreur:
            QtWidgets.QMessageBox.warning(self, "Erreur", "{}".format(erreur))
            logger.warning(erreur)

    def verif_champ_numero_of_cb(self):
        """ Verifie les infos saisie dans le champ Numéro OF """
        try:
            saisie = str(self.ui.lineEditNumeroOf.text())
            if (len(saisie)==7) and (saisie[:2]=="OF"):
                self.description_etiquette.numero_of = saisie[2:]
                self.avance_ihm()
            else:
                self.ui.lineEditNumeroOf.clear() 
        except Exception as erreur:
            QtWidgets.QMessageBox.warning(self, "Erreur", "{}".format(erreur))
            self.ui.lineEditNumeroOf.clear() 
            logger.warning(erreur)

    def verif_champ_reference_produit_cb(self):
        """ Verifie les infos saisie dans le champ Reference Produit  """
        try:
            saisie = str(self.ui.lineEditRefProduit.text())
            if (11<=len(saisie)<=14) and (saisie[:2]=="RP"):
                self.description_etiquette.reference_produit = saisie[2:]
                # Rafraichissement de la sequence_ihm en fonction des infos lue en bdd
                if not self.description_etiquette.produit_serialise :
                    if (self.sequence_ihm.count(self._ihm_attente_saisie_numero_serie) == 1):
                        del self.sequence_ihm[self.sequence_ihm.index(self._ihm_attente_saisie_numero_serie)]
                if not self.description_etiquette.produit_versionne :
                    if (self.sequence_ihm.count(self._ihm_attente_saisie_version_logicielle) == 1):
                        del self.sequence_ihm[self.sequence_ihm.index(self._ihm_attente_saisie_version_logicielle)]      
                self.avance_ihm()
            else:
                self.ui.lineEditRefProduit.clear() 
        except Exception as erreur:
            QtWidgets.QMessageBox.warning(self, "Erreur", "{}".format(erreur))
            self.ui.lineEditRefProduit.clear() 
            logger.warning(erreur)

    def verif_champ_quantite_cb(self):
        """ Verifie les infos saisie dans le champ Quantité """
        try:
            saisie = str(self.ui.lineEditQuantite.text())
            if (len(saisie)>=2) and (saisie[0]=="Q"):
                self.description_etiquette.quantite = int(saisie[1:])
                self.avance_ihm()
            else:
                self.ui.lineEditQuantite.clear() 
        except Exception as erreur:
            QtWidgets.QMessageBox.warning(self, "Erreur", "{}".format(erreur))
            self.ui.lineEditQuantite.clear() 
            logger.warning(erreur)

    def verif_champ_numero_serie_cb(self):
        """ Verifie les infos saisie dans le champ Numéro de Série """
        try:
            saisie = str(self.ui.lineEditNumeroSerie.text())
            if (len(saisie)==8) and (saisie[:2]=="NS"):
                self.description_etiquette.numero_serie = int(saisie[2:])
                self.avance_ihm()
            else:
                self.ui.lineEditNumeroSerie.clear() 
        except Exception as erreur:
            QtWidgets.QMessageBox.warning(self, "Erreur", "{}".format(erreur))
            logger.warning(erreur)

    def verif_champ_version_cb(self):
        """ Verifie les infos saisie dans le champ Version """
        try:
            saisie = str(self.ui.lineEditVersion.text())
            if (5<=len(saisie)<=6) and (saisie[0]=="V"):
                self.description_etiquette.version_logicielle = saisie
                self.avance_ihm()
            else:
                self.ui.lineEditVersion.clear() 
        except Exception as erreur:
            QtWidgets.QMessageBox.warning(self, "Erreur", "{}".format(erreur))
            logger.warning(erreur)
