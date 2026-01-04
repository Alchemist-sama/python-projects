import game_logo 
import random
from game_data import data


def compare(a,b):
   if  a['follower_count'] > b['follower_count']:
      return 'A'
   elif b['follower_count'] > a['follower_count']:
      return 'B'
   else:
      return 'TIE'
      
previous_choice = None
game_over = False
score = 0
a = random.choice(data)
while game_over is False:
    
    print(game_logo.logo)

   
    b = random.choice(data)
    while a == b:
       b = random.choice(data)

    print(f"Compare A: {a['name']}, a {a['description']} from {a['country']}")
    print(game_logo.vs)
    print(f"Against B: {b['name']}, a {b['description']}, from {b['country']}")
    choice = input('who has more followers A OR B')
    choice =choice.upper()
    correct_answer = compare(a,b)

    if choice == correct_answer:
      score +=1
      print(f'this is your current score: {score}')
      if correct_answer == 'B':
        a=b 
    else :
       print('you chose wrong')
       print(f' this is your final score: {score} ')
       game_over = True
    previous_choice = choice 
    