from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QFrame, QHBoxLayout, QWidget, QLabel, QPushButton, QFileDialog
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap, QFont


# TODO: add line edit to show which file, 
class StartMenu(QWidget):
    filesAccepted = Signal(str) 
    
    def __init__(self):
        super(StartMenu, self).__init__()
        self.initUI()
        # self.resize(self.sizeHint())
        self._json_file = None
        self._netlist = None
        
    def initUI(self):
        background_label = QLabel(self)
        pixmap = QPixmap('Untitled Project-24 3.jpg')    
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        self.setFixedSize(pixmap.width(), pixmap.height())
        
        desc_label = QLabel('Placement Automation', self)
        desc_font = QFont('Georgia', 50)
        desc_label.setFont(desc_font)
        desc_label.setStyleSheet("color: white;")
        # desc_label.setStyleSheet("color: #49495E;")
        
        btn_open_json = QPushButton('Open JSON File', self)
        btn_open_sp = QPushButton('Open SP File', self)
        
        btn_open_json.setStyleSheet("background-color: #49495E; color: white;")
        btn_open_sp.setStyleSheet("background-color: #49495E; color: white;")
        
        self.json_label = QLabel("No .json file open", self)
        self.sp_label = QLabel("No .sp file open", self)
        
        self.json_label.setStyleSheet("color: black;")
        self.sp_label.setStyleSheet("color: black;") 
        
        hbox = QHBoxLayout()
        self.btn_ok = QPushButton('Ok', self)
        btn_cancel = QPushButton('Cancel', self)
        
        self.btn_ok.setStyleSheet("background-color: #796FB8; color: white;") 
        btn_cancel.setStyleSheet("background-color: #796FB8; color: white;")
        
        btn_open_json.clicked.connect(self.openJsonFile)
        btn_open_sp.clicked.connect(self.openSpFile)
        self.btn_ok.clicked.connect(self.acceptFiles)
        btn_cancel.clicked.connect(self.cancelSelections)
        
        hbox.addWidget(btn_cancel)
        hbox.addWidget(self.btn_ok)
        hbox.setAlignment(Qt.AlignRight)
        
        json_vbox = QVBoxLayout()
        json_vbox.addWidget(btn_open_json, 0, Qt.AlignLeft | Qt.AlignTop)
        json_vbox.addWidget(self.json_label, 0, Qt.AlignLeft | Qt.AlignTop)
        
        sp_vbox = QVBoxLayout()
        sp_vbox.addWidget(btn_open_sp, 0, Qt.AlignLeft | Qt.AlignTop)
        sp_vbox.addWidget(self.sp_label, 0, Qt.AlignLeft | Qt.AlignTop)
        # sp_vbox.setSpacing(5)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(desc_label, 0, Qt.AlignTop)
        main_layout.addLayout(json_vbox)
        main_layout.addLayout(sp_vbox)
        main_layout.addLayout(hbox)
        
        
    def cancelSelections(self):
        self.sp_label.setText("No .sp file open")
        self.json_label.setText("No .json file open")
        self._json_file = None
        self._netlist = None
        self.btn_ok.setStyleSheet("background-color: #796FB8; color: white;") 
        
    
    def openJsonFile(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            print(f"Selected JSON file: {file_name}")
            self._json_file = file_name
            self.json_label.setText(f"Selected file: {file_name}")
            if self._netlist:
                self.btn_ok.setStyleSheet("background-color: #49495E; color: white;")


    def openSpFile(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open SP File", "", "SP Files (*.sp);;All Files (*)", options=options)
        if file_name:
            print(f"Selected SP file: {file_name}")
            self._netlist = file_name
            self.sp_label.setText(f"Selected file: {file_name}")
            if self._json_file:
                self.btn_ok.setStyleSheet("background-color: #49495E; color: white;")
       
       
    def acceptFiles(self):
        if self._json_file and self._netlist:            
            print("Both files accepted!")
            self.filesAccepted.emit("Files accepted!")
            self.close()
        else:
            print("Please select both files")   
        
        
    def getNetlist(self):
        return self._netlist
    
    
    def getJson(self):
        return self._json_file


'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QFont

class StartMenu(QWidget):
    def __init__(self):
        super(StartMenu, self).__init__()
        self.initUI()
        self._json_file = None
        self._netlist = None

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignCenter)

        desc_label = QLabel('Placement Automation', self)
        desc_font = QFont('Georgia', 36)
        desc_label.setFont(desc_font)

        btn_open_json = QPushButton('Open JSON File', self)
        btn_open_json.setStyleSheet("background-color: #49495E")
        btn_open_sp = QPushButton('Open SP File', self)
        btn_open_sp.setStyleSheet("background-color: #49495E")

        self.json_label = QLabel("No file open", self)
        self.sp_label = QLabel("No file open", self)

        hbox = QVBoxLayout(self)
        btn_ok = QPushButton('Ok', self)
        btn_cancel = QPushButton('Cancel', self)

        btn_open_json.clicked.connect(self.openJsonFile)
        btn_open_sp.clicked.connect(self.openSpFile)
        btn_ok.clicked.connect(self.acceptFiles)

        hbox.addWidget(btn_cancel)
        hbox.addWidget(btn_ok)
        hbox.setAlignment(Qt.AlignRight)

        json_vbox = QVBoxLayout()
        json_vbox.addWidget(btn_open_json, 0, Qt.AlignLeft | Qt.AlignTop)
        json_vbox.addWidget(self.json_label, 0, Qt.AlignLeft | Qt.AlignTop)

        sp_vbox = QVBoxLayout()
        sp_vbox.addWidget(btn_open_sp, 0, Qt.AlignLeft | Qt.AlignTop)
        sp_vbox.addWidget(self.sp_label, 0, Qt.AlignLeft | Qt.AlignTop)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(desc_label, 0, Qt.AlignTop)
        main_layout.addLayout(json_vbox)
        main_layout.addLayout(sp_vbox)
        main_layout.addLayout(hbox)

        # Connect the resize event to the method that adjusts the image size
        self.resizeEvent = self.on_resize

    def on_resize(self, event):
        # Calculate aspect ratio
        pixmap = self.background_label.pixmap()
        aspect_ratio = pixmap.width() / pixmap.height()

        # Set the size of the QLabel to fit the window
        self.background_label.setGeometry(0, 0, self.width(), int(self.width() / aspect_ratio))

    def openJsonFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            print(f"Selected JSON file: {file_name}")
            self._json_file = file_name
            self.json_label.setText(f"Selected file: {file_name}")

    def openSpFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open SP File", "", "SP Files (*.sp);;All Files (*)", options=options)
        if file_name:
            print(f"Selected SP file: {file_name}")
            self._netlist = file_name
            self.sp_label.setText(f"Selected file: {file_name}")

    def acceptFiles(self):
        if self._json_file and self._netlist:
            print("Both files accepted!")
        else:
            print("Please select both files")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    start_menu = StartMenu()
    start_menu.show()
    sys.exit(app.exec_())
'''
        
'''class StartMenu(QWidget):
    filesAccepted = Signal(str) 
    
    def __init__(self):
        super(StartMenu, self).__init__()
        self.initUI()
        self._json_file = None
        self._netlist = None

    def initUI(self):        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout(central_widget)
        
        hbox = QHBoxLayout()
        btn_ok = QPushButton('Ok', self)
        btn_cancel = QPushButton('Cancel', self)
        
        btn_open_json = QPushButton('Open JSON File', self)
        btn_open_sp = QPushButton('Open SP File', self)
        # btn_ok = QPushButton('Ok', self)
        
        btn_open_json.clicked.connect(self.openJsonFile)
        btn_open_sp.clicked.connect(self.openSpFile)
        btn_ok.clicked.connect(self.acceptFiles)
        
        hbox.addWidget(btn_cancel)
        hbox.addWidget(btn_ok)
        
        frame = QFrame()
        frame.setFixedSize(100,100)
        frame.setObjectName("StartWidget")
        frame.setStyleSheet("#StartWidget {background-color:red;}") 
        
        vbox.addWidget(frame)

        vbox.addWidget(btn_open_json)
        vbox.addWidget(btn_open_sp)
        vbox.addLayout(hbox)
        
        central_widget.setLayout(vbox)

        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('Open Files')

    def openJsonFile(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            print(f"Selected JSON file: {file_name}")
            self._json_file = file_name

    def openSpFile(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open SP File", "", "SP Files (*.sp);;All Files (*)", options=options)
        if file_name:
            print(f"Selected SP file: {file_name}")
            self._netlist = file_name
       
    def acceptFiles(self):
        if self._json_file and self._netlist:
            print("Both files accepted!")
            self.filesAccepted.emit("Files accepted!")
        else:
            print("Please select both files")   
        
    def getNetlist(self):
        return self._netlist
    
    def getJson(self):
        return self._json_file'''


'''def main():
    f = open("/dev/null", "w")
    os.dup2(f.fileno(), 2)
    f.close()

    # app = QApplication(sys.argv)
    app = QApplication(sys.argv)
    
    window = StartMenu()
    window.show()
    
    # file_name_netlist = 'two_stage_opamp_ac_deck.sp'
    # file_name_json = 'two_stage_opamp_constraints.json'
    
    file_name_netlist = window.getNetlist()
    file_name_json = window.getJson()

    netlist_details = getNetlistDetails(file_name_netlist)
    json_details = getJSONDetails(file_name_json)

    component_generator = ComponentGeneration()
    component_generator.generate_coordinates(netlist_details, json_details)
    components = component_generator.get_components()
    
    global_placement = GlobalPlacement(components)
    global_placement_list = global_placement.sort_and_sweep(json_details)

    if global_placement_list:
        for component in global_placement_list:
            print(f"{component.name}: top left: ({component.rectangle.x1}, {component.rectangle.y1}); bottom right: ({component.rectangle.x2}, {component.rectangle.y2})")
    
    window1 = RectanglesWidget(global_placement_list)
    if global_placement_list:
        window1.setGeometry(0, 0, 10000, 10000)  # Set the window geometry
        window1.setWindowTitle('Phase 2')
        window1.show()
    
    validator = PlacementValidator()
    if global_placement_list and json_details:
        print(validator.isPlacementValid(global_placement_list, json_details))
        print("\n")

    if global_placement_list and json_details:
        minimizer = MinimizePlacement(global_placement_list, json_details)
        final_placement_list = minimizer.minimize()
        
        if final_placement_list:
            for component in final_placement_list:
                print(f"{component.name}: top left: ({component.rectangle.x1}, {component.rectangle.y1}); bottom right: ({component.rectangle.x2}, {component.rectangle.y2})")

            print(validator.isPlacementValid(final_placement_list, json_details))
    
            window2 = RectanglesWidget(final_placement_list)
            window2.setGeometry(0, 0, 10000, 10000)  # Set the window geometry
            window2.setWindowTitle('Phase 3')
            window2.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
'''

'''def main():
    app = QApplication(sys.argv)
    window = StartMenu()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()'''

'''import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Python Menus & Toolbars")
        self.resize(400, 200)
        self.centralWidget = QLabel("Hello, World")
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)

    def _createMenuBar(self):
        menuBar = self.menuBar()    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
'''

'''import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QFileDialog

class FileViewer(QMainWindow):
    def __init__(self):
        super(FileViewer, self).__init__()

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        openFile1 = QAction('Open File 1', self)
        openFile1.triggered.connect(self.showDialogFile1)
        fileMenu.addAction(openFile1)

        openFile2 = QAction('Open File 2', self)
        openFile2.triggered.connect(self.showDialogFile2)
        fileMenu.addAction(openFile2)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('File Viewer')

    def showDialogFile1(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open File 1', '', 'Text files (*.txt);;All Files (*)')
        if fname:
            print(f"File 1 opened: {fname}")

    def showDialogFile2(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open File 2', '', 'Text files (*.txt);;All Files (*)')
        if fname:
            print(f"File 2 opened: {fname}")

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QFileDialog


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()

        self.initUI()

    def initUI(self):
        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        vbox = QVBoxLayout(central_widget)

        # Create a button
        btn = QPushButton('Click me!', self)
        btn.clicked.connect(self.onButtonClick)

        # Add the button to the layout
        vbox.addWidget(btn)

        # Set the layout for the central widget
        central_widget.setLayout(vbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PyQt5 Example')

    def onButtonClick(self):
        QMessageBox.information(self, 'Message', 'Button clicked!')



def main():
    f = open("/dev/null", "w")
    os.dup2(f.fileno(), 2)
    f.close()

    app = QApplication(sys.argv)
    viewer = FileViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()'''