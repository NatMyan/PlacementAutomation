import sys
import os

from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PySide6.QtCore import Qt, QRectF, QPointF


class ComponentWidget(QWidget):
    def __init__(self, components, parent=None):
        super().__init__(parent)
        if components:
            self.components = components
            self.scale_factor = 90
            self.selected_component = None
            self.offset = QPointF(0, 0)  # Offset to track the position change
            
            self.setStyleSheet("background-color: white;")
            
            min_x = min(comp.rectangle.x1 for comp in components)
            min_y = min(comp.rectangle.y1 for comp in components)
            
            if min_x <= 0:
                for comp in self.components:
                    comp.rectangle.x1 -= min_x - 3
            if min_y <= 0:
                for comp in self.components:
                    comp.rectangle.y1 -= min_y - 3
                    

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        
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
    
    
    def mouseReleaseEvent(self, event):
        self.selected_component = None
        self.offset = QPointF(0, 0)
        self.update()
        super().mouseReleaseEvent(event)
    
    
   