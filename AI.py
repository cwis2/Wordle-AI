import random
import utils

def initialFilter(wordlist, correct, almost_correct, guesses):
    """Fliters the wordlist
        wordlist: list of words
        correct: dict {letter,index}
        almost_correct: list of letters in word
        guesses: all guessed words"""

    new_list = []                 # Stores new wordlist
    for word in wordlist:         # Loops over every word
        # Stores bool (Are the correct letters in the word in the correct order?)
        flag = True

        for i in range(5):
            if i in correct and word[i] != correct[i]:
                # If the dict is has key "i" but the word doesn't have the correct letter at correct[i]
                flag = False
                break

        if not flag:  # If the previous check failed move on
            continue

        if all(letter in word for letter in almost_correct) and word not in guesses:
            # If all letters that are in almost_correct are in the word and not guessed before
            new_list.append(word)

    return new_list


def secondaryFilter(wordlist, correct_once, used_letters):
    """Filters the wordlist again
        wordlist: list of words
        correct_once: list of letters that only appear in the word once
        used_letters: list of letters that don't appear in the word"""
    
    new_list = []          # Stores new wordlist
    for word in wordlist:  # For each word in the wordlist

        flag = True
        for letter in correct_once:
            if word.count(letter) > 1:
                flag = False

        # If there is a repeat letter that shouldn't be there
        if not flag:
            continue

        # If no letters in used_letters are in the word
        if not any(letter in word for letter in used_letters):
            list.append(word)

    return new_list


def makeguess(wordlist, guesses, feedback):
    """Plays Wordle pretty well (At least better than me ;-;)"""
    if len(guesses) == 0:    # First Guess
        return "SPARE"

    elif len(guesses) == 1:  # Second Guess
        return "CLOUD"

    elif len(guesses) == 2:  # Third Guess
        return "THINK"

    else:  # Fourth Guess onward
        used_letters = []    # Stores all used letters that aren't in the word
        almost_correct = []  # Stores all yellow letters
        correct = {}         # Stores all green letters
        # Stores letters that only appear once but have been guessed twice (looks has two 'O's)
        correct_once = []

        for i in range(len(feedback)):     # Loops over the list of lists
            for j in range(5):
                if feedback[i][j] == 1:    # If yellow
                    almost_correct.append(guesses[i][j])

                elif feedback[i][j] == 2:  # If green
                    correct[j] = guesses[i][j]

                else:  # If not in word
                    # If not yellow (to avoid problems down the line)
                    if guesses[i][j] not in almost_correct:
                        used_letters.append(guesses[i][j])
                    else:
                        correct_once.append(guesses[i][j])

        if len(correct.keys()) == 5:  # If there are 5 correct letters in the Dictionary
            s = ""                    # Stores the word
            for i in range(5):
                s += correct[i]       # Add every letter in the correct order
            return s

        # Removes all words that don't contain all correct and almost correct letters and have been previously guessed
        wordlist = initialFilter(wordlist, correct, almost_correct, guesses)

        # Removes all words that contain wrong letters (may remove all words)
        new_wordlist = secondaryFilter(wordlist, correct_once, used_letters)

        # If new_wordlist isn't empty
        if not len(new_wordlist) == 0:
            return random.choice(new_wordlist)
        else:  # If it is empty we choose from the initial filter
            return random.choice(wordlist)


if __name__ == "__main__":
    wordlist = utils.readwords("allwords5.txt")
    print(f"AI: 'My next choice would be {makeguess(wordlist)}'")
