import random
import math

def cooling_temp(temp, alpha):
    """Cooling function"""
    return temp * alpha


def fun(x):
    """Function to minimize"""
    return x**2 + 4*x + 4

def hiperparameter(d):
    return d

def annealing(fun, temp, alpha):
    x = fun(random.randint(0, 100))
    temp_max = temp
    print(f"Current x: {x}, Current temp: {temp}, Current fun(x): {fun(x)}")
    while temp > 0.001:
        new_x = x + hiperparameter(x*2) * (temp / temp_max) * random.uniform(-1, 1)
        delta = fun(new_x) - fun(x)
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temp):
            x = new_x
        temp = cooling_temp(temp, alpha)
        print(f"Current x: {x}, Current temp: {temp}, Current fun(x): {fun(x)}")


# start Value
Temprature = 1000
Cooling_factor = 0.999

annealing(fun, Temprature, Cooling_factor)


