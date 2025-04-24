from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QPlainTextEdit, QGridLayout, QListWidget, QFileDialog, QHBoxLayout, QVBoxLayout, QListWidgetItem

from .highlight import PythonHighlighter
from ..core.runs import run_script, transform_in_py

import os, sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sucuri IDE")

        self.widgets()
        self.config_widgets()
        self.set_layout() 
        self.set_fonts()

    def widgets(self):
        self.open_path_button = QPushButton()
        self.list_widget_files = QListWidget()
        self.save_file_button = QPushButton()
        self.create_file_button = QPushButton()
        
        self.run_code_button = QPushButton()
        self.plain_text_code = QPlainTextEdit()
        self.plain_text_terminal = QPlainTextEdit()

    def config_widgets(self):
        self.open_path_button.setText("Abri pasta")
        self.open_path_button.clicked.connect(self.add_list_files)

        self.list_widget_files.setMaximumWidth(200)
        self.list_widget_files.clicked.connect(self.open_selected_file) 

        self.save_file_button.setText("Salvar")
        self.save_file_button.setMaximumWidth(200)
        self.save_file_button.clicked.connect(self.save_file)
        
        self.create_file_button.setText("Novo")
        self.create_file_button.setMaximumWidth(200)
        self.create_file_button.clicked.connect(self.create_new_file)


        self.run_code_button.setMaximumWidth(100)
        self.run_code_button.setText("Rodar")
        self.run_code_button.clicked.connect(self.run_code)

        self.plain_text_code.setMinimumWidth(500)
        self.plain_text_code.setMinimumHeight(500)
        self.plain_text_code.installEventFilter(self)
        PythonHighlighter(self.plain_text_code.document())

        self.plain_text_terminal.setMaximumHeight(250)

    def set_layout(self):
        hlyt = QHBoxLayout()
        hlyt.addWidget(self.create_file_button)
        hlyt.addWidget(self.save_file_button)
        
        vlyt = QVBoxLayout()
        vlyt.addWidget(self.plain_text_code)
        vlyt.addWidget(self.plain_text_terminal)

        lyt = QGridLayout()
        self.setLayout(lyt)

        lyt.addWidget(self.open_path_button, 0, 0)
        lyt.addWidget(self.run_code_button, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)
        lyt.addWidget(self.list_widget_files, 1, 0)
        lyt.addLayout(vlyt, 1, 1)
        lyt.addLayout(hlyt, 2, 0)
        
    def set_fonts(self):
        font_code = QFont()
        font_code.setFamilies(["Consolas", "Courier New", "monospace"])
        font_code.setPointSize(16)
        font_code.setStyleHint(QFont.StyleHint.Monospace)

        font = QFont()
        font.setFamilies(["Consolas", "Courier New", "monospace"])
        font.setPointSize(12)
        font.setStyleHint(QFont.StyleHint.Monospace)

        self.plain_text_code.setFont(font_code)
        self.plain_text_terminal.setFont(font)
        self.list_widget_files.setFont(font)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj is self.plain_text_code:
            if event.key() == Qt.Key.Key_Tab and self.plain_text_code.hasFocus():
                # Special tab handling
                tc = self.plain_text_code.textCursor()
                tc.insertText("    ")
                return True
            else:
                return False
        return False
        
    def add_list_files(self):
        self.selected_path = QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        files = os.listdir(self.selected_path)

        files_list = []
        for file in files:
            if os.path.isfile(file):
                if file.find(".su") != -1:
                    files_list.append(file)

        self.list_widget_files.addItems(files_list)

        self.cmd = f"$-->{self.selected_path}> "
        self.plain_text_terminal.setPlainText(self.cmd)

    def open_selected_file(self):
        file = self.list_widget_files.currentItem()
        file = file.text()

        if os.path.isfile(file):
            self.selected_file_path = self.selected_path + "/" + file

            with open(self.selected_file_path, "r", encoding="utf-8") as su:
                su_data = su.read()
            
            su.close()

            self.plain_text_code.setPlainText(su_data)

    def create_new_file(self):
        created_file = QFileDialog.getSaveFileName(self, "Criar arquivo", dir=self.selected_path)

        i = created_file[0][::-1].find("/")
        file = created_file[0][::-1][:i][::-1]

        file_item = QListWidgetItem()
        file_item.setText(file)

        self.list_widget_files.addItem(file_item)
        self.list_widget_files.setCurrentItem(file_item)

        new_file = open(created_file[0], "w")
        new_file.close()

        self.open_selected_file()

    def save_file(self):
        data = self.plain_text_code.toPlainText()

        with open(self.selected_file_path, "w", encoding="utf-8") as su:
            su.write(data)
        su.close()

    def run_code(self):
        self.save_file()
        
        py_file_path = transform_in_py(self.selected_file_path)
         
        cmd = run_script(py_file_path)

        self.cmd = f"{self.cmd}\n$-->{self.selected_path}> runing::${self.selected_file_path}\n{cmd}\n$-->{self.selected_path}>"

        self.plain_text_terminal.setReadOnly(True)
        self.plain_text_terminal.setPlainText(self.cmd)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

    app.shutdown()
