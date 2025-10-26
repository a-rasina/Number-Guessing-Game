from random import randint
import time

# Difficulty settings
difficulties = {
    '1': {'attempts': 10, 'name': 'Easy'},
    '2': {'attempts': 5, 'name': 'Medium'},
    '3': {'attempts': 3, 'name': 'Hard'}
}

# Global high scores tracker per difficulty
high_scores = {
    '1': None,  # Easy
    '2': None,  # Medium
    '3': None   # Hard
}

def get_difficulty():
    """Prompt user for difficulty level and return max attempts, name, and choice"""
    print("Please select the difficulty level:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")
    
    choice = input("Enter your choice: ")
    max_attempts = difficulties.get(choice, difficulties['2'])['attempts']
    difficulty_name = difficulties.get(choice, difficulties['2'])['name']
    
    return max_attempts, difficulty_name, choice

def play_round(max_attempts, difficulty_name, secret, difficulty_key):
    """Play a single round of the guessing game"""
    print(f"Great! You have selected the {difficulty_name} difficulty level.")
    print("Let's start the game!")
    
    count = 0
    start_time = time.time()  # Start timer for the entire game
    
    while count < max_attempts:
        guess = int(input('Enter your guess: '))
        count += 1
        
        if guess == secret:
            elapsed_time = time.time() - start_time
            print(f"Congratulations! You guessed the correct number in {count} attempts and it took you {elapsed_time:.2f} seconds!")
            # Update high score if the user won
            update_high_score(count, difficulty_key)
            return True, count  # Game won, return True and attempt count
        elif guess < secret:
            print(f"❌ Incorrect! The number is greater than {guess}")
            print()  # Empty line for better readability
            hint(secret, count)
        else:  # guess > secret
            print(f"❌ Incorrect! The number is less than {guess}")
            print()  # Empty line for better readability
            hint(secret, count)
    
    # Game over - out of chances
    print(f"Game Over! You've run out of chances. The correct number was {secret}.")
    return False, count  # Game lost, return False and attempt count

def reset_game():
    """Reset the game with a new secret number and difficulty"""
    secret = randint(1, 100)
    max_attempts, difficulty_name, choice = get_difficulty()
    return secret, max_attempts, difficulty_name, choice

def hint(secret, attempt_count):
    """A hint system that provides clues to the user if they are stuck"""
    hints_given = []
    
    # Hint 1: Even/Odd
    if secret % 2 == 0:
        hints_given.append("The number is even")
    else:
        hints_given.append("The number is odd")
    
    # Hint 2: Divisibility (after first few attempts)
    if attempt_count >= 2:
        if secret % 5 == 0:
            hints_given.append("The number is divisible by 5")
        if secret % 10 == 0:
            hints_given.append("The number is divisible by 10")
       
    
    # Hint 3: Range (after more attempts)
    if attempt_count >= 3:
        if secret <= 25:
            hints_given.append("The number is in the first quarter (1-25)")
        elif secret <= 50:
            hints_given.append("The number is in the second quarter (26-50)")
        elif secret <= 75:
            hints_given.append("The number is in the third quarter (51-75)")
        else:
            hints_given.append("The number is in the fourth quarter (76-100)")

    # Display hints in a formatted box
    if hints_given:
        print("💡 Hints:")
        for hint in hints_given:
            print(f"   • {hint}")
        print()  # Extra empty line after all hints

def get_difficulty_choice():
    """Helper function to get difficulty choice"""
    print("Please select the difficulty level:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")
    
    choice = input("Enter your choice: ")
    return choice

def update_high_score(attempts_count, difficulty_key):
    """Update high score if the current attempt count is better (lower)"""
    global high_scores
    
    if high_scores[difficulty_key] is None or attempts_count < high_scores[difficulty_key]:
        high_scores[difficulty_key] = attempts_count
        difficulty_name = difficulties[difficulty_key]['name']
        print(f"NEW HIGH SCORE for {difficulty_name} difficulty: {attempts_count} attempts!")
    else:
        difficulty_name = difficulties[difficulty_key]['name']
        print(f"Current best score for {difficulty_name}: {high_scores[difficulty_key]} attempts")

def display_all_high_scores():
    """Display all high scores for all difficulties"""
    print("\n CURRENT HIGH SCORES:")
    for key, name in [('1', 'Easy'), ('2', 'Medium'), ('3', 'Hard')]:
        score = high_scores[key]
        if score is not None:
            print(f"  {name}: {score} attempts")
        else:
            print(f"  {name}: No score yet")
    print()

# Main game loop
print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.\n")

secret = randint(1, 100)
max_attempts, difficulty_name, difficulty_key = get_difficulty()

while True:
    won, attempts_count = play_round(max_attempts, difficulty_name, secret, difficulty_key)
    
    # Display all high scores after each round
    display_all_high_scores()
    
    decision = input("Do you want another round? yes/no: ").lower()
    if decision == 'yes':
        secret, max_attempts, difficulty_name, difficulty_key = reset_game()
    else:
        print("Okay, thank you for the game!")
        break