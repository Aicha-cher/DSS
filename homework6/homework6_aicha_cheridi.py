import sys # System-specific parameters and functions

from PyQt6.QtWidgets import (QApplication, QPushButton, QWidget,QMainWindow,
                             QFileDialog, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QMenu)

import pyqtgraph as pg
import json
import imageio.v2 as io
from PyQt6.QtGui import  QAction
from PyQt6.QtCore import  Qt

# Preparing the environment for the image:
class Interface(QWidget):
    def __init__(self):
        super().__init__() #super() is used to refer the superclass from the subclass.

        # Initialize a QGridLayout
        self.l = QGridLayout(self)
        # Create an ImageView inside the central widget
        self.imv = pg.ImageView()
        self.l.addWidget(self.imv)
        
        

#Let's define our widget
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        ## Run the function to set defaults
        self.set_defaults()

        # Creating a CentralWidget
        w = QWidget(self)
        self.setCentralWidget(w) # QMainWindow takes ownership of the widget pointer and deletes it at the appropriate time.
        self.setAcceptDrops(True)
        self.mainLayout = QVBoxLayout()
        w.setLayout(self.mainLayout)


        # setting the minimum size
        self.setMinimumSize(250, 300) #images of 256x256+space for buttons
        # self.setMaximumSize(1920, 1080)
        ####------- Menu -------####

        self.menu = self.menuBar()
        self.menu.setNativeMenuBar(False)
        file_menu = self.menu.addMenu("&File")
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open)
        save_action = QAction("Save", self)
        save_action.setShortcut('ctrl+s')
        save_action.triggered.connect(self.save)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
    
        
        ####------- IMAGE WIDGET -------####
        self.imageViewer = Interface()
        self.mainLayout.addWidget(self.imageViewer)


    
        ####------- Make the layout look better -------####
        # self.mainLayout.addStretch(1)


    def updateMainDD(self,index): # update language
        self.indexLanguage = index # define a global variable saving the index of the selected option
        self.language = self.availableLangs[self.indexLanguage] # define a variable containing the language of the given index
        self.setWindowTitle(self.options["available languages"][self.language]["window title"]) # Update the window title w.r.t the language selected
        self.openButton.setText(self.options["available languages"][self.language]["button"]) # Update the text of the button

    


    def set_defaults(self): ## Set default values for the application
        # Settings for the window:
        self.status = self.statusBar()
        # self.showNormal() # Shows the window maximized
        self.setAcceptDrops(True) #enables drop events

        # Initialize the variable containing the image 
        self.im = None 


        ## Load the settings from the json file
        with open ("settings.json", "r") as jsonfile:
            self.options = json.load(jsonfile)

        ## Set window options (width, height)
        width = self.options["defaults"]["width"]
        height = self.options["defaults"]["height"]
        self.resize(width, height)

        # Settings with language
        ## Store the available languages, the default language and select the index of the default language
        self.availableLangs = list(self.options["available languages"].keys()) # list: [english, deutsch]
        self.language = self.options["defaults"]["language"] ## english / deutsch
        self.indexLanguage = self.availableLangs.index(self.language)

        ## Change the window title depending on the default language
        self.setWindowTitle(self.options["available languages"][self.language]["window title"])


        
    ####----CLEAR WIDGETS----#### Think a way to clear properly!
    ### Clear items inside a Layout
    def clearItems(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearItems(item.layout())
    
    ### Clear layouts inside layouts 
    def clearLayouts(self, layout):
        self.clearItems(layout)
        for i in reversed (range(layout.count())):
            layout_item = layout.itemAt(i)
            self.clearItems(layout_item.layout())
            layout.removeItem(layout_item)

    ## Function to open and load an image
    def open(self):
        fn, _ = QFileDialog.getOpenFileName(filter="*.png *.jpg")

        if fn:
            self.status.showMessage(fn)
            self.im = io.imread(fn)
            self.imageViewer.imv.setImage(self.im)
            QMessageBox.information(self, 
            "file loaded", 
            "Image succesfully loaded!")
        else: 
            QMessageBox.critical(self, 
            "Meaningful error", 
            "Something went wrong!")
    
    def save(self):
        fn, _ = QFileDialog.getSaveFileName(filter="*.png *.jpg")
        
        if fn:
            io.imwrite(fn, self.im)
            QMessageBox.information(self, 
            "file saved", 
            "Image succesfully saved!")
        else: 
            QMessageBox.critical(self, 
            "saving error", 
            "Something went wrong!")

    # drag and drop
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
    def dragMoveEvent(self,  event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.DropAction.CopyAction)
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.im = io.imread(self.file_path)
            self.imageViewer.imv.setImage(self.im)
            event.accept()
        else:
            event.ignore()

        
def main():

    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()