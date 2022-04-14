from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QFileDialog, QVBoxLayout, QPlainTextEdit, QPushButton, QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator

# Create the main app class inheriting from QMainWindow

class Window(QMainWindow):
    #Add a constructor extending the parent window
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('PyQt5 Lab')
        self.createMenu()
        self.createTabs()
        self.fileName = None
        
    
    # Method adding the menu panel
    def createMenu(self):
        # Create a menu bar
        self.menu = self.menuBar()

        self.createFileMenu()
        self.createTask1Menu()
        self.createTask2Menu()
        self.createTask3Menu()


    def createTask1Menu(self):
        self.task1Menu = self.menu.addMenu("Task 1")
        self.task1Menu.addAction('Open image file', self.openImageFile)
        # Extend the file menu with exit position


    def createTask2Menu(self):
        self.task2Menu = self.menu.addMenu("Task 2")
        self.task2Menu.addAction('Clear', self.clearNotepadContent)
        self.task2Menu.addAction('Open', self.openTextFile)
        self.task2Menu.addAction('Save', self.saveNotepadContent)
        self.task2Menu.addAction('Save as', self.saveNotepadContent)

    def createTask3Menu(self):
        self.task3Menu = self.menu.addMenu("Task 3")
        self.task3Menu.addAction('Clear', self.clearTextFields)

    def openImageFile(self):
        # Create a file open dialog, returning the path to the choosen file
        fileName, _ = QFileDialog.getOpenFileName(self.tab_1, "Select an image file",  "Initial file name", "All Files (*);;Python Files (*.py);; PNG (*.png)")
        
        # If a file has been choosen, display the image using QPixmap
        if fileName:
            label = QLabel(self.tab_1)
            pixmap = QPixmap(fileName)
            label.setPixmap(pixmap)
            self.tab_1.layout = QVBoxLayout(self) 
            self.tab_1.resize(pixmap.width(),pixmap.height())
            self.tab_1.layout.addWidget(label)
            self.tab_1.setLayout(self.tab_1.layout)

    def openTextFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.tab_2, "Select an image file",  "Initial file name", "All Files (*);;Python Files (*.py);; TXT (*.txt)")
        
        fileContent = open(fileName).read()
        self.editText.setPlainText(fileContent)

    def clearNotepadContent(self):
        self.editText.setPlainText("")
        self.editText.setFocus()


    def saveNotepadContent(self):
        if self.fileName is None:
            self.fileName, _ = QFileDialog.getSaveFileName(self, "Save File")

        if self.fileName:
            file =open(self.fileName, "w")
            file.write(self.editText.toPlainText())
            file.close()

    def saveAs(self):
        self.fileName = None
        self.saveNotepadContent()
        

    def createFileMenu(self):
        # Add a drop-down list of the name File
        self.fileMenu = self.menu.addMenu("File")
        self.fileMenu.addAction('Exit', self.close)

    def secondTabContent(self):
        self.editText = QPlainTextEdit()
        self.tab_2.layout = QVBoxLayout()
        openFileBtn = QPushButton("Open text file")
        openFileBtn.clicked.connect(self.openTextFile)
        self.tab_2.layout.addWidget(openFileBtn)
        self.tab_2.layout.addWidget(self.editText)
        clearContentBtn = QPushButton("Clear content")
        clearContentBtn.clicked.connect(self.clearNotepadContent)
        saveContentBtn = QPushButton("Save content")
        saveContentBtn.clicked.connect(self.saveNotepadContent)
        self.tab_2.layout.addWidget(clearContentBtn)
        self.tab_2.layout.addWidget(saveContentBtn)
        self.tab_2.setLayout(self.tab_2.layout)

    def thirdTabContent(self):
        self.tab_3.layout = QVBoxLayout()

        self.fieldA = QLineEdit()
        self.fieldB = QLineEdit()
        self.fieldC = QLineEdit()
        self.fieldC.setValidator(QIntValidator())
        self.sumField = QLineEdit()
        self.sumField.setDisabled(True)
        self.fieldA.textChanged.connect(self.joinFields)
        self.fieldB.textChanged.connect(self.joinFields)
        self.fieldC.textChanged.connect(self.joinFields)
        
        self.tab_3.layout.addWidget(QLabel("Field A:"))
        self.tab_3.layout.addWidget(self.fieldA)
        self.tab_3.layout.addWidget(QLabel("Field B:"))
        self.tab_3.layout.addWidget(self.fieldB)
        self.tab_3.layout.addWidget(QLabel("Field C:"))
        self.tab_3.layout.addWidget(self.fieldC)
        self.tab_3.layout.addWidget(QLabel("Field A + B + C:"))
        self.tab_3.layout.addWidget(self.sumField)

        self.tab_3.setLayout(self.tab_3.layout)

    def clearTextFields(self):
        self.fieldA.setText("")
        self.fieldB.setText("")
        self.fieldC.setText("")


    def joinFields(self):
        self.sumField.setText(self.fieldA.text() + self.fieldB.text() + self.fieldC.text())
    
    # Method adds an internal widget to the window
    def createTabs(self):
        # Create a tab widget
        self.tabs = QTabWidget()
        
        # Create seperate widgets for tabs
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()
        
        # Add tabs to the tab widget
        self.tabs.addTab(self.tab_1, "Task 1")        
        self.tabs.addTab(self.tab_2, "Task 2")        
        self.tabs.addTab(self.tab_3, "Task 3")

        self.secondTabContent()
        self.thirdTabContent()
        
        # Attach the widget to the main window as central widget
        self.setCentralWidget(self.tabs)


# Run the window
app = QApplication([])
win = Window()
win.show()
app.exec_()

