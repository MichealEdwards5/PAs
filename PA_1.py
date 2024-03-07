import random
import time
from random import choice
from tabulate import tabulate

def random_1D_axis(steps):
    percentage_reached_origin=0
    
    for i in range(100):
        x_axis=0
        for i in range(steps):
            x_axis+=choice([-1,1])
            if x_axis==0:
                percentage_reached_origin+=1
                break

    return f'%{percentage_reached_origin}'

def random_2D_axis(steps):
    percentage_reached_origin=0
    axes=['x','y']
    
    for i in range(100):
        x_axis=0
        y_axis=0
        for i in range(steps):
            axis=choice(axes)
            
            if axis=='x':
                x_axis+=choice([-1,1])
            else:
                y_axis+=choice([-1,1])
    
            if x_axis == 0 and y_axis == 0:
                percentage_reached_origin+=1
                break

    return f'%{percentage_reached_origin}'

def random_3D_axis(steps):
    percentage_reached_origin=0
    axes=['x','y','z']
    
    for i in range(100):
        x_axis=0
        y_axis=0
        z_axis=0
        for i in range(steps):
            axis=choice(axes)
            
            if axis=='x' :
                x_axis+=choice([-1,1])
            elif axis=='y' :
                y_axis+=choice([-1,1])
            else:
                z_axis+=choice([-1,1])
    
            if x_axis == 0 and y_axis == 0 and z_axis == 0:
                percentage_reached_origin+=1
                break
    return f'%{percentage_reached_origin}'

def main():
    steps=[20,200,2000,20000,200000,2000000]
    one_D_data=['1D']
    two_D_data=['2D']
    three_D_data=['3D']
    three_D_times=['3D Computation Time:']
    
    for i in steps:
        rand_1D=random_1D_axis(i)
        rand_2D=random_2D_axis(i)
        
        start_time=time.time()
        rand_3D=random_3D_axis(i)
        end_time=time.time()
        three_D_func_time=end_time-start_time
        
        one_D_data.append(rand_1D)
        two_D_data.append(rand_2D)
        three_D_data.append(rand_3D)
        three_D_times.append(f'{three_D_func_time:.2f} s')
        
    
    total_data=[one_D_data,two_D_data,three_D_data,three_D_times]
    headers=['# of steps',steps[0],steps[1],steps[2],steps[3],steps[4],steps[5]]
    
    return print(tabulate(total_data, headers, tablefmt="grid"))

main()