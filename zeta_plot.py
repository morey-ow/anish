#%%
from manim import *

import numpy as np
from zeta import zeta

#%%
def get_data(filename):
    with open(filename, 'r') as f:
        data=f.readlines()
    
    #print(len(data))
    num_points=len(data)-1
    #s=np.zeros(num_points, dtype=complex)
    #zetas=np.zeros(num_points, dtype=complex)
    #s will be the y-coord of points on critical line
    s=[] 

    #zetas =zeta(s) will hold values of zeta evaluated at
    zetas=[]
    for row in range(1, num_points):
        print(row, data[row])
        a, b=data[row].split()
        s.append(complex(a))
        zetas.append(complex(b))
    #print(s)
    #print(zetas)
    return np.asarray(s, dtype=complex), np.asarray(zetas, dtype=complex)



#%%
class ZetaCritical(Scene):
    def norm(self, c):
        return np.sqrt(c.real**2 + c.imag**2)

    def plot_zeros(self, s, zetas, axes):
        norm=np.vectorize(self.norm)
        zeros=s[norm(zetas)<0.08]
        print('Here are the zeros', zeros)
        self.add(VGroup(*[Dot(axes.c2p(0.5,zero)) for zero in zeros.imag]))
        self.add(VGroup(*[Tex(f'{round(zero,2)}').move_to(axes.c2p(0.8,zero)).scale(0.6) for zero in zeros.imag]))


    def plot_complex(self, data, axes):
        return axes.plot_line_graph(data.real, data.imag, add_vertex_dots=False)

    def construct(self):
        s, zetas =get_data('zeta50-1.csv')
        axes_left=Axes(
            x_range=[0,1],
            y_range=[0,50,5],
            x_length=2,
            axis_config={'include_numbers': True}
        )
        axes_right=Axes(
            x_range=[-3,3],
            y_range=[-3,3],
            axis_config={'include_numbers': True}
        )
        s_tex=MathTex('s')
        t=ValueTracker(0).align_to(axes_left, UP)
        zeta_tex=MathTex('\\zeta(s)').move_to(3*UR)
        axes=VGroup(axes_left, axes_right).arrange(RIGHT).scale(0.9)
        one_half=MathTex('\\frac{1}{2}').next_to(axes_left.x_axis.n2p(0.5),DOWN)
        s_tex=MathTex('s').next_to(axes_left.y_axis.n2p(50),RIGHT)
        self.add(axes, s_tex, zeta_tex, one_half)

        graph_left=self.plot_complex(s, axes_left)
        graph_right=self.plot_complex(zetas, axes_right)
        self.plot_zeros(s, zetas, axes_left)

        self.play(Create(VGroup(graph_left,graph_right), run_time=4, rate_func=linear))
        #self.play(Create(graph_right, run_time=8, rate_func=linear))
        
        #print('Here is zeros imaginary parts')
        #print(zeros.imag)
        #print([axes_left.c2p(0.5,zero) for zero in zeros.imag])
        self.wait(1)

# %%
class analytic_cont_zeta(Scene):
    def construct(self):

        #create Axes
        x_min, x_max =0,2
        y_min, y_max=-2,2

        axes=Axes(
            x_range=(x_min,x_max),
            y_range=(y_min,y_max),
            x_axis_config={'include_numbers': True},
            y_axis_config={'include_numbers': True}
        )
        self.add(axes)
        
        # add horizontal lines

        step_size=3
        num_lines=(y_max-y_min)
        lines=[]
        for y in range(y_min, y_max, step_size):
            line=axes.plot_line_graph([1, x_max], [y,y] )
            lines.append(line)
            #self.add(line)
        self.add(*lines)

        #compute zeta(line) for various lines
        zeta_lines=[]
        for y in  np.arange(-5.5, 5, 1): #np.arange(y_min, y_max, step_size):
            zeta_value_xs=[]
            zeta_value_ys=[]
            for x in np.arange(1.001, 5, 1):
                zeta_value=zeta(x+1J*y)
                zeta_value_xs.append(zeta_value.real)
                zeta_value_ys.append(zeta_value.imag)
            #print(zeta_value_xs)
            #print(zeta_value_ys)
            points=[axes.c2p(x, y) for x, y in zip(zeta_value_xs, zeta_value_ys)]
            graph=VMobject(color=RED).set_points_smoothly(points)
            graph2=axes.plot_line_graph(zeta_value_xs, zeta_value_ys)
            label=Text(f'{y}').next_to(graph2)
            graph2.set_color(GREEN)
            #self.add(graph2)
            self.add(graph)
            #self.play(Create(graph))

# %%
