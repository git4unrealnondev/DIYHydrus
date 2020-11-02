'''
qt5.py Is a GUI Handler.
'''

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

class qt5(QWidget):
    '''
    Main manager for QT5
    '''
    def __init__(self):
        '''
        Creates QT5 Application
        '''
        self.app = QApplication([])
        #self.app.setWindowTitle("Charting Software")
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, Qt.red)
        self.app.setPalette(palette)
        
        screenx, screeny = self.get_screen_size()
        self.draw_hbox(True, 0, 0, screenx, screeny)
        
        
        self.app.exec()
        
    def get_screen_size(self):
        self.screen = self.app.primaryScreen()
        rect = self.screen.availableGeometry()
        return rect.width(), rect.height()
        
    def draw_hbox(self, stretch, x, y, endx, endy):
        hbox = QHBoxLayout()

        if stretch:
            hbox.addStretch(1)

        self.app.addLayout(hbox)
        hbox.setGeometry(x , y, endx, endy)
        hbox.show()
