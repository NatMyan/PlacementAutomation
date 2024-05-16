from ComponentCollection import ComponentCollection, Component, Rectangle
from ComponentWidget3 import ComponentWidget
from GetData import getJSONDetails, getNetlistDetails
from PlacementValidator import PlacementValidator
from Legalization import Legalization2
from MainForANN import mainForANN
from StartMenu2 import StartMenu

import tensorflow as tf
import numpy as np
import os
import sys
from PySide6.QtWidgets import QApplication
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense        
from sklearn.preprocessing import StandardScaler   


if __name__ == '__main__':
    f = open("/dev/null", "w")
    os.dup2(f.fileno(), 2)
    f.close()
    
    print("vakh")
    app = QApplication(sys.argv)
    
    start_menu = StartMenu()
    start_menu.show()
      
    app.exec_()
    
    validator = PlacementValidator()
    
    file_name_netlist = start_menu.getNetlist()
    file_name_json = start_menu.getJson()
    
    netlist_details = getNetlistDetails(file_name_netlist)
    json_details = getJSONDetails(file_name_json)
    
    regenerate_pressed = True
    print("before comps, app")
    
    comps, isValid = mainForANN(netlist_details, json_details, validator)
    
    
    widget = ComponentWidget(comps, netlist_details, json_details, validator)

    widget.regenerate_signal.connect(widget.execute_mainForANN)
    widget.change_placement_state(isValid)
    widget.setWindowTitle("Placement")
    widget.resize(900, 800)
    
    widget.show()
    
    app.exec_()
        

   