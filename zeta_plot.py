#%%
from manim import *

import numpy as np

#%%
def get_data(filename):
    with open(filename, 'r') as f:
        data=f.readlines()
    
    #print(len(data))
    num_points=len(data)-1
    #s=np.zeros(num_points, dtype=complex)
    #zetas=np.zeros(num_points, dtype=complex)
    s=[]
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
