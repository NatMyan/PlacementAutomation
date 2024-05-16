from GetData import getNetlistDetails
from ConfigDialog2 import ConfigDialog

import os
import json
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QFrame, QDialog, QHBoxLayout, QWidget, QLabel, QPushButton, QFileDialog
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QApplication, QComboBox, QLineEdit, QFormLayout
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QLineEdit, QPushButton, QSizePolicy


class StartMenu(QWidget):
    filesAccepted = Signal(str) 

    def __init__(self):
        super().__init__()
        self.initUI()
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
        
        layout = QVBoxLayout()
        
        self.btn_open_sp = QPushButton('Open SP File')
        self.btn_open_sp.setStyleSheet("background-color: #49495E; color: white;")
        self.btn_open_sp.clicked.connect(self.openSPFile)
        
        self.sp_label = QLabel("No .sp file open", self)
        self.sp_label.setStyleSheet("color: black;") 
        
        sp_vbox = QVBoxLayout()
        sp_vbox.addWidget(self.btn_open_sp, 0, Qt.AlignLeft | Qt.AlignTop)
        sp_vbox.addWidget(self.sp_label, 0, Qt.AlignLeft | Qt.AlignTop)
        
        self.btn_config_dialog = QPushButton('Open Configuration Dialog')
        self.btn_config_dialog.setStyleSheet("background-color: #796FB8; color: white;")
        self.btn_config_dialog.setEnabled(False)
        self.btn_config_dialog.clicked.connect(self.openConfigDialog)
        
        config_vbox = QVBoxLayout()
        config_vbox.addWidget(self.btn_config_dialog, 0, Qt.AlignLeft | Qt.AlignTop)
        
        hbox = QHBoxLayout()
        self.btn_ok = QPushButton('Ok', self)
        self.btn_ok.setEnabled(False)
        btn_cancel = QPushButton('Cancel', self)
        
        self.btn_ok.setStyleSheet("background-color: #796FB8; color: white;") 
        btn_cancel.setStyleSheet("background-color: #796FB8; color: white;")
        
        self.btn_ok.clicked.connect(self.acceptFiles)
        btn_cancel.clicked.connect(self.cancelSelections)
        
        hbox.addWidget(btn_cancel)
        hbox.addWidget(self.btn_ok)
        hbox.setAlignment(Qt.AlignRight)
        
        layout.addWidget(desc_label, 0, Qt.AlignTop)
        layout.addLayout(sp_vbox)
        layout.addLayout(config_vbox)
        layout.addLayout(hbox)
        
        self.setLayout(layout)
        
            
    def openSPFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open SP File", "", "SP Files (*.sp);;All Files (*)", options=options)
        if file_name:
            print(f"Selected SP file: {file_name}")
            self.sp_label.setText(f"Selected file: {file_name}")
            self._netlist = file_name
            self.netlist_map = getNetlistDetails(self._netlist)
            self.btn_config_dialog.setStyleSheet("background-color: #49495E; color: white;")
            # Here you can process the .sp file to extract component names
            self.btn_config_dialog.setEnabled(True)
            
            
    def cancelSelections(self):
        self.sp_label.setText("No .sp file open")
        self._netlist = None
        self.btn_config_dialog.setStyleSheet("background-color: #796FB8; color: white;")
        self.btn_config_dialog.setEnabled(False)
        

    def openConfigDialog(self):
        # print ("netliist map", self.netlist_map)
        self.dialog = ConfigDialog(self.netlist_map)
        data = self.dialog.getData()
        print ("dataaaaaaaaa", data)
        
        # json_size = os.stat("config_data_ic.json").st_size
        if not self.does_all_exist(data):
            open('config_data_ic.json', 'w').close()
            
        elif self.does_all_exist(data):
            self.btn_ok.setStyleSheet("background-color: #49495E; color: white;")
            self.btn_ok.setEnabled(True)
        self.dialog.exec_()
    
    
    def does_all_exist(self, data):
        return ("match_on_x" in data and "match_on_y" in data and "important_paths" in data and "size_unit" in data and 
                "min_diff_dist" in data and "gate_out_height" in data and "diff_side_width" in data and data["match_on_x"]
                and data["match_on_y"] and data["important_paths"] and data["size_unit"] and data["min_diff_dist"] and
                data["gate_out_height"] and data["diff_side_width"])
        
        
    def acceptFiles(self):
        if self._netlist:            
            print("Both files accepted!")
            self.filesAccepted.emit("Files accepted!")
            self.close()
        else:
            print("Please select both files")
            
    
    def getJson(self):
        json_file = self.dialog.getJson()
        return json_file
    
    
    def getNetlist(self):
        return self._netlist
        

