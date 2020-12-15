# -*- coding: utf-8 -*-

"""
Exceptions personnalisé pour le projet
"""

class InitialisationError(Exception):
    """ Exception lancee lors de l'initialisation """
    def __init__(self, message):
        self.message = "Erreur à l'initialisation de l'application: \n{}".format(message)        