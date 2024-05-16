# pls don't look at this code, it's a bit too bad lol

import json
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QFrame, QDialog, QHBoxLayout, QWidget, QLabel, QPushButton, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QComboBox, QLineEdit, QFormLayout
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QLineEdit, QPushButton, QSizePolicy


class ConfigDialog(QDialog):
    def __init__(self, netlist_map):
        super().__init__()
        if netlist_map:
            self.netlist_map = netlist_map
            self.data = self.load_json_to_python("config_data_ic.json")
            print("data is", self.data)
            if not self.is_valid(self.data):
                open('config_data_ic.json', 'w').close()
                self.data = {}
            self.initUI()
            

    def initUI(self):
        pal = self.palette()
        pal.setColor(self.backgroundRole(), "#9cccfb")
        self.setPalette(pal)
       
        layout = QVBoxLayout()
        
        self.form_layout = QFormLayout()
        
        self.combo_boxes_x = []
        self.combo_boxes_y = []
        self.combo_boxes_i = []
        
        # Size Unit
        self.size_unit_lineedit = QLineEdit()
        self.size_unit_label = QLabel("Size Unit:", self)
        self.size_unit_label.setStyleSheet("color: black;") 
        self.form_layout.addRow(self.size_unit_label, self.size_unit_lineedit)
        
        # Min Diff Dist
        self.min_diff_dist_lineedit = QLineEdit()
        self.min_diff_dist_label = QLabel("Min Diff Dist:", self)
        self.min_diff_dist_label.setStyleSheet("color: black;") 
        self.form_layout.addRow(self.min_diff_dist_label, self.min_diff_dist_lineedit)
        
        # Gate Out Height
        self.gate_out_height_lineedit = QLineEdit()
        self.gate_out_height_label = QLabel("Gate Out Height:", self)
        self.gate_out_height_label.setStyleSheet("color: black;") 
        self.form_layout.addRow(self.gate_out_height_label, self.gate_out_height_lineedit)
        
        # Diff Side Width
        self.diff_side_width_lineedit = QLineEdit()
        self.diff_side_width_label = QLabel("Diff Side Width:", self)
        self.diff_side_width_label.setStyleSheet("color: black;") 
        self.form_layout.addRow(self.diff_side_width_label, self.diff_side_width_lineedit)
        
        # Set data in QLineEdit widgets
        if "size_unit" in self.data and self.data["size_unit"]:
            self.size_unit_lineedit.setText(self.data["size_unit"])
            
        if "min_diff_dist" in self.data and self.data["min_diff_dist"]:
            self.min_diff_dist_lineedit.setText(self.data["min_diff_dist"])
            
        if "gate_out_height" in self.data and self.data["gate_out_height"]:
            self.gate_out_height_lineedit.setText(self.data["gate_out_height"])
            
        if "diff_side_width" in self.data and self.data["diff_side_width"]:
            self.diff_side_width_lineedit.setText(self.data["diff_side_width"])
        
        # layout.addLayout(self.form_layout)
        
        # Initialize combo boxes and add pair buttons
        self.addPairComboBoxesX()
        self.addPairComboBoxesY()
        self.addPairComboBoxesI()
        
        if "match_on_x" in self.data and self.data["match_on_x"]:
            self.setComboBoxItems(self.combo_boxes_x, self.data, "match_on_x")
            
        if "match_on_y" in self.data and self.data["match_on_y"]:
            self.setComboBoxItems(self.combo_boxes_y, self.data, "match_on_y")
            
        if "important_paths" in self.data and self.data["important_paths"]:
            self.setComboPathItems(self.combo_boxes_i, self.data, "important_paths")
        
        layout.addLayout(self.form_layout)
        
        # OK and Cancel buttons
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("background-color: #796FB8; color: white;")
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("background-color: #796FB8; color: white;")
        
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("background-color: #796FB8; color: white;")
        
        ok_button.clicked.connect(self.onOKClicked)
        cancel_button.clicked.connect(self.onCancelClicked)
        clear_button.clicked.connect(self.onClearClicked)
        
        hbox = QHBoxLayout()
        hbox.addWidget(cancel_button)
        hbox.addWidget(ok_button)
        hbox.addWidget(clear_button)
        hbox.setAlignment(Qt.AlignRight)
        layout.addLayout(hbox)

        self.setLayout(layout)
        
        
    def setComboBoxItems(self, combo_boxes, data, key):
        existing_paths = set()
        for pair in data[key]:
            left_comp, right_comp = pair
            
            if (left_comp, right_comp) in existing_paths:
                continue
            if not left_comp or not right_comp:
                continue
            
            if not combo_boxes or len(combo_boxes) > 1:
                # Create new combo boxes if combo_boxes is empty
                combo_box_left = QComboBox()
                combo_box_right = QComboBox()
                for comp_name in self.netlist_map:
                    combo_box_left.addItem(comp_name)
                    combo_box_right.addItem(comp_name)
                # Add new combo boxes to the layout
                row_layout = QHBoxLayout()
                row_layout.addWidget(combo_box_left)
                row_layout.addWidget(combo_box_right)
                
                if key == "match_on_x":
                    match_on_label = QLabel("Match on X:", self)
                    combo_box_left.setStyleSheet("background-color: #2f3760; color: white;")
                    combo_box_right.setStyleSheet("background-color: #2f3760; color: white;")
                    
                elif key == "match_on_y":
                    match_on_label = QLabel("Match on Y:", self)
                    combo_box_left.setStyleSheet("background-color: #4f3869; color: white;")
                    combo_box_right.setStyleSheet("background-color: #4f3869; color: white;")
                    
                match_on_label.setStyleSheet("color: black;")
                combo_box_left.setMinimumWidth(80)  # Set minimum width
                combo_box_left.setMinimumHeight(20)  # Set minimum height
                combo_box_right.setMinimumWidth(80)  # Set minimum width
                combo_box_right.setMinimumHeight(20)  # Set minimum height
                self.form_layout.addRow(match_on_label, row_layout)
                
            elif len(combo_boxes) == 1:
                # Reuse existing combo boxes
                combo_box_left, combo_box_right = combo_boxes[0]  # Get the 1st pair of combo boxes
            
            # Set the current index based on the data
            left_index = combo_box_left.findText(left_comp)
            right_index = combo_box_right.findText(right_comp)
            combo_box_left.setCurrentIndex(left_index)
            combo_box_right.setCurrentIndex(right_index)
            
            # Append the combo boxes back to the combo_boxes list
            combo_boxes.append((combo_box_left, combo_box_right))
            existing_paths.add((left_comp, right_comp))
            
            
    def setComboPathItems(self, combo_boxes, data, key):
        existing_paths = set()
        for path in data[key]:
            left_comp, mid_comp, right_comp = path
            
            if (left_comp, mid_comp, right_comp) in existing_paths:
                continue
            if not left_comp or not mid_comp or not right_comp:
                continue
            
            if not combo_boxes or len(combo_boxes) > 1:
                # Create new combo boxes if combo_boxes is empty
                combo_box_left = QComboBox()
                combo_box_mid = QComboBox()
                combo_box_right = QComboBox()
                for comp_name in self.netlist_map:
                    combo_box_left.addItem(comp_name)
                    combo_box_mid.addItem(comp_name)
                    combo_box_right.addItem(comp_name)
                # Add new combo boxes to the layout
                row_layout = QHBoxLayout()
                row_layout.addWidget(combo_box_left)
                row_layout.addWidget(combo_box_mid)
                row_layout.addWidget(combo_box_right)
                
                if key == "important_paths":
                    match_on_label = QLabel("Important Paths:", self)
                    combo_box_left.setStyleSheet("background-color: #384f69; color: white;")
                    combo_box_mid.setStyleSheet("background-color: #384f69; color: white;")
                    combo_box_right.setStyleSheet("background-color: #384f69; color: white;")
                    
                match_on_label.setStyleSheet("color: black;")
                
                combo_box_left.setMinimumWidth(80)  # Set minimum width
                combo_box_left.setMinimumHeight(20)  # Set minimum height
                combo_box_mid.setMinimumWidth(80)  # Set minimum width
                combo_box_mid.setMinimumHeight(20)  # Set minimum height
                combo_box_right.setMinimumWidth(80)  # Set minimum width
                combo_box_right.setMinimumHeight(20)  # Set minimum height
                self.form_layout.addRow(match_on_label, row_layout)
                
            elif len(combo_boxes) == 1:
                # Reuse existing combo boxes
                combo_box_left, combo_box_mid, combo_box_right = combo_boxes[0]  # Get the 1st pair of combo boxes
                
            # Set the current index based on the data
            left_index = combo_box_left.findText(left_comp)
            mid_index = combo_box_mid.findText(mid_comp)
            right_index = combo_box_right.findText(right_comp)
            combo_box_left.setCurrentIndex(left_index)
            combo_box_mid.setCurrentIndex(mid_index)
            combo_box_right.setCurrentIndex(right_index)
            # Append the combo boxes back to the combo_boxes list
            combo_boxes.append((combo_box_left, combo_box_mid, combo_box_right))
            existing_paths.add((left_comp, mid_comp, right_comp))


    def addPairComboBoxesX(self):        
        combo_box_x_left = QComboBox()
        combo_box_x_right = QComboBox()
        
        combo_box_x_left.setStyleSheet("background-color: #2f3760; color: white;")
        combo_box_x_right.setStyleSheet("background-color: #2f3760; color: white;")
        
        combo_box_x_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Adjust the size policy
        combo_box_x_left.setMinimumWidth(80)  # Set minimum width
        combo_box_x_left.setMinimumHeight(20)  # Set minimum height
        
        combo_box_x_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Adjust the size policy
        combo_box_x_right.setMinimumWidth(80)  # Set minimum width
        combo_box_x_right.setMinimumHeight(20)  # Set minimum height
        
        combo_box_x_left.addItem("-")
        combo_box_x_right.addItem("-")
        
        for comp_name in self.netlist_map:
            combo_box_x_left.addItem(comp_name)
            combo_box_x_right.addItem(comp_name)
        
        self.combo_boxes_x.append((combo_box_x_left, combo_box_x_right))
                
        row_layout_x = QHBoxLayout()
        row_layout_x.addWidget(combo_box_x_left)
        row_layout_x.addWidget(combo_box_x_right)
        match_on_x_label = QLabel("Match on X:", self)
        match_on_x_label.setStyleSheet("color: black;") 
        
        if not hasattr(self, 'add_pair_button_x'):
            self.add_pair_button_x = QPushButton(f"Add Pair X")
            self.add_pair_button_x.setStyleSheet("background-color: #6c9ccc; color: white;")
            self.add_pair_button_x.clicked.connect(lambda: self.onAddPairButtonClicked('x'))
            row_layout_x.addWidget(self.add_pair_button_x)
            
        self.form_layout.addRow(match_on_x_label, row_layout_x)

        
    def addPairComboBoxesY(self):        
        combo_box_y_left = QComboBox()
        combo_box_y_right = QComboBox()
        
        combo_box_y_left.setStyleSheet("background-color: #4f3869; color: white;")
        combo_box_y_right.setStyleSheet("background-color: #4f3869; color: white;")
        
        combo_box_y_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Adjust the size policy
        combo_box_y_left.setMinimumWidth(80)  # Set minimum width
        combo_box_y_left.setMinimumHeight(20)  # Set minimum height
        
        combo_box_y_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Adjust the size policy
        combo_box_y_right.setMinimumWidth(80)  # Set minimum width
        combo_box_y_right.setMinimumHeight(20)  # Set minimum height
        
        combo_box_y_left.addItem("-")
        combo_box_y_right.addItem("-")
        
        for comp_name in self.netlist_map:
            combo_box_y_left.addItem(comp_name)
            combo_box_y_right.addItem(comp_name)
        
        self.combo_boxes_y.append((combo_box_y_left, combo_box_y_right))
                
        row_layout_y = QHBoxLayout()
        row_layout_y.addWidget(combo_box_y_left)
        row_layout_y.addWidget(combo_box_y_right)
        match_on_y_label = QLabel("Match on Y:", self)
        match_on_y_label.setStyleSheet("color: black;") 
        
        if not hasattr(self, 'add_pair_button_y'):
            self.add_pair_button_y = QPushButton(f"Add Pair Y")
            self.add_pair_button_y.setStyleSheet("background-color: #6c9ccc; color: white;")
            self.add_pair_button_y.clicked.connect(lambda: self.onAddPairButtonClicked('y'))
            row_layout_y.addWidget(self.add_pair_button_y)
            
        self.form_layout.addRow(match_on_y_label, row_layout_y)


    def addPairComboBoxesI(self):        
        combo_box_i_left = QComboBox()
        combo_box_i_mid = QComboBox()
        combo_box_i_right = QComboBox()
        
        combo_box_i_left.setStyleSheet("background-color: #384f69; color: white;")
        combo_box_i_mid.setStyleSheet("background-color: #384f69; color: white;")
        combo_box_i_right.setStyleSheet("background-color: #384f69; color: white;")
        
        combo_box_i_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Adjust the size policy
        combo_box_i_left.setMinimumWidth(80)  # Set minimum width
        combo_box_i_left.setMinimumHeight(20)  # Set minimum height
        
        combo_box_i_mid.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Adjust the size policy
        combo_box_i_mid.setMinimumWidth(80)  # Set minimum width
        combo_box_i_mid.setMinimumHeight(20)  # Set minimum height
        
        combo_box_i_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Adjust the size policy
        combo_box_i_right.setMinimumWidth(80)  # Set minimum width
        combo_box_i_right.setMinimumHeight(20)  # Set minimum height
        
        combo_box_i_left.addItem("-")
        combo_box_i_mid.addItem("-")
        combo_box_i_right.addItem("-")
        
        for comp_name in self.netlist_map:
            combo_box_i_left.addItem(comp_name)
            combo_box_i_mid.addItem(comp_name)
            combo_box_i_right.addItem(comp_name)
        
        self.combo_boxes_i.append((combo_box_i_left, combo_box_i_mid, combo_box_i_right))
                
        row_layout_i = QHBoxLayout()
        row_layout_i.addWidget(combo_box_i_left)
        row_layout_i.addWidget(combo_box_i_mid)
        row_layout_i.addWidget(combo_box_i_right)
        match_on_i_label = QLabel("Important Paths:", self)
        match_on_i_label.setStyleSheet("color: black;") 
        
        if not hasattr(self, 'add_pair_button_i'):
            self.add_pair_button_i = QPushButton(f"Add Path")
            self.add_pair_button_i.setStyleSheet("background-color: #6c9ccc; color: white;")
            self.add_pair_button_i.clicked.connect(lambda: self.onAddPairButtonClicked('i'))
            row_layout_i.addWidget(self.add_pair_button_i)
            # self.form_layout.addRow(match_on_i_label, row_layout_i)
            
        self.form_layout.addRow(match_on_i_label, row_layout_i)
    
    
    def is_valid(self, data):
        return bool(data.get("match_on_x") and data.get("match_on_y") and data.get("important_paths") and data.get("size_unit") and 
                    data.get("min_diff_dist") and data.get("gate_out_height") and data.get("diff_side_width"))
    
        
    def onAddPairButtonClicked(self, axis):
        if axis == 'x':
            self.addPairComboBoxesX()
        elif axis == 'y':
            self.addPairComboBoxesY()
        elif axis == 'i':
            self.addPairComboBoxesI()
    
    
    def collectPairData(self, combo_boxes):
        pairs = []
        for combo_box_pair in combo_boxes:
            left = combo_box_pair[0].currentText()
            right = combo_box_pair[1].currentText()
            if left != "-" and right != "-":
                pairs.append([left, right])
        return pairs
    
    
    def collectPathData(self, combo_boxes):
        paths = []
        for combo_box_path in combo_boxes:
            path = []
            for combo_elem in combo_box_path:
                comb_el = combo_elem.currentText()
                if comb_el != '-':
                    path.append(comb_el)
            paths.append(path)
        return paths
    
        
    def onOKClicked(self):
        # open('config_data_ic.json', 'w').close()
        data = self.getData()
        with open('config_data_ic.json', 'w') as json_file:
            json.dump(data, json_file, indent = 4)
        self.accept()
    
    
    def onCancelClicked(self):
        self.reject()
        
        
    def onClearClicked(self):
        open('config_data_ic.json', 'w').close()
        self.size_unit_lineedit.clear()
        self.min_diff_dist_lineedit.clear()
        self.gate_out_height_lineedit.clear()
        self.diff_side_width_lineedit.clear()
        self.reject()
    
    
    def read_input(self, file_name):
        try:
            with open(file_name, 'r') as file:
                return file.readlines()
        except:
            return "File not found"  
    
    
    def load_json_to_python(self, json_file):
        json_lines = self.read_input(json_file)
        json_content = '\n'.join(json_lines)
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError:
            data = {}
        return data
    
    
    def setData(self):
        self.setDataForPairs(self.data["match_on_x"], self.combo_boxes_x)
        self.setDataForPairs(self.data["match_on_y"], self.combo_boxes_y)
        self.setDataForPaths(self.data["important_paths"], self.combo_boxes_i)
        
        self.size_unit_lineedit.setText(self.data["size_unit"])
        self.min_diff_dist_lineedit.setText(self.data["min_diff_dist"])
        self.gate_out_height_lineedit.setText(self.data["gate_out_height"])
        self.diff_side_width_lineedit.setText(self.data["diff_side_width"])
        

    def setDataForPairs(self, pairs, combo_boxes):
        for index, pair in enumerate(pairs):
            left_comp, right_comp = pair
            left_combo_box, right_combo_box = combo_boxes[index]
            left_combo_box.setCurrentText(left_comp)
            right_combo_box.setCurrentText(right_comp)
            

    def setDataForPaths(self, paths, combo_boxes):
        for index, path in enumerate(paths):
            combo_box_left, combo_box_mid, combo_box_right = combo_boxes[index]
            for i, comp in enumerate(path):
                if i == 0:
                    combo_box_left.setCurrentText(comp)
                elif i == 1:
                    combo_box_mid.setCurrentText(comp)
                elif i == 2:
                    combo_box_right.setCurrentText(comp)
        
    
    def getData(self):
        data = {
            "match_on_x": self.collectPairData(self.combo_boxes_x),
            "match_on_y": self.collectPairData(self.combo_boxes_y),
            "important_paths": self.collectPathData(self.combo_boxes_i),
            "size_unit": self.size_unit_lineedit.text(),
            "min_diff_dist": self.min_diff_dist_lineedit.text(),
            "gate_out_height": self.gate_out_height_lineedit.text(),
            "diff_side_width": self.diff_side_width_lineedit.text()
        }
        return data
    
    
    def remove_duplicates_from_json(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        for key, value in data.items():
            if isinstance(value, list):
                data[key] = list(dict.fromkeys(map(tuple, value)))
                
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
            
            
    def getJson(self):
        json_file = 'config_data_ic.json'
        self.remove_duplicates_from_json(json_file)
        return json_file