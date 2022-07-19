# -*- coding: utf-8 -*-
""" Run with `manim -pql scene.py <scene-name>`. """
# Manim base class.
from manim import Animation
from manim import Scene

# Manim actions.
from manim import Transform

# Manim interpolation.
from manim import linear

# Manim shapes.
from manim import DecimalNumber
from manim import Text
from manim import Circle
from manim import Square
from manim import Triangle
from manim import Dot
from manim import Line

# Manim constants (colors).
from manim import BLACK
from manim import BLUE
from manim import DARK_BLUE
from manim import GREEN
from manim import GREEN_A
from manim import GREEN_D
from manim import ORANGE
from manim import PINK
from manim import RED
from manim import WHITE
from manim import YELLOW

# Manim constants (coordinates).
from manim import ORIGIN
from manim import LEFT
from manim import RIGHT
from manim import DOWN
from manim import UP
from manim import UR

# Other packages.
import numpy as np


class Shapes(Scene):
    """ Illustrates directional placement of shapes. """
    def construct(self):
        """ Construct and display the animation. """
        circle1 = Circle().shift(2 * LEFT)
        circle2 = Circle().shift(2 * RIGHT)
        square1 = Square().shift(2 * UP)
        square2 = Square().shift(2 * DOWN)
        triangle = Triangle()

        self.add(circle1, circle2, square1, square2, triangle)
        self.wait(1)


class MobjectPlacement(Scene):
    """ Illustrates relative placement of Mobject's. """
    def construct(self):
        """ Construct and display the animation. """
        circle = Circle()
        square = Square()
        triangle = Triangle()

        circle.move_to(LEFT * 2)
        square.next_to(circle, LEFT)
        triangle.align_to(circle, LEFT)

        self.add(circle, square, triangle)
        self.wait(1)


class FiniteVolumeScheme(Scene):
    """ Illustrates creation of a FVM stencil. """
    def construct(self):
        """ Construct and display the animation. """
        animated = True
        n_cells = 5 - 1

        for k in np.arange(-n_cells, n_cells + 1, 2):
            square = Square().set_fill(BLACK, opacity=1.0)
            dot = Dot()

            if animated:
                self.play(
                    square.animate.shift(LEFT * k),
                    dot.animate.shift(LEFT * k)
                )
                self.play(
                    square.animate.set_fill(RED),
                    dot.animate.set_fill(BLACK),
                    run_time=2
                )
            else:
                self.add(
                    square.shift(LEFT * k), 
                    dot.shift(LEFT * k)
                )

        self.wait(5)


class MobjectStyling(Scene):
    """ Illustrates the use of styles. """
    def construct(self):
        """ Construct and display the animation. """
        circle = Circle().shift(LEFT + UP)
        square = Square().shift(UP + RIGHT)
        triangle = Triangle().shift(RIGHT + 0.5 * DOWN)

        circle.set_stroke(color=GREEN, width=20)
        square.set_fill(YELLOW, opacity=0.5)
        triangle.set_fill(PINK, opacity=0.9)

        # You can play with this for Z-order control.
        self.add(circle, square, triangle)
        self.wait(1)


class Count(Animation):
    """ Create a counter to interpolate decimal numbers. """
    def __init__(self, number: DecimalNumber, 
                 start: float, end: float, **kwargs) -> None:
        super().__init__(number,  **kwargs)
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        """ Set value of DecimalNumber according to alpha. """
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)


class CountingScene(Scene):
    """ Illustrate the use of a custom animation. """
    def construct(self):
        """ Construct and display the animation. """
        number = DecimalNumber().set_color(WHITE).scale(5)

        # Add an updater to keep the DecimalNumber centered 
        # as its value changes across iterations.
        number.add_updater(lambda number: number.move_to(ORIGIN))

        self.add(number)
        self.wait()

        # Play the Count Animation to count from 0 to 100 in 4 seconds
        self.play(Count(number, 0, 100), run_time=4, rate_func=linear)
        self.wait()


class MobjectCoordinates(Scene):
    """ Illustrates coordinates access and more features. """
    def construct(self):
        """ Construct and display the animation. """
        self.camera.background_color = DARK_BLUE

        p1 = [-1, -1, 0]
        p2 = [+1, -1, 0]
        p3 = [+1, +1, 0]
        p4 = [-1, +1, 0]

        line12 = Line(p1, p2)
        line23 = Line(p2, p3)
        line34 = Line(p3, p4)

        a = line12\
            .append_points(line23.points)\
            .append_points(line34.points)

        x0 = a.get_start()
        x2 = a.get_end()
        x1 = a.get_center()
        xt = a.get_top()
        xb = a.get_bottom()
        xr = a.point_from_proportion(0.5)

        point0 = [f"{x:+.1f}" for x in np.round(x0, 2).tolist()]
        point2 = [f"{x:+.1f}" for x in np.round(x2, 2).tolist()]
        point1 = [f"{x:+.1f}" for x in np.round(x1, 2).tolist()]

        conf = dict(font_size=24, font="Monospace", should_center=False)
        text0 = Text(f"a.get_start()  = {point0}", **conf)
        text2 = Text(f"a.get_end()    = {point2}", **conf)
        text1 = Text(f"a.get_center() = {point1}", **conf)

        self.add(text0.set_color(YELLOW).to_edge(UR))
        self.add(text2.set_color(RED).next_to(self.mobjects[-1], DOWN))
        self.add(text1.set_color(BLUE).next_to(self.mobjects[-1], DOWN))

        self.add(Dot(x0).scale(2).set_color(YELLOW))
        self.add(Dot(x2).scale(2).set_color(RED))
        self.add(Dot(xt).scale(2).set_color(GREEN_A))
        self.add(Dot(xb).scale(2).set_color(GREEN_D))
        self.add(Dot(x1).scale(2).set_color(BLUE))
        self.add(Dot(xr).scale(2).set_color(ORANGE))
        self.add(*[Dot(x) for x in a.points])
        self.add(a)


class ExampleRotation(Scene):
    """ Illustrates manual manipulation of object coordinates. """
    def construct(self):
        """ Construct and display the animation. """
        rotate = True

        self.camera.background_color = WHITE
        m1a = Square().set_color(RED).shift(LEFT)
        m1b = Circle().set_color(RED).shift(LEFT)
        m2a= Square().set_color(BLUE).shift(RIGHT)
        m2b= Circle().set_color(BLUE).shift(RIGHT)

        if rotate:
            points = m2a.points
            points = np.roll(points, int(len(points)/4), axis=0)
            m2a.points = points

        self.play(
            Transform(m1a, m1b),
            Transform(m2a, m2b), 
            run_time=2
        )

