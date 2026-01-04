import random
player= int(input("enter your choice: 0 for rock, 1 for paper and 2 for scissors"))
com = random.randint(0,2)
#print("computer choice is:" + str(com))
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
images =[rock,paper,scissors]
if player >=0 and player <=2:
    print("you chose:")
    print(images[player])
    print("computer chose:")
    print(images[com])
if player == com:
    print("it's a draw")
elif player == 0 and com ==2 or player ==1 and com ==0 or player ==2 and com ==1:
    print("you win")
else:
    print("you lose")
