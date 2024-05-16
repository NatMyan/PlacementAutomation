from pulp import LpProblem, LpVariable, LpMinimize, lpSum
from ComponentCollection import Component, Rectangle
# from sortedcontainers import SortedList


class Legalization2:
    def __init__(self, placement_lst, json_details):
        if placement_lst and json_details:
            self.placement_lst = placement_lst
            self.json_details = json_details
    
    def legalize(self):
        if self.placement_lst and self.json_details:
            # sorted_lst = sorted(self.placement_lst, key = lambda comp: (comp.rectangle.x1, comp.rectangle.y1))
            
            # x_starts = self.__get_starts(sorted_lst, self.json_details["match_on_x"])
            # y_starts = self.__get_starts(sorted_lst, self.json_details["match_on_y"])
            # imp_starts = self.__get_starts(sorted_lst, self.json_details["important_paths"])
            # 
            # self.__match_x(sorted_lst, x_starts)
            # self.__match_y(sorted_lst, y_starts)
            # self.__fix_imp_paths(sorted_lst, imp_starts)
            
            self.__resolve_overlaps(self.placement_lst)
            
            placement_list = self.placement_lst
            return placement_list
            
                        
    def __resolve_overlaps(self, components):
        i = 0
        while True:
            print("W iter: ", i)
            overlaps_detected = False
            for comp1 in components:
                for comp2 in components:
                    if comp1 != comp2 and self.__overlaps(comp1.rectangle, comp2.rectangle):
                        self.__resolve_overlap(comp1.rectangle, comp2.rectangle)
                        overlaps_detected = True
            if not overlaps_detected:
                break
            
            i += 1    
            
    
    def __resolve_overlap(self, rect1, rect2):
        x_overlap = max(0, min(rect1.x1 + rect1.width, rect2.x1 + rect2.width) - max(rect1.x1, rect2.x1))
        y_overlap = max(0, min(rect1.y1 + rect1.height, rect2.y1 + rect2.height) - max(rect1.y1, rect2.y1))
        
        if x_overlap > 0 and y_overlap > 0:
            if x_overlap < y_overlap:
                if rect1.x1 < rect2.x1:
                    rect1.x1 = rect1.x1 - x_overlap - float(self.json_details["min_diff_dist"])
                else:
                    rect2.x1 = rect2.x1 - x_overlap - float(self.json_details["min_diff_dist"])
            else:
                if rect1.y1 < rect2.y1:
                    rect1.y1 = rect1.y1 - y_overlap - float(self.json_details["min_diff_dist"])
                else:
                    rect2.y1 = rect2.y1 - y_overlap - float(self.json_details["min_diff_dist"])
                    

    def __overlaps(self, rect1, rect2):
        overlap_area = 0    
        
        x_dist = (min(rect1.x2, rect2.x2) - max(rect1.x1, rect2.x1))
        y_dist = (min(rect1.y2, rect2.y2) - max(rect1.y1, rect2.y1))
        
        if x_dist > 0 and y_dist > 0:
            overlap_area = x_dist * y_dist  
                                
        return overlap_area > 0


