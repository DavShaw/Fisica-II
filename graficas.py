import matplotlib.pyplot as plot
import numpy as np
import sympy as sp

# Variables or constants
t = sp.symbols('t')
a = sp.symbols('a')
w = sp.symbols('w')
phi = sp.symbols('phi')

# Warning: I was looking for information, and google says phi can be variable and also can be a constant
# for me is more comfortable to use it as a constant.

phi = 1.618


# Functions (v(t) and a(t))
function_vt = -1*(a * sp.sin(w * t + phi))
function_at = -1 * (a*w*w * sp.cos(w*t + phi))
function_xt = a*sp.cos(w*t + phi)


# Function to graph function
def graph_function(function, title, x_title, y_title, outplut_name = "f.png"):
    t_interval = [i for i in range(-50, 50)]
    v_evalated_in_intervals = []
    for time in t_interval: # This is the x
        v = function.subs({a: 1, w: 1, phi: 0, t: time}) # This is the y
        v_evalated_in_intervals.append(v)
    plot.plot(t_interval, v_evalated_in_intervals)
    plot.title(title)
    plot.xlabel(x_title)
    plot.ylabel(y_title)
    plot.savefig(outplut_name)

# Warning: I tried to invoke the same function at the same time, but it get bugged!!!

#graph_function(function_vt, 'v(t)', 't', 'v', 'vt.png')
#graph_function(function_at, 'a(t)', 't', 'v', 'at.png')
#graph_function(function_xt, 'x(t)', 't', 'v', 'xt.png')
    