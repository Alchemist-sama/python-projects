from coffee_data import menu, resources
def res_check(water_vol,coffee_vol, milk_vol,D_milk,D_water,D_coffee):
    if water_vol < D_water:
        return " not enough water "
    elif D_milk > milk_vol:
     return " not enough milk"
    elif D_coffee > coffee_vol:
        return ' not enough coffee'
    else:
        return 'ok'

#choice = None

   
        




#print (water_vol - milk_vol)
water_vol = resources['water']
coffee_vol = resources['coffee']
milk_vol = resources['milk']

s_list =['off','report']
machine_on = True 
while machine_on:
    choice = input(" what would you like ? (espresso/latte/cappuccino):")
    choice = choice.lower()
    drink_list = menu.keys()
    if choice not in menu and choice not in s_list :
        print("invalid drink")
        continue
    if choice ==  'report':
        print(f"water:{water_vol}ml, \ncoffee:{coffee_vol}g,\nmilk:{milk_vol}ml \n ")
        continue
    elif choice == 'off':
        machine_on = False
        break    
    drink = (menu[choice])
    drink_cost = float(drink['cost'])
    D_water=(drink['ingredients']['water'])
    D_milk = (drink['ingredients']['milk'])
    D_coffee = (drink['ingredients']['coffee'])
    checker= res_check(water_vol,coffee_vol, milk_vol,D_milk,D_water,D_coffee)
    if checker != 'ok':
        print(checker)
        continue

    if choice in   drink_list:
        print ('please insert your coins')
        quarters = int(input("how many quaters ? :"))
        quarters = float((0.25 * quarters))
        dimes = int(input("how many dimes ? :"))
        dimes = float((0.10 * dimes))
        pennies = int(input("how many pennies ? :"))
        pennies = float((0.01 * pennies))
        nickels = int(input("how many nickels ? :"))
        nickels = float ((0.05 * nickels))
        customer_total = (quarters + dimes + pennies +nickels )
        change =round(( customer_total - drink_cost),2)
        if customer_total >=drink_cost:
            print(f" the {choice} costs ${drink_cost} here is your change: ${change}")
            print(f" here is your {choice} ☕ enjoy!")
            water_vol -= D_water
            milk_vol -= D_milk
            coffee_vol -= D_coffee              
        else :
            print(f" the{choice} costs ${ drink_cost} you dont have enough , your money has been refunded")
        
                        