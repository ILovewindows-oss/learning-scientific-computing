# -*- coding: utf-8 -*-
""" Run with `manim -pql scene.py AnimatedSquareToCircle`. """
# Manim base class.
from manim import Scene

# Manim actions.
from manim import Create
from manim import ReplacementTransform
from manim import Rotate

# Manim shapes.
from manim import Circle
from manim import Square

# Manim constants.
from manim import BLUE
from manim import GREEN
from manim import PINK
from manim import LEFT
from manim import RIGHT
from manim import PI


class AnimatedSquareToCircle(Scene):
    """ Scene for animated convertion of a square into a circle. """
    def construct(self):
        """ Construct and display the animation. """
        circle = Circle()
        square = Square()

        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(ReplacementTransform(square, circle)) 
        self.play(circle.animate.set_fill(PINK, opacity=0.5))


class DifferentRotations(Scene):
    """ Run with `manim -pql scene.py DifferentRotations`. """
    def construct(self):
        """ Construct and display the animation. """
        lsquare = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        rsquare = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)

        self.play(
            lsquare.animate.rotate(PI),
            Rotate(rsquare, angle=PI),
            run_time=2
        )
        self.wait()
