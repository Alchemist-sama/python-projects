def add(num1,num2):
    return num1+num2
def subtract(num1,num2):
    return num1-num2
def divide(num1,num2):
    return num1/num2
def multiply(num1,num2):
    return num1*num2

operators={"+":add,"-":subtract,"/":divide,"*":multiply}
cal = True
result = []
while cal == True:
    num1= float(input("enter the first number:\n"))
    op=input(" pick your operator :\n +\n-\n*\n/\n")
    num2= float(input("enter the Next number:\n"))
    if op in operators:
     cal_value= operators[op](num1,num2) 
     result.append(cal_value)
     print(cal_value)
    else : 
        print(" invalid operator")    
    more_cal=input(" do yoou want to continue the calculation with the previous value ?Y or N\n") 
    more_cal.upper()
    if more_cal ==   "Y" or "y":
        op=input(" pick your operator :\n +\n-\n*\n/\n")
        num2= float(input("enter the Next number:\n"))
        print(operators[op](result[-1],(num2)))
    else:
        print("\n"*20)  
        cal = False  
        break


