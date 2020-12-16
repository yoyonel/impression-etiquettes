#!./venv/bin/python
# -*- coding: utf-8 -*-

import logging
import sys

from PyQt5 import QtWidgets

from imprimeti.app import Imprimi

logger = logging.getLogger(__name__)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Imprimi(app)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
