# -*- coding: utf-8 -*-
""" Run with `manim -pql scene.py UsingSections`. 

You can also add the `--save_sections` flag to the command to
output video for individual sections.
"""
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


class UsingSections(Scene):
    """ Illustration of how to use sections. """
    def construct(self):
        """ Construct and display the animation. """
        self.next_section("Part I")
        circle = Circle().shift(LEFT)
        square = Square()

        circle.set_fill(PINK, opacity=0.5)
        square.set_fill(BLUE, opacity=0.6)

        square.next_to(circle, RIGHT, buff=0.5)
        self.play(Create(circle), Create(square))

        self.clear()
        self.wait()

        self.next_section("Part II")
        lsquare = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        rsquare = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)

        self.play(
            lsquare.animate.rotate(PI),
            Rotate(rsquare, angle=PI),
            run_time=2
        )
        self.wait()
