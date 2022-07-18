# -*- coding: utf-8 -*-
""" Run with `manim -pql scene.py CreateCircle`. """
from manim import Scene
from manim import Create
from manim import Circle
from manim import PINK


class CreateCircle(Scene):
    """ Scene for creating a circle. """
    def construct(self):
        """ Construct and display the animation. """
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        self.play(Create(circle))
