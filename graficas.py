import matplotlib.pyplot as plot
import sympy as sp

# Variables or constants
t = sp.symbols('t')
a = sp.symbols('a')
w = sp.symbols('w')

# Warning: I was looking for information, and google says phi can be variable and also can be a constant
# for me is more comfortable to use it as a constant.
phi = 1.68

# This is just a comment to know if git works here!!


# Functions (v(t) and a(t))
function_vt = -1*(a * sp.sin(w * t + phi))
function_at = -1 * (a*w*w * sp.cos(w*t + phi))
function_xt = a*sp.cos(w*t + phi)


# Function to graph function
def get_list_of_points(function, start = -50, end = 50, step = 0.1):

    t_interval = []
    v_evalated_in_intervals = []

    i = start
    while True:
        t_interval.append(i)
        i += step
        if i > end:
            break

    for time in t_interval: # This is the x
        v = function.subs({a: 1, w: 1, t: time}) # This is the y
        v_evalated_in_intervals.append(v)

    return t_interval, v_evalated_in_intervals

def option_menu():
    print("1. v(t)")
    print("2. a(t)")
    print("3. x(t)")
    print("4. All functions")
    print("5. Another")
    option = input("Choose an option: ")
    return option

def main():
    option = option_menu()
    start = int(input("Start: "))
    end = int(input("End: "))
    step = float(input("Step: "))
    if option == "1":
        t, v = get_list_of_points(function_vt, start, end, step)
        plot.plot(t, v)
        plot.title("v(t)")
        plot.xlabel("t")
        plot.ylabel("v(t)")
        plot.savefig("v.png")
    if option == "2":
        t, a = get_list_of_points(function_at, start, end, step)
        plot.plot(t, a)
        plot.title("a(t)")
        plot.xlabel("t")
        plot.ylabel("a(t)")
        plot.savefig("a.png")
    if option == "3":
        t, x = get_list_of_points(function_xt, start, end, step)
        plot.plot(t, x)
        plot.title("x(t)")
        plot.xlabel("t")
        plot.ylabel("x(t)")
        plot.savefig("x.png")
    if option == "4":
        t, v = get_list_of_points(function_vt, start, end, step)
        plot.plot(t, v)
        t, a = get_list_of_points(function_at, start, end, step)
        plot.plot(t, a)
        t, x = get_list_of_points(function_xt, start, end, step)
        plot.plot(t, x)
        plot.title("All functions")
        plot.xlabel("t")
        plot.ylabel("f(t)")
        plot.savefig("all.png")

main()
