import random
word_list = ['aardvark','babbon','camel']
guesses = []
game_over = False 
chosen_word = random.choice(word_list)
print(chosen_word)
stages = [
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """,  # 0 lives left (LOSE)

    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,  # 1 life left

    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,  # 2 lives left

    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,  # 3 lives left

    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,  # 4 lives left

    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,  # 5 lives left

    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,  # 6 lives left (empty gallows, game start)
]
lives =6
 
display =['-'] * len(chosen_word)
print(display)
while not game_over:
    ask = input("guess a letter!\n")
    guess = ask.lower()
    chosen_list = list(chosen_word)
    if guess in guesses:
        print("You've already guessed this letter")
        continue
    else:
        guesses.append(guess)


  

# 3. Replace blanks with correct guesses
    for position in range(len(chosen_word)):
        letter = chosen_word[position]
        if letter == guess:
          display[position] = guess
            
    if guess not in chosen_list:
        lives -=1
        print(f"you guessed {guess}, that's not in the word. you {lives} life left")
        print(stages[lives])
        if lives ==0:
            game_over = True
            print("you lose")
            print(f"the word is {chosen_word}")
              

# 4. Show updated display
    print(display)      
    if '-' not in display:
        game_over = True
        print("you win")
