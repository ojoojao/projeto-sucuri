import sys, os
from sintaxe import a_palavras_reservadas, r_palavras_reservadas, funcoes
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PySide6.QtWidgets import QApplication,  QWidget, QPushButton, QPlainTextEdit, QGridLayout, QListWidget, QFileDialog, QHBoxLayout, QListWidgetItem

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        
        self.words()

    def highlightBlock(self, text):
        for keyword in self.blue_w:
            index = text.find(keyword)
            while index >= 0:
                length = len(keyword)
                self.setFormat(index, length, self.blue)
                index = text.find(keyword, index + length)

        for keyword in self.purlple_w:
            index = text.find(keyword)
            while index >= 0:
                length = len(keyword)
                self.setFormat(index, length, self.purlple)
                index = text.find(keyword, index + length)
        
        for keyword in self.yellow_w:
            index = text.find(keyword)
            while index >= 0:
                length = len(keyword)
                self.setFormat(index, length, self.yellow)
                index = text.find(keyword, index + length)
    
    def words(self):
        self.blue = QTextCharFormat()
        self.blue.setForeground(QColor("darkCyan"))
        self.blue.setFontWeight(QFont.Bold)
        self.blue_w = a_palavras_reservadas.keys()

        self.purlple = QTextCharFormat()
        self.purlple.setForeground(QColor("magenta"))
        self.purlple.setFontWeight(QFont.Bold)
        self.purlple_w = r_palavras_reservadas.keys()

        self.yellow = QTextCharFormat()
        self.yellow.setForeground(QColor("yellow"))
        self.yellow.setFontWeight(QFont.Bold)
        self.yellow_w = list(funcoes.keys())
        self.yellow_w.append("[")
        self.yellow_w.append("]")
        self.yellow_w.append("{")
        self.yellow_w.append("}")
        self.yellow_w.append("(")
        self.yellow_w.append(")")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor de Texto")

        self.widgets()
        self.config_widgets()
        self.set_layout() 

    def widgets(self):
        self.plain_text = QPlainTextEdit()

        self.list_widget = QListWidget()

        self.save_file_button = QPushButton()

        self.open_path_button = QPushButton()

        self.create_file_button = QPushButton()

    def config_widgets(self):
        self.plain_text.setMinimumWidth(500)
        self.plain_text.setMinimumHeight(500)
        self.plain_text.installEventFilter(self)
        PythonHighlighter(self.plain_text.document())

        self.list_widget.setMaximumWidth(200)
        self.list_widget.clicked.connect(self.open_file) 

        self.open_path_button.setText("Abri pasta")
        self.open_path_button.clicked.connect(self.list_files)

        self.save_file_button.setText("Salvar")
        
        self.create_file_button.setText("Novo")
        self.create_file_button.clicked.connect(self.novo)

    def set_layout(self):
        lyt = QGridLayout()
        self.setLayout(lyt)

        hlyt = QHBoxLayout()
        hlyt.addWidget(self.create_file_button)
        hlyt.addWidget(self.save_file_button)

        lyt.addWidget(self.open_path_button, 0, 0)
        lyt.addWidget(self.list_widget, 1, 0)
        lyt.addLayout(hlyt, 2, 0)
        lyt.addWidget(self.plain_text, 1, 1)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj is self.plain_text:
            if event.key() == Qt.Key.Key_Tab and self.plain_text.hasFocus():
                # Special tab handling
                tc = self.plain_text.textCursor()
                tc.insertText("    ")
                return True
            else:
                return False
        return False
        
    def list_files(self):
        self.selected_path = QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        self.files = os.listdir(self.selected_path)

        self.list_widget.addItems(self.files)

    def open_file(self):
        file = self.list_widget.currentItem()
        file = file.text()

        if os.path.isfile(file):
            self.file_path = self.selected_path+"\\"+file
            with open(self.file_path, "r", encoding="utf-8") as su:
                su_data = su.readlines()
                print(su_data)
            su.close()

    def novo(self):
        created_file = QFileDialog.getSaveFileName(self, "Criar arquivo")
        self.file_path = created_file[0]

        i = self.file_path[::-1].find("/")
        file = self.file_path[::-1][:i][::-1]

        i = self.file_path.find(file)
        path = self.file_path[:i]

        file_item = QListWidgetItem()
        file_item.setText(file)

        self.list_widget.addItem(file_item)
        self.list_widget.setCurrentItem(file_item)

        new_file = open(self.file_path, "w")
        new_file.close()

        self.open_file()



    def save(self):
        pass

        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

    app.shutdown()
