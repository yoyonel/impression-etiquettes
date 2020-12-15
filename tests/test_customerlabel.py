import sys
import unittest

sys.path.append("..")

import CustomerLabel
from constants import *


class CustomerLabelTest(unittest.TestCase):

    def setUp(self):
        self.etiquette = CustomerLabel(host=BDD_ADRESSE_SERVEUR, user=BDD_NOM_UTILISATEUR,
                                      passwd=BDD_MOT_DE_PASSE, database=BDD_NOM_BASE)

    def test_mafonction(self):
        self.assertEqual(self.etiquette, 5)


if __name__ == '__main__':
    unittest.main()