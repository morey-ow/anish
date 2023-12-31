from manim import *

#here is how to make a graph
# of data points x=(x_0, x_1 ,..)
# y=(y_0, y_1, ...) 
# using .set_points_smoothly
# and .c2p(x, y)
class Example(Scene):
    def construct(self):
        x = [0 , 1, 2, 3,  4,  5,  6,  7]
        y = [0 , 1, 4, 9, 16, 25, 20, 10]
        X_MIN = min(x)-1
        X_MAX = max(x)+1
        Y_MIN = min(y)-1
        Y_MAX = max(y)+1
        STEP = 2

        axes = Axes(
            x_range=(X_MIN,X_MAX,STEP),
            y_range=(Y_MIN,Y_MAX,STEP),
            x_length=7,
            y_length=7
        )

        coords = [axes.c2p(_x,_y) for _x,_y in zip(x,y)]

        graph = VMobject(color=RED).set_points_smoothly(coords)

        self.add(axes,graph)
        self.wait()
        
#Here is how to plot a function using
# axes.plot
def function1(z):
    return z**3

class MyScene2(Scene):

# can't create a function to plot as the
# class function of the scene 

    def construct(self):
        axes=Axes(
            x_range=[-5,5],
            y_range=[-5,5,5],
            x_length=14,
            axis_config={'include_numbers': True}
        )
        self.add(axes)
        x1=[-5, 5, 0.1]
        graph1=axes.plot(lambda t: 2*t, x_range=x1,  use_vectorized=True)
        graph2=axes.plot(function1, x_range=x1)
        self.add(graph1, graph2)
        self.play(Transform(graph1, graph2), rate_func=linear)
        self.wait()
        