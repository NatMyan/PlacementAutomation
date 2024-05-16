from GetData import getNetlistDetails, getJSONDetails
from PlacementValidator import PlacementValidator
from MinimizePlacement import MinimizePlacement
# from MinimizePlacement1 import MinimizePlacement
from ComponentCollection import ComponentCollection
from ComponentGeneration import ComponentGeneration 
from Legalization import SolveLayoutCompaction, Legalization, Legalization2
# from StartMenu2 import StartMenu
from StartMenu import StartMenu
# from ComponentWidget import ComponentWidget
from ComponentWidget2 import ComponentWidget

import os
import sys
import csv
from PySide6.QtWidgets import QApplication
           
          
if __name__ == '__main__':
    f = open("/dev/null", "w")
    os.dup2(f.fileno(), 2)
    f.close()
    
    print("vakh")
    app = QApplication(sys.argv)
    
    start_menu = StartMenu()
    start_menu.show()
      
    app.exec_()
        
    file_name_netlist = start_menu.getNetlist()
    file_name_json = start_menu.getJson()
         
    netlist_details = getNetlistDetails(file_name_netlist)
    json_details = getJSONDetails(file_name_json)
    validator = PlacementValidator()
    
#---------------------------------------------------------------------------------------------------------------------
    component_generator = ComponentGeneration()
    components = component_generator.generate_coordinates(netlist_details, json_details)
    
    if components:
        print('Info: Components:')
        for component in components:
            print(f'    {component}')
    print("vakh7")
    print('Info: General placement: ', validator.check_general_placement(components))
    print('Info: Full placement: ', validator.isPlacementValid(components, json_details))
    print('\n')
    
    widget_c = ComponentWidget(components)
    widget_c.setWindowTitle("Phase 1")
    widget_c.resize(900, 700)
    widget_c.show()
            
    app.exec_()

          
#---------------------------------------------------------------------------------------------------------------------
    print(components)
    global_placement = MinimizePlacement(components, json_details)
    global_placement_list = global_placement.minimize()
    # Make all coordinates start from 0 to further constrain the LP problem value space.
    ComponentCollection.make_coords_positive(global_placement_list)
           
    if global_placement_list:
        print('Info: Global:')
        for component in global_placement_list:
            print(f'    {component}')

    print('Info: General placement: ', validator.check_general_placement(global_placement_list))
    print('Info: Full placement: ', validator.isPlacementValid(global_placement_list, json_details))
    print('\n')
        
    # widget_g = ComponentWidget(components)
    widget_g = ComponentWidget(global_placement_list)
    widget_g.setWindowTitle("Phase 2")
    widget_g.resize(800, 800)
    widget_g.show()
            
    app.exec_()
    
           
#---------------------------------------------------------------------------------------------------------------------
    # Paper suggests to perform compaction sequentially, first in horizontal then vertical direcitons,
    # and claims that solving both problems in parallel is NP-complete.
    
    # legalized_list_horizontal = SolveLayoutCompaction(global_placement_list, json_details, direction='horizontal')
    # 
    # if legalized_list_horizontal:
    #     print('Info: Legal (horizontal):')
    #     for component in legalized_list_horizontal:
    #         print(f'    {component}')
    # 
    # # draw_components(legalized_list_horizontal)
    # 
    # legalized_list_vertical = SolveLayoutCompaction(legalized_list_horizontal, json_details, direction='vertical')
    #     
    # if legalized_list_vertical:
    #     print('Info: Legal (vertical):')
    #     for component in legalized_list_vertical:
    #         print(f'    {component}')
    # 
    # print('Info: General placement: ', validator.check_general_placement(legalized_list_vertical))
    # print('Info: Full placement: ', validator.isPlacementValid(legalized_list_vertical, json_details))

    # legalized = Legalization(legalized_list_vertical, json_details)
    # legalized_list = legalized.legalize()
      
    # if legalized_list:
    #     print("Legal:")
    #     for component in legalized_list:
    #         print(f"    {component}")
         
    # print("Info: General placement: ", validator.check_general_placement(legalized_list))
    # print("Info: Full placement: ", validator.isPlacementValid(legalized_list, json_details))
    
    legalized = Legalization2(global_placement_list, json_details)
    legalized_lst = legalized.legalize()
    
    if legalized_lst:
        print('Info: Legal:')
        for component in legalized_lst:
            print(f'    {component}')
    
    print("Info: General placement: ", validator.check_general_placement(legalized_lst))
    print("Info: Full placement: ", validator.isPlacementValid(legalized_lst, json_details))
    
    # widget_l = ComponentWidget(components)
    # widget_l = ComponentWidget(legalized_list_vertical)
    widget_l = ComponentWidget(legalized_lst)
    widget_l.setWindowTitle("Phase 3")
    widget_l.resize(800, 800)
    widget_l.show()
            
    app.exec_()
    
    print(legalized_lst)
             
#---------------------------------------------------------------------------------------------------------------------  
    if components:
        print('Info: Components:')
        for component in components:
            print(f'    {component}')
    
    print('Info: General placement: ', validator.check_general_placement(components))
    print('Info: Full placement: ', validator.isPlacementValid(components, json_details))
    
    component_names = list(netlist_details.keys())
    csv_file = 'data.csv'
    
    ''' Check if file exists and is empty '''
    is_empty = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0
    print(is_empty)
    
    points = []
    for comp in components:
        points.append(comp.rectangle.x1)
        points.append(comp.rectangle.y1)
        points.append(comp.rectangle.x2)
        points.append(comp.rectangle.y2)
    print ("Points:", points)
    
    with open(csv_file, mode='a', newline='') as file:  
        writer = csv.writer(file) 
        
        if is_empty:
            header_row = []
            for comp in component_names:
                header_row.append(f'{comp}_width') 
                header_row.append(f'{comp}_length') 
                header_row.append(f'{comp}_nf') 
                header_row.append(f'{comp}_m') 
            for comp in component_names:
                header_row.append(f'{comp}_x1') 
                header_row.append(f'{comp}_y1') 
                header_row.append(f'{comp}_x2') 
                header_row.append(f'{comp}_y2') 
            writer.writerow(header_row)
        
        row = []
        for comp in component_names:
            for prop in ['w', 'l', 'nf', 'm']:
                row.append(netlist_details[comp][prop])
        for num in points:
            row.append(num)
        
        writer.writerow(row)
        
    
