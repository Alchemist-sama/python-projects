print(r'''          ____...------------...____
               _.-"` /o/__ ____ __ __  __ \o\_`"-._
             .'     / /                    \ \     '.
             |=====/o/======================\o\=====|
             |____/_/________..____..________\_\____|
             /   _/ \_     <_o#\__/#o_>     _/ \_   \
             \_________\####/_________/
              |===\!/========================\!/===|
              |   |=|          .---.         |=|   |
              |===|o|=========/     \========|o|===|
              |   | |         \() ()/        | |   |
              |===|o|======{'-.) A (.-'}=====|o|===|
              | __/ \__     '-.\uuu/.-'    __/ \__ |
              |==== .'.'^'.'.====|
          jgs |  _\o/   __  {.' __  '.} _   _\o/  _|
              `""""-""""""""""""""""""""""""""-""""` ''')

print("welcome to treasure island . your mission is to find the treasure")
choice1 = input('you\'re at a cross road. where do you want to go ? type "left" or "right" \n').lower()
if choice1 == "left":
    choice2 = input('you\'ve come to a lake. there is an island in the middle of the lake. type "wait" to wait for a boat. type "swim" to swim across. \n').lower()
    if choice2 == "wait":
        choice3 = input("you arrive at the island unharmed. there is a house with 3 doors. one red, one yellow and one blue. which colour do you choose ? \n").lower()
        if choice3 == "red":
            print("it's a room full of fire. game over")
        elif choice3 == "blue":
            print("you enter a room of beasts. game over")
        elif choice3 == "yellow":
            print(r'''
                  


                            _.--.
                        _.-'_:-'||
                    _.-'_.-::::'||
               _.-:'_.-::::::'  ||
             .'`-.-:::::::'     ||
            /.'`;|:::::::'      ||_
           ||   ||::::::'     _.;._'-._
           ||   ||:::::'  _.-!oo @.!-._'-.
           \'.  ||:::::.-!()oo @!()@.-'_.|
            '.'-;|:.-'.&$@.& ()$%-'o.'\U||
              `>'-.!@%()@'@_%-'_.-o _.|'||
               ||-._'-.@.-'_.-' _.-o  |'||
               ||=[ '-._.-\U/.-'    o |'||
               || '-.]=|| |'|      o  |'||
               ||      || |'|        _| ';
               ||      || |'|    _.-'_.-'
               |'-._   || |'|_.-'_.-'
            jgs '-._'-.|| |' `_.-'
                    '-.||_/.-' you found the treasure! you win!''')
        else:
            print('''
                  you chose a door that doesn't exist. game over''')
    else:
        print("you get attacked by an angry trout. game over")
