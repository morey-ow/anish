#create analytic cont for square
from manim import *
class Square(Scene):
    def construct(self):

        #create Axes
        x_min, x_max =-16,16
        y_min, y_max=-9,9

        axes=Axes(
            x_range=(x_min, x_max),
            y_range=(y_min,y_max),
            x_axis_config={'include_numbers': False},
            y_axis_config={'include_numbers': False}
        )
        self.add(axes)
        
        #add horizontal lines and their squares
        lines=[]
        for y in range(-3, 4, 1):
            
            #create lines
            line=axes.plot_line_graph([1, x_max], [y,y] )
            lines.append(line.copy())
            self.add(line)

            #square (z -> z^2) the lines

            #compute square datapoints
            sq_value_xs=[]
            sq_value_ys=[]
            for x in np.arange(1,5, 1):
                sq_value=(x+1J*y)**2
                sq_value_xs.append(sq_value.real)
                sq_value_ys.append(sq_value.imag)
            
            
            #graph the square data
            #using set_points_smoothly
            points=[axes.c2p(xi, yi) for xi, yi in zip(sq_value_xs, sq_value_ys)]
            graph=VMobject(color=RED).set_points_smoothly(points)
            
            #graph2 is line connecting
            #datapoints, not as nice looking
            #as set points smoothly

            #graph2=axes.plot_line_graph(sq_value_xs, sq_value_ys)
            #graph2.set_color(GREEN)
            #self.add(graph2)
            self.play(Transform(line, graph))
        self.play(Create(VGroup(*lines)))
        self.wait


class ConjugateSquare(Scene):
    def construct(self):

        #create Axes
        x_min, x_max =-16,16
        y_min, y_max=-9,9

        axes=Axes(
            x_range=(x_min, x_max),
            y_range=(y_min,y_max),
            x_axis_config={'include_numbers': False},
            y_axis_config={'include_numbers': False}
        )
        self.add(axes)
        
        #add horizontal lines and their squares
        lines=[]
        for y in range(-3, 4, 1):
            
            #create lines
            line=axes.plot_line_graph([1, x_max], [y,y] )
            lines.append(line.copy())
            self.add(line)

            #square (z -> z^2) the lines

            #compute square datapoints
            sq_value_xs=[]
            sq_value_ys=[]
            for x in np.arange(1,5, 1):
                sq_value=(x+1J*y)**2
                sq_value_xs.append(sq_value.real)
                sq_value_ys.append(-sq_value.imag) # the minus sign is the conjugate
            
            
            #graph the square data
            #using set_points_smoothly
            points=[axes.c2p(xi, yi) for xi, yi in zip(sq_value_xs, sq_value_ys)]
            graph=VMobject(color=RED).set_points_smoothly(points)
            
            #graph2 is line connecting
            #datapoints, not as nice looking
            #as set points smoothly

            #graph2=axes.plot_line_graph(sq_value_xs, sq_value_ys)
            #graph2.set_color(GREEN)
            #self.add(graph2)
            self.play(Transform(line, graph))
        self.play(Create(VGroup(*lines)))
        self.wait
