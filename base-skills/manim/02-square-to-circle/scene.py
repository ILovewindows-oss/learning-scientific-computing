# -*- coding: utf-8 -*-
""" Run with `manim -pql scene.py SquareToCircle`. """
# Manim base class.
from manim import Scene

# Manim actions.
from manim import Create
from manim import FadeOut
from manim import Transform

# Manim shapes.
from manim import Circle
from manim import Square

# Manim constants.
from manim import PINK
from manim import PI


class SquareToCircle(Scene):
    """ Scene for converting a square into a circle. """
    def construct(self):
        """ Construct and display the animation. """
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.rotate(PI / 4)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
