# -*- coding: utf-8 -*-
""" Run with `manim -pql scene.py SquareAndCircle`. """
# Manim base class.
from manim import Scene

# Manim actions.
from manim import Create

# Manim shapes.
from manim import Circle
from manim import Square

# Manim constants.
from manim import BLUE
from manim import PINK
from manim import RIGHT


class SquareAndCircle(Scene):
    """ Scene for placing a square beside a circle. """
    def construct(self):
        """ Construct and display the animation. """
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.set_fill(BLUE, opacity=0.6)

        square.next_to(circle, RIGHT, buff=0.5)
        self.play(Create(circle), Create(square))
