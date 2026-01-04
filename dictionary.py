dictionary ={}

while True:
    name = input("what is your name?\n")
    bid = int(input("enter your bid\n"))
    dictionary[name] = bid
    highest_value= max(dictionary.values())
    winner = max(dictionary,key =dictionary.get)
    ask = input("does anyone else want to bid ? yes or no\n")
    if ask == "yes":
        print("\n "*20)
    else:
        print(f"the winning bid is ${highest_value} sold to mr{winner} ")   
        break 

