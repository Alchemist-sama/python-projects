print("welcome to python pizza deliveries!")
size = input("what size of pizza do you want ? s,m,L?")
pepperoni= input("do you want pepperoni on your pizza ? Y/N")
extra_cheese = input("do you want extra cheese ? Y OR N")
''' s= 15, m =20, l=25, pep for small piz = 2, for m and l = 3 , cheese =1'''
bill =0

if size == "s" :
  bill += 15
elif size == "m":
  bill += 20
else:
  bill += 25
if pepperoni == "Y":
    if size == "s":
       bill += 2
    else :
       bill += 3
if extra_cheese == "Y":
   bill +=1          
print(f"your total bill is ${bill}")