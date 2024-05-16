from ComponentCollection import ComponentCollection, Component, Rectangle
from GetData import getJSONDetails, getNetlistDetails
from Legalization import Legalization2
# from ComponentWidget import ComponentWidget
from MainForANN import mainForANN

import tensorflow as tf
import numpy as np
import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout, QLabel
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QPixmap, QImage
from PySide6.QtCore import Qt, QRectF, QPointF, QObject, Signal
    
    
class ComponentWidget(QWidget):
    regenerate_signal = Signal(str)
    file_saved = Signal(str)
    
    def __init__(self, components, netlist_details, json_details, validator, parent=None):
        super().__init__(parent)
        self.components = components
        
        self.netlist_details = netlist_details
        self.json_details = json_details
        self.validator = validator
        
        self.scale_factor = 90
        self.selected_component = None
        self.offset = QPointF(0, 0)  # Offset to track the position change
        
        self.setStyleSheet("background-color: white;")
        
        min_x = min(comp.rectangle.x1 for comp in components)
        min_y = min(comp.rectangle.y1 for comp in components)
        
        if min_x <= 0:
            for comp in self.components:
                comp.rectangle.x1 -= min_x - 2
        if min_y <= 0:
            for comp in self.components:
                comp.rectangle.y1 -= min_y - 2

        self.regenerate_button = QPushButton("Regenerate")
        self.regenerate_button.clicked.connect(self.regenerate_components)
        self.regenerate_button.setStyleSheet("background-color: #4e6d5e; color: white;")
        
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("background-color: #4e6d5e; color: white;")
        self.save_button.clicked.connect(self.save_placement)
        
        self.exit_button = QPushButton("Exit")
        self.exit_button.setStyleSheet("background-color: #4e6d5e; color: white;")
        self.exit_button.clicked.connect(self.exit)
        
        self.placement_state_label = QLabel("Placement State: False")
        self.placement_state_label.setStyleSheet("color: black;")
    
        
        layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.placement_state_label)
        hbox.addWidget(self.regenerate_button)
        hbox.addWidget(self.save_button)
        hbox.addWidget(self.exit_button)
        hbox.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        layout.addLayout(hbox)
        self.setLayout(layout)
        
        # self.regenerate_components()
    
    
    def change_placement_state(self, valid):
        if valid:
            self.placement_state_label.setText("Placement State: True")
        else:
            self.placement_state_label.setText("Placement State: False")
            
    
    def regenerate_components(self):
        self.regenerate_signal.emit("signal emitted")
        print("regenerate signal!")
        
        
    def execute_mainForANN(self):
        comps, isValid = mainForANN(self.netlist_details, self.json_details, self.validator)
        print(self.components)
        print("comps:")
        print(comps)
        self.components = comps
        self.update()
        
    
    def exit(self):
        # exit_pressed = True
        quit()
    
    
    def save_placement(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Placement", "", "Images (*.jpg)")
        if filename:
            self.regenerate_button.hide()
            self.save_button.hide()
            self.exit_button.hide()
            
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            pixmap.toImage().save(filename)
            
            self.regenerate_button.show()
            self.exit_button.show()
            self.save_button.show()
            
            self.file_saved.emit(filename)
            print("Saved as jpg")
            
    
    # def save_placement(self):
    #     filename, _ = QFileDialog.getSaveFileName(self, "Save Placement", "placement", "Images (*.jpg)")
    #     if filename:
    #         # pixmap = QPixmap(self.size())  # Create a pixmap with the size of the widget
    #         # painter = QPainter(pixmap)  # Create a QPainter to paint on the pixmap
    #         # self.render(painter)  # Render the widget onto the pixmap
    #         # painter.end()  # End painting
    #         # 
    #         # # Adjust the area to include only the placement of components
    #         # rect = self.contentsRect()  # Get the rectangle that contains the placement
    #         # cropped_pixmap = pixmap.copy(rect)  # Crop the pixmap to include only the placement area
    #         # 
    #         # # Save the cropped pixmap as an image
    #         # cropped_pixmap.toImage().save(filename)
    #         imageVar = QImage(self.size(), QImage.Format.Format_ARGB32)
    #         self.render(imageVar)
    #         imageVar.save(filename)


    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)

        # brush = QBrush(Qt.SolidPattern)
        # painter.setBrush(Qt.green)
        # brush_color = QColor("#45f0d0")
        # brush_color = QColor("#61f1c8")
        brush_color = QColor("#a0f4cc")
        brush = QBrush(brush_color)
        painter.setBrush(brush)
        # painter.setBrush(brush)

        for comp in self.components:
            rect = comp.rectangle
            x1, y1, width, height = rect.x1, rect.y1, rect.width, rect.height
            qrect = QRectF(self.scale_factor * x1, self.scale_factor * y1, self.scale_factor * width, self.scale_factor * height)
            painter.drawRect(qrect)
            font = QFont()
            font.setPointSizeF(8)
            painter.setFont(font)
            painter.drawText(qrect, Qt.AlignCenter, comp.name)
    
        
    def mousePressEvent(self, event):
        mouse_pos = event.pos()
        for comp in self.components:
            rect = QRectF(self.scale_factor * comp.rectangle.x1, self.scale_factor * comp.rectangle.y1,
                        self.scale_factor * comp.rectangle.width, self.scale_factor * comp.rectangle.height)
            if rect.contains(mouse_pos):
                self.selected_component = comp
                # Calculate the offset based on the center of the rectangle
                self.offset = QPointF(mouse_pos.x() - (rect.x() + rect.width() / 2),
                                      mouse_pos.y() - (rect.y() + rect.height() / 2))
                self.update()
                return
        super().mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if self.selected_component:
            mouse_pos = event.pos()
            # Calculate the new position based on the center of the rectangle and the offset
            new_x_center = (mouse_pos.x() - self.offset.x()) / self.scale_factor
            new_y_center = (mouse_pos.y() - self.offset.y()) / self.scale_factor
            # Update the rectangle position
            self.selected_component.rectangle.x1 = new_x_center - self.selected_component.rectangle.width / 2
            self.selected_component.rectangle.y1 = new_y_center - self.selected_component.rectangle.height / 2
            self.update()
            return
        super().mouseMoveEvent(event)
    
    
    # def mouseReleaseEvent(self, event):
    #     self.selected_component = None
    #     self.offset = QPointF(0, 0)
    #     self.update()
    #     super().mouseReleaseEvent(event)
    

    def check_overlap(self):
        for i, comp1 in enumerate(self.components):
            for j, comp2 in enumerate(self.components):
                if i != j:  # Avoid comparing the same rectangle with itself
                    rect1 = QRectF(self.scale_factor * comp1.rectangle.x1, self.scale_factor * comp1.rectangle.y1,
                                self.scale_factor * comp1.rectangle.width, self.scale_factor * comp1.rectangle.height)
                    rect2 = QRectF(self.scale_factor * comp2.rectangle.x1, self.scale_factor * comp2.rectangle.y1,
                                self.scale_factor * comp2.rectangle.width, self.scale_factor * comp2.rectangle.height)
                    if rect1.intersects(rect2):
                        return True
        return False


    def mouseReleaseEvent(self, event):
        self.selected_component = None
        self.offset = QPointF(0, 0)
        if self.check_overlap():
            self.placement_state_label.setText("Placement State: False")
        else:
            self.placement_state_label.setText("Placement State: True")
        self.update()
        super().mouseReleaseEvent(event)

# def main():
#     app = QApplication(sys.argv)
#     
#     # Get the netlist details
#     file_name_netlist = '../folded_cascode_opamp_ac_deck2.sp'
#     file_name_json = '../folded_cascode_opamp_constraints2.json'
#     
#     netlist_details = getNetlistDetails(file_name_netlist)
#     json_details = getJSONDetails(file_name_json)
#     
#     
#     
#     # Create the ComponentWidget and show it
#     widget = ComponentWidget(components=[])  # Initialize with an empty list of components
#     widget.setWindowTitle("Placement")
#     widget.resize(900, 800)
#     widget.show()
#     
#     # Execute the application event loop
#     sys.exit(app.exec_())
# 
# if __name__ == "__main__":
#     main()