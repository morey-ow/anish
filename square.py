#create analytic cont for square
from manim import *
class Square(Scene):
    def construct(self):

        #create Axes
        x_min, x_max =-5,5
        y_min, y_max=-5,5

        axes=Axes(
            x_range=(-x_min**2,x_max**2),
            y_range=(y_min*2,y_max*2),
            x_axis_config={'include_numbers': True},
            y_axis_config={'include_numbers': True}
        )
        self.add(axes)
        
        #add horizontal lines

        
        lines=[]
        for y in range(y_min, y_max, 1):
            
            #create lines
            line=axes.plot_line_graph([1, x_max], [y,y] )
            lines.append(line)
            self.add(line)

            #square (z -> z^2) the lines

            #compute square datapoints
            sq_value_xs=[]
            sq_value_ys=[]
            for x in np.arange(1,x_max, 1):
                sq_value=(x+1J*y)**2
                #print(sq_value)
                sq_value_xs.append(sq_value.real)
                sq_value_ys.append(sq_value.imag)
            #print(sq_value_xs)
            #print(zeta_value_ys)
            
            #graph the square data
            points=[axes.c2p(xi, yi) for xi, yi in zip(sq_value_xs, sq_value_ys)]
            for i,v in enumerate(points):
                print(f'i={i}, point={v}')
            graph=VMobject(color=RED).set_points_smoothly(points)
            #graph2=axes.plot_line_graph(sq_value_xs, sq_value_ys)
            #graph2.set_color(GREEN)
            #self.add(graph2)
            self.play(Transform(line, graph))
            
