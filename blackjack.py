import random

play = True
def deal_cards():
     player_card=random.sample(cards,2)
     com_card=random.sample(cards,2)
     return random.sample(cards,2)

def compare(player_card,com_card):
          if p_card > 21 and len(player_card)>2:
                return ("unlucky boy try again")
          elif p_card == c_card :
                return (" draw")
          elif p_card > 21 and c_card < 21 :
                return(" you lose! computer wins")    
          elif c_card > 21 :
                return(" computer went over ! you win") 
          elif p_card == 0 :
                 return (" Black jack , you win")
          elif c_card ==0:
                 return(" you lose computer has the black jack")
          else: 
                 return("you win")
               
def calculate_scores(hand):
      if p_card == 21 and len(player_card)==2:
                return 0
      elif c_card == 21 and len(com_card)==2:
                return 0
      elif 11 in player_card and p_card > 21:
             player_card.remove(11)
             player_card.append(1)
             return player_card 
      elif 11 in com_card and c_card > 21:
             com_card.remove(11)
             com_card.append(1)
             return player_card 
      
                
                
     
while play is True:
    cards = [11,2,3,4,5,6,7,8,9,10,10,10,10]
    player_card=[]
    com_card=[]
    choice=input("do you want to play a game of black jack ? Y OR N")
    choice= choice.upper()
    if choice == "Y":
        player_card=deal_cards()
        com_card = deal_cards()
        p_card = sum(player_card)
        c_card=sum(com_card)    
        print(f"your cards: {player_card} sum is {p_card}")            
        print(f"computer's first cards: {com_card[0]} sum is {c_card}")
        stand=input("do you want to stand or hit ? S OR H") 
        stand=stand.upper()
        if stand == "h":
            player_card.append(deal_cards())
            p_card =sum(player_card)
        elif  stand =="s":
           while c_card < 17:
                 com_card.append(deal_cards())
                 c_card = sum(com_card)
            
                 
        
        player= calculate_scores(player_card)
        com=calculate_scores(com_card)
        result=compare(player_card,com_card)
        print(f"{result} your cards are {player_card} and computer's cards are {com_card}")
    else:
        play = False
        break    


   
