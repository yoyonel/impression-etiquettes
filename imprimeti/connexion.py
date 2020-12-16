#!./venv/bin/python
# -*- coding: utf-8 -*-


import mysql.connector as MC

import imprimeti.constantes as const


def essai_connexion_bdd():
    pass

def envoi_requete_bdd(requete):
    """ Chargement de la liste des opérateurs depuis la base de données
    """
    try:
        mysql_connexion = None
        mysql_connexion = MC.connect(host=const.BDD_ADRESSE_SERVEUR, user=const.BDD_NOM_UTILISATEUR,
                                    passwd=const.BDD_MOT_DE_PASSE, database=const.BDD_NOM_BASE)
        mysql_curseur = mysql_connexion.cursor()
        mysql_curseur.execute(str(requete))
        enregistrements = mysql_curseur.fetchall()
        mysql_curseur.close()        
        mysql_connexion.close()
        return enregistrements    
    except MC.Error as erreur:
        print(erreur)
    finally:
        if mysql_connexion :
            if mysql_connexion.is_connected():
                mysql_connexion.close()

