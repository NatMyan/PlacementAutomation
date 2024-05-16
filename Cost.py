from ComponentCollection import ComponentCollection

import math


class Cost:
    def __init__(self, components, json_details):
        if components and json_details:
            self.components = components
            self.json_details = json_details
        else:
            raise ValueError('Invalid args for constructor.')


    def __cost_overlap_2_rects(self, rect1, rect2):
        overlap_area = 0

        x_dist = (min(rect1.x2, rect2.x2) - max(rect1.x1, rect2.x1))
        y_dist = (min(rect2.y2, rect2.y2) - max(rect1.y1, rect2.y1))

        if x_dist > 0 and y_dist > 0:
            overlap_area = x_dist * y_dist
        
        return overlap_area
    

    def cost_overlap(self):
        area = 0
        sorted_placement = sorted(self.components, key=lambda comp: (comp.y1, comp.x1))

        for i, _ in enumerate(sorted_placement):
            for j, _ in enumerate(sorted_placement):
                if i == j:
                    continue

                rect1 = sorted_placement[i].rectangle
                rect2 = sorted_placement[j].rectangle
                
                overlap_area = self.__cost_overlap_2_rects(rect1, rect2)
                
                # overlap_area = 0
                #  
                # x_dist = (min(rect1.x2, rect2.x2) - max(rect1.x1, rect2.x1))
                # y_dist = (min(rect2.y2, rect2.y2) - max(rect1.y1, rect2.y1))
                #  
                # if x_dist > 0 and y_dist > 0:
                #     overlap_area = x_dist * y_dist

                # area += math.pow(10 * overlap_area, 2)
                
                area += overlap_area

        return area


    def cost_distance(self):
        distance = 0
        for i, _ in enumerate(self.components):
            for j, _ in enumerate(self.components):
                if i != j:
                    distance += self.__distance_between_rectangles(
                        self.components[i].rectangle, self.components[j].rectangle
                    )

        return distance


    def __distance_between_rectangles(self, rect1, rect2):
        if self.__rectangles_intersect(rect1, rect2):
            return 0

        # Horizontal distance.
        if rect2.x2 < rect1.x1:  # rect2 is to the left of rect1.
            dx = rect1.x1 - rect2.x2
        elif rect1.x2 < rect2.x1:  # rect2 is to the right of rect1.
            dx = rect2.x1 - rect1.x2
        else:  # Rectangles overlap on x-axis.
            dx = 0

        # Vertical distance.
        if rect2.y2 < rect1.y1:  # rect2 is above rect1.
            dy = rect1.y1 - rect2.y2
        elif rect1.y2 < rect2.y1:  # rect2 is below rect1.
            dy = rect2.y1 - rect1.y2
        else:  # Rectangles overlap on y-axis.
            dy = 0

        # Euclidean distance
        distance = math.sqrt((dx ** 2) + (dy ** 2))

        return distance


    def __rectangles_intersect(self, rect1, rect2):
        x_intersect = not (rect2.x1 > rect1.x2 or rect2.x2 < rect1.x1)
        y_intersect = not (rect2.y1 > rect1.y2 or rect2.y2 < rect1.y1)

        return x_intersect and y_intersect
    
    
    def __one_cost_match_on_x(self, pair):
        mismatch = 0
        up, down, center = pair[0], pair[1], 0 # i # pair[2]

        found_up = next((item for item in self.components if item.name == up), None)
        found_down = next((item for item in self.components if item.name == down), None)

        if found_up and found_down:
            mid_x_up = (found_up.x1 + found_up.x2) / 2
            mid_x_down = (found_down.x1 + found_down.x2) / 2

            # mismatch += math.pow(mid_x_up + mid_x_down - 2 * center, 2) + math.pow(found_up.y1 - found_down.y2, 2)
            overlap = self.__cost_overlap_2_rects(found_up, found_down)
            # full_overlap = self.cost_overlap()
            
            if (mid_x_up < mid_x_down):
                mismatch += abs(mid_x_up - mid_x_down) + overlap # + full_overlap # + 1/len(json_details["match_on_x"])
            else:
                mismatch += 5 * (abs(mid_x_up - mid_x_down) + overlap) # + full_overlap)
        
        return mismatch
    
    
    # def cost_match_on_x(self):
    def cost_match_on_x(self, full_overlap):
        mismatch = 0
        
        i = 0
        for pair in self.json_details['match_on_x']:
            up, down, center = pair[0], pair[1], 0 # i # pair[2]

            found_up = next((item for item in self.components if item.name == up), None)
            found_down = next((item for item in self.components if item.name == down), None)

            if found_up and found_down:
                mid_x_up = (found_up.x1 + found_up.x2) / 2
                mid_x_down = (found_down.x1 + found_down.x2) / 2

                # mismatch += math.pow(mid_x_up + mid_x_down - 2 * center, 2) + math.pow(found_up.y1 - found_down.y2, 2)
                overlap = self.__cost_overlap_2_rects(found_up, found_down)
                # full_overlap = self.cost_overlap()
                
                if (mid_x_up < mid_x_down):
                    mismatch += abs(mid_x_up - mid_x_down) + overlap # + full_overlap # + 1/len(json_details["match_on_x"])
                else:
                    mismatch += 5 * (abs(mid_x_up - mid_x_down) + overlap) # + full_overlap)
                    
            i += 1

        return mismatch

    def __one_cost_match_on_y(self, pair):
        mismatch = 0
        left, right = pair[0], pair[1]

        found_left = next((item for item in self.components if item.name == left), None)
        found_right = next((item for item in self.components if item.name == right), None)

        if found_left and found_right:
            mid_y_left = (found_left.y1 + found_left.y2) / 2
            mid_y_right = (found_right.y1 + found_right.y2) / 2
            
            overlap = self.__cost_overlap_2_rects(found_left, found_right)
            # full_overlap = self.cost_overlap()
            
            if mid_y_left < mid_y_right:
                mismatch += abs(mid_y_left - mid_y_right) + overlap # + full_overlap # + 1/len(json_details["match_on_y"])
            else:
                mismatch += 5 * (abs(mid_y_left - mid_y_right) + overlap) # + full_overlap)
        
        return mismatch
        
    # def cost_match_on_y(self):
    def cost_match_on_y(self, full_overlap):
        mismatch = 0

        for pair in self.json_details['match_on_y']:
            left, right = pair[0], pair[1]

            found_left = next((item for item in self.components if item.name == left), None)
            found_right = next((item for item in self.components if item.name == right), None)

            if found_left and found_right:
                mid_y_left = (found_left.y1 + found_left.y2) / 2
                mid_y_right = (found_right.y1 + found_right.y2) / 2
                
                overlap = self.__cost_overlap_2_rects(found_left, found_right)
                # full_overlap = self.cost_overlap()
                
                if mid_y_left < mid_y_right:
                    mismatch += abs(mid_y_left - mid_y_right) + overlap # + full_overlap # + 1/len(json_details["match_on_y"])
                else:
                    mismatch += 5 * (abs(mid_y_left - mid_y_right) + overlap) # + full_overlap)
                    
        return mismatch
    
    
    def __important_paths(self):
        imp_paths_rects = []

        for path in self.json_details['important_paths']:
            filtered_components = []

            for name in path:
                # Order matters.
                for comp in self.components:
                    if comp.name == name:
                        filtered_components.append(comp)
                        break

            if len(filtered_components) != len(path):
                raise ValueError(f'Invalid transistors in path: {path}')

            imp_paths_rects.append(filtered_components)
        
        return imp_paths_rects
            

    def cost_important_paths(self):
        imp_paths_rects = self.__important_paths()
        
        total_slopes = 0
           
        for path_rects in imp_paths_rects:
            for i in range(len(path_rects) - 1):
                # Get the origin of the first.
                x_first = (path_rects[i].x1 + path_rects[i].x2) / 2
                y_first = (path_rects[i].y1 + path_rects[i].y2) / 2
                
                # Get the origin of the second.
                x_second = (path_rects[i + 1].x1 + path_rects[i + 1].x2) / 2
                y_second = (path_rects[i + 1].y1 + path_rects[i + 1].y2) / 2
                    
                # Check to avoid zero division or excessively large values when dividing.
                # if abs(x_first - x_second) <= 0.1:
                #     slope = 0
                # else:
                #     slope = math.pow(10 * abs(y_first - y_second) / abs(x_first - x_second), 2)
                
                if abs(y_first - y_second) <= 0.01:
                    slope = 0
                else:
                    # slope = math.pow(10 * abs(x_first - x_second) / abs(y_first - y_second), 2)
                    slope = abs(x_first - x_second) / abs(y_first - y_second)

                total_slopes += slope

        return total_slopes
    
    
    def cost_bounding_rect_area(self):
        if self.components:
            min_x1 = min(comp.rectangle.x1 for comp in self.components)
            max_x2 = max(comp.rectangle.x2 for comp in self.components)
            min_y1 = min(comp.rectangle.y1 for comp in self.components)
            max_y2 = max(comp.rectangle.y2 for comp in self.components)

            x = (max_x2 - min_x1)
            y = (max_y2 - min_y1)   
            
            return max(x, y) - min(x, y)     
        

    def cost_function(self, points, verbose=False):
        assert len(points) == 2 * len(self.components)

        comp_coll = ComponentCollection(self.components)
        # Keep components' initial coordintates intact.
        res_points = comp_coll.transform_to_list()
        # Update with new set of coordinates for cost calculation.
        comp_coll.update_from_list(points)

        overlap = self.cost_overlap()
        distance = self.cost_distance()

        x_match = self.cost_match_on_x(overlap)
        y_match = self.cost_match_on_y(overlap)
        
        importants = self.cost_important_paths()
        
        bound_rect = self.cost_bounding_rect_area()
        
        # total = 5 * overlap + 0.1 * distance + 2 * x_match + 2 * y_match + 1.5 * importants
        total = 5 * overlap + 0.1 * distance + 3 * x_match + 3 * y_match + 2 * importants + bound_rect

        # Restore components coordinates to initial values.
        comp_coll.update_from_list(res_points)
        
        if verbose:
            print('Info: Fitness details: overlap: {}, distance (0.1x): {}, x_match: {}, y_match: {}, importants: {}, bound_rect: {}, total: {}'.format(
                overlap, distance, x_match, y_match, importants, bound_rect, total
            ))

        return total
    
    
'''def cost_overlap(self):
        # Event points contain the x-coordinates of rectangle boundaries
        events = []
        for comp in self.components:
            events.append((comp.rectangle.x1, comp.rectangle.y1, 'start', comp.rectangle))
            events.append((comp.rectangle.x2, comp.rectangle.y2, 'end', comp.rectangle))
        events.sort()  # Sort event points based on x-coordinate

        active_rectangles = []
        overlap_area = 0
        prev_x = events[0][0]

        for x, y, event_type, rect in events:
            # Calculate the area contributed by active rectangles up to the current event point
            width = x - prev_x
            height = 0
            for active_rect in active_rectangles:
                height += max(0, min(active_rect.y1 + active_rect.height, y) - max(active_rect.y1, rect.y1))
            overlap_area += width * height

            # Update active rectangles based on the event type
            if event_type == 'start':
                active_rectangles.append(rect)
                active_rectangles.sort(key=lambda r: r.y1, reverse=True)
            else:
                active_rectangles.remove(rect)

            prev_x = x

        return overlap_area'''