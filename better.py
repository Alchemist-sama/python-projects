import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

# Store in a list
game_images = [rock, paper, scissors]

# Player choice
player = int(input("Enter your choice: 0 for Rock, 1 for Paper, 2 for Scissors:\n"))

if player >= 0 and player <= 2:
    print("You chose:")
    print(game_images[player])

    # Computer choice
    com = random.randint(0, 2)
    print("Computer chose:")
    print(game_images[com])

    # Decide winner
    if player == com:
        print("It's a draw")
    elif (player == 0 and com == 2) or (player == 1 and com == 0) or (player == 2 and com == 1):
        print("You win!")
    else:
        print("You lose!")
else:
    print("You entered an invalid number. You lose!")
