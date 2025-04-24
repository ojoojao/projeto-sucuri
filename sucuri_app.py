import sys
from PySide6.QtWidgets import QApplication
from sucuri_run.interface.IDE import MainWindow

def run_main_app():
    sys.argv += ['-platform', 'windows:darkmode=2']

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    app.exec()

    app.shutdown()

if __name__ == "__main__":
    run_main_app()

from datetime import datetime

data = datetime.strftime()