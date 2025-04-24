import sys, os, subprocess
from sintaxe import a_palavras_reservadas, r_palavras_reservadas, funcoes, operadores
from PySide6.QtCore import Qt, QEvent, QSize
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PySide6.QtWidgets import QApplication,  QWidget, QPushButton, QPlainTextEdit, QGridLayout, QListWidget, QFileDialog, QHBoxLayout, QVBoxLayout, QListWidgetItem, QTextEdit

def transform_in_py(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as suc:
        t = suc.readlines()
    suc.close()

    lines = []
    for i, l in enumerate(t):
        lines.append(l)

        for k in a_palavras_reservadas.keys():
            if k in lines[i]:
                lines[i] = str(lines[i]).replace(k, a_palavras_reservadas[k])
        
        for k in r_palavras_reservadas.keys():
            if k in lines[i]:
                lines[i] = str(lines[i]).replace(k, r_palavras_reservadas[k])
        
        for k in funcoes.keys():
            if k in lines[i]:
                lines[i] = str(lines[i]).replace(k, funcoes[k])

    text = ""
    for l in lines:
        text += l
    
    i = file_path[::-1].find("/")
    file = file_path[::-1][:i][::-1]
    i = file_path.find(file)
    path = file_path[:i]
    path = path + "run_files/"
    
    file = file.replace(".su", ".py")

    file_path = path + file

    if not os.path.exists(path):
        os.makedirs(path)  
        os.system(f'attrib +h "{path[:-1]}"') 

    with open(file_path, 'w', encoding='utf-8') as py:
        py.write(text)
    py.close()
    
    return file_path

def py_cmd_to_su(cmd_text: str):   
    t = cmd_text.splitlines()

    lines = []
    for i, l in enumerate(t):
        lines.append(l)

        for k in a_palavras_reservadas.keys():
            if a_palavras_reservadas[k] in lines[i]:
                lines[i] = str(lines[i]).replace(a_palavras_reservadas[k], k)
        
        for k in r_palavras_reservadas.keys():
            if r_palavras_reservadas[k] in lines[i]:
                lines[i] = str(lines[i]).replace(r_palavras_reservadas[k], k)
        
        for k in funcoes.keys():
            if funcoes[k] in lines[i]:
                lines[i] = str(lines[i]).replace(funcoes[k], k)

    text = ""
    for l in lines:
        text += l + "\n"

    return text

def run_script(file_path):
    command = f"python {file_path}" # Replace your_script.py with the actual script name.
    process = subprocess.run(command, capture_output=True, text=True, shell=True, encoding="utf-8")

    output = process.stdout
    error = process.stderr

    if process.returncode == 0:
        print("Command executed successfully:")
        print(output)

        su_output = py_cmd_to_su(output)
        return su_output
    else:
        print(f"Command failed with error code {process.returncode}:")
        print(error)
        return f"Erro ao executar arquivo... {output}"

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

        for keyword in self.op_w:
            index = text.find(keyword)
            while index >= 0:
                length = len(keyword)
                self.setFormat(index, length, self.op)
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
        
        self.op = QTextCharFormat()
        self.op.setForeground(QColor("darkGreen"))
        self.op.setFontWeight(QFont.Bold)
        self.op_w = operadores

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

        self.terminal = QPlainTextEdit()

        self.run_code_button = QPushButton()

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

        self.terminal.setMaximumHeight(250)
        self.terminal.setReadOnly(True)

        self.run_code_button.setMaximumWidth(100)
        self.run_code_button.setText("Rodar")
        self.run_code_button.clicked.connect(self.run_code)

        self.open_path_button.setText("Abri pasta")
        self.open_path_button.clicked.connect(self.list_files)

        self.save_file_button.setText("Salvar")
        self.save_file_button.setMaximumWidth(200)
        self.save_file_button.clicked.connect(self.save)
        
        self.create_file_button.setText("Novo")
        self.create_file_button.setMaximumWidth(200)
        self.create_file_button.clicked.connect(self.novo)

    def set_layout(self):
        lyt = QGridLayout()
        self.setLayout(lyt)

        hlyt = QHBoxLayout()
        hlyt.addWidget(self.create_file_button)
        hlyt.addWidget(self.save_file_button)
        
        vlyt = QVBoxLayout()
        vlyt.addWidget(self.plain_text)
        vlyt.addWidget(self.terminal)

        lyt.addWidget(self.open_path_button, 0, 0)
        lyt.addWidget(self.run_code_button, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)
        lyt.addWidget(self.list_widget, 1, 0)
        lyt.addLayout(vlyt, 1, 1)
        lyt.addLayout(hlyt, 2, 0)
        

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
        files = os.listdir(self.selected_path)

        files_list = []
        for file in files:
            if os.path.isfile(file):
                if file.find(".su") != -1:
                    files_list.append(file)

        self.list_widget.addItems(files_list)

    def open_file(self):
        file = self.list_widget.currentItem()
        file = file.text()

        if os.path.isfile(file):
            self.file_path = self.selected_path+"/"+file
            with open(self.file_path, "r", encoding="utf-8") as su:
                su_data = su.read()
                print(su_data)
            su.close()

            self.plain_text.setPlainText(su_data)

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
        file = self.list_widget.currentItem()
        file = file.text()

        if os.path.isfile(file):
            data = self.plain_text.toPlainText()

            self.file_path = self.selected_path+"/"+file
            with open(self.file_path, "w", encoding="utf-8") as su:
                su.write(data)

        transform_in_py(self.file_path)

    def run_code(self):
        file = self.list_widget.currentItem()
        file = file.text()
        file = file.replace(".su", ".py")

        self.save()

        file_path = self.selected_path+"/run_files/"+file
        print(file_path)
        cmd = run_script(file_path)

        self.terminal.setPlainText(cmd)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

    app.shutdown()
