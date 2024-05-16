from ComponentCollection import Rectangle, Component

from typing import Dict
import random

class ComponentGeneration:
    def generate_coordinates(self, netlist_dict: Dict[str, Dict[str, float]], json_data: Dict):
        components = []

        if netlist_dict and json_data:
            # micrometer_factor = 1e6

            outHeight = float(json_data.get('gate_out_height'))
            sideWidth = float(json_data.get('diff_side_width'))

            for transistor, attributes in netlist_dict.items():
                width = attributes.get('w', 0)
                length = attributes.get('l', 0)

                nf = attributes.get('nf', 0)
                m = attributes.get('m', 0)

                topLeftX = random.uniform(0, 5)  
                topLeftY = random.uniform(0, 5) 
                
                components.append({
                    'transistor_name': transistor,
                    'lowerLeftX': topLeftX,
                    'lowerLeftY': topLeftY,
                    'width': (nf * length) + ((nf + 1) * sideWidth),
                    'height': (m * width) + (2 * outHeight),
                })
                
                i = 0
                for entry in json_data['match_on_x']:
               
                    print(entry)
                    up, down, center = entry[0], entry[1], 0 # i # 10 # entry[2]
                   

                    # Move matched rectangles to specified origin (around center in this case).
                    if transistor == up or transistor == down:
                        width = components[-1]['width']
                        components[-1]['lowerLeftX'] = center - width / 2

                    i += 1

                for entry in json_data['match_on_y']:
                    left = entry[0]

                    # Move matched rectangles to specified origin (around 0 in this case).
                    if transistor == left:
                        width = components[-1]['width']
                        components[-1]['lowerLeftX'] = -width

            if components:
                components_lst = self.construct_list(components)
                return components_lst


    def construct_list(self, components):
        components_lst = []

        for component in components:
            name = component['transistor_name']
            x1 = component['lowerLeftX']
            y1 = component['lowerLeftY']
            width = component['width']
            height = component['height']

            rectangle = Rectangle(x1, y1, width, height)
            rect_component = Component(name, rectangle)

            components_lst.append(rect_component)

        return components_lst