'''class Legalization:
    def __init__(self, components, json_details):
        if components and json_details:
            self.components = components
            self.json_details = json_details
            self.flags = {
                'x' : 1,
                'y' : 2,
                'i' : 4
            }


    def legalize(self):
        if self.components and self.json_details:
            sorted_lst = sorted(self.components, key=lambda comp: (comp.rectangle.x1, comp.rectangle.y1))
            
            # x_starts = self.__get_starts(sorted_lst, self.json_details["match_on_x"])
            # y_starts = self.__get_starts(sorted_lst, self.json_details["match_on_y"])

            # self.comps_w_flags = dict((comp, {'x' : False, 'y': False}) for comp in self.components)
            # print(self.comps_w_flags)
            # 
            # for comp in self.components:
            #     if self.__is_component_in_x(comp.name):
            #         self.comps_w_flags[comp]['x'] = True
            #     if self.__is_component_in_y(comp.name):
            #         self.comps_w_flags[comp]['y'] = True
            
            self.__resolve_overlaps(self.components)

            placement_list = self.components
            return placement_list
        
                                     
    # def __get_move_with_comp_list(self, comp_name):
    #     comps_to_move = []
    #     for comp in self.components:
    #         while (comp.name != comp_name):
    #             if self.__is_pair_in_x(comp.name):
    #                 comps_to_move.append(comp.name)
    #             if self.__is_pair_in_y(comp_name):
    #                 comps_to_move.append(comp.name)
                    
    
    def __is_component_in_x (self, comp_name):
        for lst in self.json_details["match_on_x"]:
            if comp_name in lst:
                return True
        return False
    
    
    def __is_component_in_y (self, comp_name):
        for lst in self.json_details["match_on_y"]:
            if comp_name in lst:
                return True
        return False
    
             
    def __resolve_overlaps(self, components):
        i = 0
        while True:   # i < 100:    # ara de lav eli
            print("W iter: ", i)
            overlaps_detected = False
            for comp1 in components:
                for comp2 in components:
                    if comp1 != comp2:
                        print(f'Components to resolve: {comp1}, {comp2}')
                        overlap = self.__overlap_area(comp1.rectangle, comp2.rectangle)

                        if overlap > 0:
                            self.__resolve_overlap(comp1, comp2)
                            # draw_components(components)
                            overlaps_detected = True
                 
            if not overlaps_detected:
                break
                                      
            i += 1
            
                   
    def __get_move_on_x_list(self, comp_name): 
        comps_to_move_x = [comp_name]
        for pair in self.json_details["match_on_x"]:
            if comp_name in pair:
                other_comp = pair[0] if pair[1] == comp_name else pair[1]
                comps_to_move_x.append(other_comp)
        return comps_to_move_x
        
    def __get_move_on_y_list(self, comp_name): 
        comps_to_move_y = [comp_name]
        for pair in self.json_details["match_on_y"]:
            if comp_name in pair:
                other_comp = pair[0] if pair[1] == comp_name else pair[1]
                comps_to_move_y.append(other_comp)
        return comps_to_move_y                   
        
        
    # def __get_move_on_i_path(self, comp_name):
    #     comps_to_move_i = [comp_name]
    #     for path in self.json_details["important_paths"]:
    #         if comp_name in path:
    #             for comp in path:
    #                 if comp != comp_name:
    #                     comps_to_move_i.append(comp)
    #     return comps_to_move_i
    
        
    def __move_on_x(self, comps_to_move, x_overlap):
        for comp_name in comps_to_move:
            for comp in self.components:
                if comp.name == comp_name:
                    comp.rectangle.x1 = comp.rectangle.x1 - x_overlap - float(self.json_details["min_diff_dist"])
        
    
    def __move_on_y(self, comps_to_move, y_overlap):
        for comp_name in comps_to_move:
            for comp in self.components:
                if comp.name == comp_name:
                    comp.rectangle.y1 = comp.rectangle.y1 - y_overlap - float(self.json_details["min_diff_dist"])
    
                   
    def __resolve_overlap(self, comp1, comp2):
        x_overlap = max(0, min(comp1.rectangle.x1 + comp1.rectangle.width, comp2.rectangle.x1 + comp2.rectangle.width) - max(comp1.rectangle.x1, comp2.rectangle.x1))
        y_overlap = max(0, min(comp1.rectangle.y1 + comp1.rectangle.height, comp2.rectangle.y1 + comp2.rectangle.height) - max(comp1.rectangle.y1, comp2.rectangle.y1))

        if x_overlap > 0 and y_overlap > 0:
            if x_overlap < y_overlap:
                comps_to_move_on_x = []
                # comps_to_move_i = []

                if comp1.rectangle.x1 < comp2.rectangle.x1:
                    comps_to_move_on_x.extend(self.__get_move_on_x_list(comp1.name))
                    # comps_to_move_i.extend(self.__get_move_on_i_path(comp1.name))
                else:
                    comps_to_move_on_x.extend(self.__get_move_on_x_list(comp2.name))
                    # comps_to_move_i.extend(self.__get_move_on_i_path(comp2.name))

                # comps_to_move_on_x.extend(comps_to_move_i)
                comps_to_move_on_x = list(set(comps_to_move_on_x))
                self.__move_on_x(comps_to_move_on_x, x_overlap)
                
            else:
                comps_to_move_on_y = []
                # comps_to_move_i = []

                if comp1.rectangle.y1 < comp2.rectangle.y1:
                    comps_to_move_on_y.extend(self.__get_move_on_y_list(comp1.name))
                    # comps_to_move_i.extend(self.__get_move_on_i_path(comp1.name))
                else:
                    comps_to_move_on_y.extend(self.__get_move_on_y_list(comp2.name))
                    # comps_to_move_i.extend(self.__get_move_on_i_path(comp2.name))

                # comps_to_move_on_y.extend(comps_to_move_i)
                comps_to_move_on_y = list(set(comps_to_move_on_y))
                self.__move_on_y(comps_to_move_on_y, y_overlap)
    

    def __overlap_area(self, rect1, rect2):
        overlap_area = 0

        print(f'    rect1: {rect1}')
        print(f'    rect2: {rect2}')

        min_x2 = min(rect1.x2, rect2.x2)
        max_x1 = max(rect1.x1, rect2.x1)
        min_y2 = min(rect1.y2, rect2.y2)
        max_y1 = max(rect1.y1, rect2.y1)

        print(f'    min_x2: {min_x2}, max_x1: {max_x1}, min_y2: {min_y2}, max_y1: {max_y1}')

        x_dist = min_x2 - max_x1
        y_dist = min_y2 - max_y1

        if x_dist > 0 and y_dist > 0:
            overlap_area = x_dist * y_dist

        print(f'    x_dist: {x_dist}, y_dist: {y_dist}, overlap_area: {overlap_area}')

        return overlap_area



# class Event:
#     def __init__(self, x, comp, is_start):
#         self.x = x
#         self.comp = comp
#         self.is_start = is_start

#     def __lt__(self, other):
#         if self.x != other.x:
#             return self.x < other.x
#         else:
#             return self.is_start and not other.is_start


# class ConstraintGraph:
#     def __init__(self, components):
#         self.components = components
#         self.adjacency_list = {comp: set() for comp in components}

#     def add_constraint(self, comp1, comp2):
#         self.adjacency_list[comp1].add(comp2)

#     def remove_constraint(self, comp1, comp2):
#         self.adjacency_list[comp1].remove(comp2)

#     def get_adjacent_components(self, comp):
#         return self.adjacency_list[comp]

#     def __repr__(self):
#         text = f'{self.__class__.__name__}(\n'

#         for comp, ref_comps in self.adjacency_list.items():
#             text += f'    {comp.name}: {", ".join(ref_comp.name for ref_comp in ref_comps)}\n'

#         text += ')'

#         return text


# Plain sweep algorithm.
# def generate_constraint_graph(components, direction):
#     graph = ConstraintGraph(components)

#     events = []

#     for comp in components:
#         if direction == 'horizontal':
#             events.append(Event(comp.x1, comp, True))
#             events.append(Event(comp.x2, comp, False))
#         else:
#             events.append(Event(comp.y1, comp, True))
#             events.append(Event(comp.y2, comp, False))

#     events.sort()
#     active_events = SortedList()

#     for event in events:
#         if event.is_start:
#             for active_event in active_events:
#                 graph.add_constraint(active_event.comp, event.comp)
#             active_events.add(event)
#         else:
#             if event in active_events:
#                 active_events.remove(event)

#     return graph


# Shadow propagation algorithm (not optimized).
def generate_horizontal_constraint_graph(components, json_details):
    sorted_comps = sorted(components, key=lambda comp: comp.x1)

    graph = {}

    # This approach will generate redundant edges between nodes,
    # which will slow the LP algorithm.

    for i, comp in enumerate(sorted_comps):
        graph[comp] = set()

        for j in range(i + 1, len(sorted_comps)):
            ref_comp = sorted_comps[j]

            # ref_comp falls within the shadow of comp in vertical direction.
            if (
                comp.y1 < ref_comp.y1 < comp.y2 or
                comp.y1 < ref_comp.y2 < comp.y2 or
                ref_comp.y1 < comp.y1 < ref_comp.y2 or
                ref_comp.y1 < comp.y2 < ref_comp.y2
            ):
                graph[comp].add(ref_comp)

    # The violated overlapping constraints between match_on_x instances should be resolved by vertical movement,
    # so remove respective edges from the graph.
    for entry in json_details['match_on_x']:
        up, down = entry[0], entry[1]

        for comp, ref_comps in graph.items():
            if comp.name == up:
                for ref_comp in ref_comps:
                    if ref_comp.name == down:
                        ref_comps.remove(ref_comp)
                        break

            if comp.name == down:
                for ref_comp in ref_comps:
                    if ref_comp.name == up:
                        ref_comps.remove(ref_comp)
                        break

    return graph


# Shadow propagation algorithm (not optimized).
def generate_vertical_constraint_graph(components, json_details):
    sorted_comps = sorted(components, key=lambda comp: comp.y1)

    graph = {}

    # This approach will generate redundant edges between nodes,
    # which will slow the LP algorithm.

    for i, comp in enumerate(sorted_comps):
        graph[comp] = set()

        for j in range(i + 1, len(sorted_comps)):
            ref_comp = sorted_comps[j]

            # ref_comp falls within the shadow of comp in horizontal direction.
            if (
                comp.x1 < ref_comp.x1 < comp.x2 or
                comp.x1 < ref_comp.x2 < comp.x2 or
                ref_comp.x1 < comp.x1 < ref_comp.x2 or
                ref_comp.x1 < comp.x2 < ref_comp.x2
            ):
                graph[comp].add(ref_comp)

    # The violated overlapping constraints between match_on_y instances should be resolved by horizontal movement,
    # so remove respective edges from the graph.
    for entry in json_details['match_on_y']:
        left, right = entry[0], entry[1]

        for comp, ref_comps in graph.items():
            if comp.name == left:
                for ref_comp in ref_comps:
                    if ref_comp.name == right:
                        ref_comps.remove(ref_comp)
                        break

            if comp.name == right:
                for ref_comp in ref_comps:
                    if ref_comp.name == left:
                        ref_comps.remove(ref_comp)
                        break

    return graph


def SolveLayoutCompaction(components, json_details, direction='horizontal'):
    if direction == 'horizontal':
        constraint_graph = generate_horizontal_constraint_graph(components, json_details)
    else:
        constraint_graph = generate_vertical_constraint_graph(components, json_details)

    print(f'Info: Constraint graph for {direction} direction is:')
    for comp, ref_comps in constraint_graph.items():
        print(f'    {comp.name}: {", ".join([ref_comp.name for ref_comp in ref_comps])}')

    prob = LpProblem(f'Layout_Compaction_{direction.capitalize()}', LpMinimize)

    # Since we are considering one direction at a time,
    # each rectangle is represented by its x or y coordinate.
    variables = {}

    for i, comp in enumerate(components):
        variables[i] = LpVariable(f'pos_{i}', lowBound=0, cat='Continuous')

        if direction == 'horizontal':
            variables[i].setInitialValue(comp.x1)
        else:
            variables[i].setInitialValue(comp.y1)

    # Objective function: Minimize total width/height
    prob += lpSum(
        variables[i] + components[i].width if direction == 'horizontal' else
        variables[i] + components[i].height for i in range(len(components))
    )

    # Constraints: No overlap between components along the specified direction.
    for i, comp in enumerate(components):
        # If current rectangle has overlap constraints associated with it.
        for adj_comp in constraint_graph[comp]:
            j = components.index(adj_comp)

            if direction == 'horizontal':
                prob += variables[i] + comp.width <= variables[j]
            else:  # vertical
                prob += variables[i] + comp.height <= variables[j]

    # Constraints: Symmetry, origins of components on given axis should match.
    # For resolving horizontal symmetry constraints components need to be moved in vertical direction and vice versa.
    if direction == 'horizontal':
        # Dealing only with x coordinate.
        for pair in json_details['match_on_y']:
            left, right = pair[0], pair[1]

            for i, comp in enumerate(components):
                if comp.name == left:
                    found_left = comp
                    left_id = i

                if comp.name == right:
                    found_right = comp
                    right_id = i

            if found_left and found_right:
                prob += variables[left_id] + found_left.width - variables[right_id] <= 0.1

        # for pair in json_details['match_on_x']:
        #     up, down = pair[0], pair[1]

        #     for i, comp in enumerate(components):
        #         if comp.name == up:
        #             found_up = comp
        #             up_id = i

        #         if comp.name == down:
        #             found_down = comp
        #             down_id = i

        #     if found_up and found_down:
        #         prob += (variables[up_id] + found_up.width / 2) - (variables[down_id] + found_down.width / 2) <= 0.1
        
    else:
        # Dealing only with y coordinate.
        for pair in json_details['match_on_x']:
            up, down = pair[0], pair[1]

            for i, comp in enumerate(components):
                if comp.name == up:
                    found_up = comp
                    up_id = i

                if comp.name == down:
                    found_down = comp
                    down_id = i

            if found_up and found_down:
                prob += variables[down_id] + found_down.height - variables[up_id] <= 0.1

        # for pair in json_details['match_on_y']:
        #     left, right = pair[0], pair[1]

        #     for i, comp in enumerate(components):
        #         if comp.name == left:
        #             found_left = comp
        #             left_id = i

        #         if comp.name == right:
        #             found_right = comp
        #             right_id = i

        #     if found_left and found_right:
        #         prob += (variables[left_id] + found_left.height / 2) - (variables[right_id] + found_right.height / 2) <= 0.1

    print('Solving problem:')
    print(prob)

    prob.solve()

    if prob.status != 1:  # Optimal
        print('Info: No feasible solution found.')

    result = []

    for i, comp in enumerate(components):
        if direction == 'horizontal':
            result.append(
                Component(comp.name,
                    Rectangle(variables[i].value(), components[i].y1, components[i].width, components[i].height)
                )
            )
        else:
            result.append(
                Component(comp.name,
                    Rectangle(components[i].x1, variables[i].value(), components[i].width, components[i].height)
                )
            )

    return result
'''