from Cost import Cost
from ComponentCollection import ComponentCollection
from numdifftools import Gradient


class MinimizePlacement:
    def __init__(self, components, json_details):
        if components and json_details:
            self.components = components
            self.repetitions = 0.0
            self.cost = Cost(self.components, json_details)
            

    def minimize(self, num_iterations=2000, learning_rate=0.001):
        if self.components:
            gradient = Gradient(self.cost.cost_function)

            for i in range(num_iterations):
                comp_coll = ComponentCollection(self.components)
                points = comp_coll.transform_to_list()

                # len(derivative) == len(points)
                derivative = gradient(points)

                for j in range(len(points)):
                    points[j] = points[j] - learning_rate * derivative[j]

                comp_coll.update_from_list(points)

                new_cost = self.cost.cost_function(points, verbose=True)
                print(f'Iteration: {i + 1}/{num_iterations}, total cost: {new_cost}')

            return self.components
