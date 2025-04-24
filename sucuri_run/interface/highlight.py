from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor

from ..core.sintaxe import a_palavras_reservadas, r_palavras_reservadas, funcoes, operadores

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
        #self.blue.setFontWeight(QFont.Bold)
        self.blue_w = a_palavras_reservadas.keys()

        self.purlple = QTextCharFormat()
        self.purlple.setForeground(QColor("magenta"))
        #self.purlple.setFontWeight(QFont.Bold)
        self.purlple_w = r_palavras_reservadas.keys()

        self.yellow = QTextCharFormat()
        self.yellow.setForeground(QColor("yellow"))
        #self.yellow.setFontWeight(QFont.Bold)
        self.yellow_w = list(funcoes.keys())
        
        self.op = QTextCharFormat()
        self.op.setForeground(QColor("darkGreen"))
        #self.op.setFontWeight(QFont.Bold)
        self.op_w = operadores