import sys
import unittest

sys.path.append("..")

from imprimeti.etiquetteperso import EtiquetteClient



class EtiquetteClientTest(unittest.TestCase):

    def setUp(self):
        self.etiquette = EtiquetteClient()

    def test_mafonction(self):
        self.assertEqual(self.etiquette, 5)


if __name__ == '__main__':
    unittest.main()