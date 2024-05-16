from ComponentCollection import ComponentCollection, Component, Rectangle
# from ComponentWidget3 import ComponentWidget
from GetData import getJSONDetails, getNetlistDetails
from PlacementValidator import PlacementValidator
from Legalization import Legalization2
from StartMenu2 import StartMenu
# from MainForANN import mainForANN

import tensorflow as tf
import numpy as np
import os
import sys
from PySide6.QtWidgets import QApplication
           

def mainForANN(netlist_details, json_details, validator):
    loaded_model = tf.keras.models.load_model("ann.h5")
    values = []
    for key in sorted(netlist_details.keys()):
        values.extend([netlist_details[key][prop] for prop in ['l', 'w', 'nf', 'm']])
    
    points = np.array(values)
    points = points.reshape(1, -1)
    
    new_output_data = loaded_model.predict(points)
    
    output = new_output_data.flatten()
    
    components = []
    j = 1
    for i in range(0, len(output.flatten()), 4):
        numbers = [num for num in output[i:i+4]]
        comp_dict = {"xm" + str(j) : numbers}
        components.append(comp_dict)
        j += 1
    
    comps = []
    
    for item in components:
        name, coords = list(item.items())[0]
        x1, y1, x2, y2 = coords
        width = x2 - x1
        height = y2 - y1
        rect = Rectangle(x1, y1, width, height)
        component = Component(name, rect)
        comps.append(component)
            
    legalized = Legalization2(comps, json_details)
    legalized_lst = legalized.legalize()
    
    if legalized_lst:
        print('Info: Legal (vertical):')
        for component in legalized_lst:
            print(f'    {component}')
    
    print("Info: General placement: ", validator.check_general_placement(legalized_lst))
    print("Info: Full placement: ", validator.isPlacementValid(legalized_lst, json_details))
    
    return comps, validator.check_general_placement(legalized_lst)  

    

