import numpy as np

funct1=np.poly1d([2,3,0,1])
print(funct1)
np.polyval(funct1, 2)

funct2=np.poly1d([1,0,1])
print(funct2)
funct2_dev=np.polyder(funct2)
np.polyval(funct2_dev, 1)
#%%
def newmans_method(funct,x_val,iterations=1):
    funct_val=np.polyval(funct,x_val)
    funct_der=np.polyder(funct)
    funct_der_val=np.polyval(funct_der, x_val)
    y=x_val-(funct_val/funct_der_val)
    try:
        if (str(y).split('.')[1][:2])==(str(x_val).split('.')[1][:2]):
            print(f'x_{iterations}={y}')
            print(f'The hundreths place is stablized, the value is {y}\nThe roots are: ')
            for i in np.roots(funct): print('x= '+str(i).strip('(').strip(")"))
            return
        print(f'x_{iterations}={y}')
    except:
        print(f'x_{iterations}={y}')
    return newmans_method(funct,y,iterations+1)

poly=(input('Input a polynomial in the form of "2x^3+4x^2+1" as "2, 4, 0, 1":')).split(',')
funct=[]

for i in poly:
    funct.append(float(i))

x_val=float(input('what is your initial number? '))
newmans_method(funct,x_val)




