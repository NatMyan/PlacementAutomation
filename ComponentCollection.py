class Rectangle:
    def __init__(self, x1, y1, width, height):
        self.x1 = x1  # Left
        self.y1 = y1  # Bottom
        self.width = width
        self.height = height

    @property
    def x2(self):
        return self.x1 + self.width

    @property
    def y2(self):
        return self.y1 + self.height

    def __repr__(self):
        return f'{self.__class__.__name__}(bottomLeft=({self.x1}, {self.y1}), width={self.width}, height={self.height})'


# -----------------------------------------------------------------------------------------------------
class Component:
    def __init__(self, name, rectangle):
        assert isinstance(rectangle, Rectangle)
        self.name = name
        self.rectangle = rectangle

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name}, {self.rectangle})'

    def __getattr__(self, attr):
        return getattr(self.rectangle, attr)

    def update(self, x1, y1):
        self.rectangle.x1 = x1
        self.rectangle.y1 = y1

# -----------------------------------------------------------------------------------------------------
class ComponentCollection:
    def __init__(self, components):
        self.components = []

        for component in components:
            assert isinstance(component, Component)

            self.components.append(component)


    def transform_to_list(self):
        points = []

        for component in self.components:
            points.append(component.rectangle.x1)
            points.append(component.rectangle.y1)

        return points


    def update_from_list(self, points):
        assert len(points) == 2 * len(self.components)

        for i in range(len(self.components)):
            self.components[i].update(points[i * 2], points[i * 2 + 1])


    @staticmethod
    def make_coords_positive(components):
        left_most = float('inf')
        bottom_most = float('inf')

        for comp in components:
            if comp.x1 < left_most:
                left_most = comp.x1

            if comp.y1 < bottom_most:
                bottom_most = comp.y1

        for comp in components:
            comp.update(
                comp.x1 + abs(left_most),
                comp.y1 + abs(bottom_most)
            )


    def __repr__(self):
        msg = f'{self.__class__.__name__}\n'

        for i, component in enumerate(self.components):
            msg += f'    {component}'

            if i != len(self.components) - 1:
                msg += '\n'

        return msg

