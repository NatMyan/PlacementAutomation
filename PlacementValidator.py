class PlacementValidator:
    def __init__(self):
        self.divergence_epsilon = 0.6
        self.max_height_epsilon = 0.5

    def check_general_placement(self, placement_lst):
        if placement_lst:
            sorted_placement = sorted(placement_lst, key=lambda comp: (comp.rectangle.y1, comp.rectangle.x1))
            for i, _ in enumerate(sorted_placement):
                for j, _ in enumerate(sorted_placement):
                    if i == j:
                        continue
                    rect1 = sorted_placement[i].rectangle
                    rect2 = sorted_placement[j].rectangle
                    x_overlap = not (rect1.x2 < rect2.x1 or rect1.x1 > rect2.x2)
                    y_overlap = not (rect1.y2 < rect2.y1 or rect1.y1 > rect2.y2)
                    if (x_overlap and y_overlap):
                        return False
            return True

    def check_match_on_x(self, placement_lst, json_details):
        if placement_lst and json_details:
            mismatch = -1
            for pair in json_details["match_on_x"]:
                left, right = pair[0], pair[1]
                found_left = next((item for item in placement_lst if item.name == left), None)
                found_right = next((item for item in placement_lst if item.name == right), None)
                if (not self.__intersects(found_left.rectangle, found_right.rectangle)):
                    mid_x_left = (found_left.rectangle.x1 + found_left.rectangle.x2) / 2
                    mid_x_right = (found_right.rectangle.x1 + found_right.rectangle.x2) / 2
                    mismatch += abs(mid_x_left - mid_x_right) + 1 / len(json_details["match_on_x"])
            return mismatch

    def check_match_on_y(self, placement_lst, json_details):
        if placement_lst and json_details:
            mismatch = -1
            for pair in json_details["match_on_y"]:
                up, down = pair[0], pair[1]
                found_up = next((item for item in placement_lst if item.name == up), None)
                found_down = next((item for item in placement_lst if item.name == down), None)
                if (not self.__intersects(found_up.rectangle, found_down.rectangle)):
                    mid_y_up = (found_up.rectangle.y1 + found_up.rectangle.y2) / 2
                    mid_y_down = (found_down.rectangle.y1 + found_down.rectangle.y2) / 2
                    mismatch += abs(mid_y_up - mid_y_down) + 1 / len(json_details["match_on_y"])
            return mismatch

    def check_important_paths(self, placement_lst, json_details):
        if placement_lst and json_details:
            path_coords = []
            for path in json_details["important_paths"]:
                path_coords.append([comp.rectangle for comp in placement_lst if comp.name in path])

            for path_crds in path_coords:
                y_coords = [abs(rect.y1 - rect.y2) / 2 for rect in path_crds]
                if max(y_coords) - min(y_coords) > self.max_height_epsilon:
                    return False
                elif max(y_coords) - min(y_coords) <= self.max_height_epsilon:
                    for i in range(len(path_crds) - 1):
                        current_rect = path_crds[i]
                        next_rect = path_crds[i + 1]
                        if current_rect.x2 != next_rect.x1:
                            return False
            return True

    def __intersects(self, rect1, rect2):
        x_overlap = not (rect1.x2 < rect2.x1 or rect1.x1 > rect2.x2)
        y_overlap = not (rect1.y2 < rect2.y1 or rect1.y1 > rect2.y2)
        return (x_overlap and y_overlap)

    def isPlacementValid(self, placement_lst, json_details):
        if placement_lst and json_details:
            return (self.check_general_placement(placement_lst) and
                    self.check_match_on_x(placement_lst, json_details) <= self.divergence_epsilon * len(placement_lst) and
                    self.check_match_on_y(placement_lst, json_details) <= self.divergence_epsilon * len(placement_lst) and
                    self.check_important_paths(placement_lst, json_details))
