
num = 45

def easy():
    guess=None
    trys = 10
    while trys > 0 and not trys == 0 and not guess == num:
        print(f"you have {trys} attempts left to guess the number")
        guess = int(input(" make a guess :\n"))
        trys-=1
        print( compare(num,guess,trys))
        if trys== 0 :
         return ' you are out of guesses'

           
    return trys,guess   

def hard():
    trys = 5
    guess = None
    while trys > 0  and not guess == num:
        print ("hard mode running")
        print(f"you have {trys} attempts left to guess the number")
        guess = int(input('make a guess:\n'))
        trys-=1
        print( compare(num,guess,trys))
        
    return trys,guess 

def compare(num,guess, trys):
    if  guess == num :
        return ' you guessed correctly , you win'
    
    if num > guess:
        result= ' guess too low ! try again '
    else :
        result='guess too high ! try again'
   
    
    if trys== 0 :
         return ' you are out of guesses'
    return result     
    
will_play = True       

while will_play:
    play = input(' do you want to play a game ?')
    play = play.lower()
    if play == 'y':
        print(" welcome to the number guessing game!\n im thinking of a number between 1 to 100")

        diff= input("choose a difficulty : EASY OR HARD\n")
        diff = diff.lower().strip()
        if diff== 'easy':
            easy()  
        elif diff == 'hard':
            hard()
        else :
            print(" print you must pick a difficulty")    
            
    else:
        will_play = False
        break        

