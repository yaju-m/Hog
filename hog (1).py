"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** REPLACE THIS LINE ***"
    total = 0
    onetotal = 0
    while num_rolls>0:
        x = dice() 
        if x == 1:
            onetotal +=1
        else:
            total += x
        num_rolls -=1
    if onetotal>0:
        return onetotal
    return total
#roll_dice(2, make_test_dice(4,6,1))

    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    "*** REPLACE THIS LINE ***"
    ones_digit= opponent_score%10
    tens_digit= opponent_score//10
    if ones_digit>tens_digit:
        points= 1+ones_digit
    else:
        points= 1+tens_digit
    return points 

    # END PROBLEM 2

def is_prime(points):
    if points==1:
        return False 
    x= 2
    while x < points: 
        if points%x==0:
            return False 
        x +=1 
    return True 

def next_prime(points):
    x = points +1
    a= is_prime(x)   
    while a == False:  
        x = x+1 
        a = is_prime(x)
    points = x 
    return points         

# Write your prime functions here!


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime and When Pigs Fly rules.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    "*** REPLACE THIS LINE ***"
    if num_rolls==0:
        points = free_bacon(opponent_score)
        if is_prime(points): 
            points= next_prime(points)
        return points 
    elif num_rolls>0:
        points = roll_dice(num_rolls, dice)
        if is_prime(points): 
            points= next_prime(points)
        return min(25-num_rolls, points)

    # END PROBLEM 2


def reroll(dice):
    """Return dice that return even outcomes and re-roll odd outcomes of DICE."""
    def rerolled():
        points=dice()
        if points%2==0:
            return points 
        else:
            points= dice()   
        # BEGIN PROBLEM 3
        "*** REPLACE THIS LINE ***"
        return points  # Replace this statement
        # END PROBLEM 3
    return rerolled


def select_dice(score, opponent_score, dice_swapped):
    """Return the dice used for a turn, which may be re-rolled (Hog Wild) and/or
    swapped for four-sided dice (Pork Chop).

    DICE_SWAPPED is True if and only if four-sided dice are being used.
    """
    # BEGIN PROBLEM 4
    "*** REPLACE THIS LINE ***"
    # Replace this statement
    dice = six_sided
    if dice_swapped == True:
        dice = four_sided 
    # END PROBLEM 4
    if (score + opponent_score) % 7 == 0:
        dice= reroll(dice)

    return dice


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False  # Whether 4-sided dice have been swapped for 6-sided  

    # BEGIN PROBLEM 5

    while (score0<goal and score1<goal):
        if player ==0: 
            num_rolls= strategy0(score0, score1)  
            dice_used = select_dice(score0, score1, dice_swapped)      
            if num_rolls == -1:
                dice_swapped = not dice_swapped
                score0+= 1
            else:    
                score0 += take_turn(num_rolls, score1, dice_used)
        else: 
            num_rolls= strategy1(score1, score0)
            dice_used= select_dice(score1, score0, dice_swapped)
            if num_rolls == -1:
                dice_swapped = not dice_swapped 
                score1+= 1
            else: 
                score1 += take_turn(num_rolls, score0, dice_used)
        if score1== 2*score0 or score0== 2*score1:
            score0, score1 = score1, score0
        player = other(player)
    return score0, score1    




#do this again for the other player, rememer to swap your args 
#do swine swap at end of while loop for both players
#use a conditional to keep track of who is playing player one or zero and execute what you need for zero 
#otherwise if player 1 is playing, just do this xxxx

    "*** REPLACE THIS LINE ***"
    # END PROBLEM 5
 #   return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert -1 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    "*** REPLACE THIS LINE ***"
    score = 0
    opponent_score = 0

    while (score < goal and opponent_score < goal):
        while opponent_score < goal: 
            what_num_rolls = strategy(score, opponent_score)
            check_strategy_roll(score, opponent_score, what_num_rolls)
            opponent_score += 1
        score += 1
        opponent_score = -1
    return None 


    # END PROBLEM 6
#for all possible combos of your score and opponents check to see that check strat roll does the right thing 

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    "*** REPLACE THIS LINE ***"
    def repeat_fn(*args):
        total= 0
        a = 1
        while a<=num_samples: 
            total += fn(*args)
            a += 1
        total = total/num_samples
        return total 
    return repeat_fn 
        # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    num_rolls = 10
    high_score= 0 
    low_dice = 10
    while num_rolls>0:
        average_value = make_averaged(roll_dice, num_samples)(num_rolls, dice)
        if average_value>high_score: 
            high_score= average_value
            low_dice=num_rolls
        num_rolls -= 1 
    return low_dice 

    # go from 1 dice to 10 dice (or backwards bc you want the lower number) and for each one check make average 
    #save this avg value and the number of dice used 



    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        rerolled_max = max_scoring_num_rolls(reroll(six_sided))
        print('Max scoring num rolls for re-rolled dice:', rerolled_max)

    if True:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    if take_turn(0, opponent_score, dice=six_sided) >= margin: 
        return 0
    else:
        return num_rolls

    # Replace this statement
    # END PROBLEM 9
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    if opponent_score== 2*score: 
        return 0
    add_to_score = take_turn(0, opponent_score, dice=six_sided)
    if add_to_score >= margin and score+add_to_score != 2*opponent_score:
        return 0
    return num_rolls    
  # Replace this statement
    # END PROBLEM 10
check_strategy(swap_strategy)
#if causes a benficial swap roll 0 
#if rolling 0 gives atleast margin points and the upcoming swap doesnt hurt you , return 0
#otherwise, roll num_rolls 

def zero_strategy(score, opponent_score, margin=8, num_rolls=4):
    """returns 0 if:
            returning it gives a beneficial swap
            or it returns at least MARGIN points after Hogtimus Prime, and doesn't cause an upcoming negative swap or give them reroll """
    if opponent_score== 2*score: 
        return 0
    add_to_score = take_turn(0, opponent_score, dice=four_sided)
    if (add_to_score >= margin) and (score+add_to_score != 2*opponent_score):
        if((score+opponent_score+add_to_score) % 7 != 0):
            return 0
    return num_rolls




def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 11
    "*** REPLACE THIS LINE ***"
    if score == 0:
        return -1
    ans = swap_strategy(score, opponent_score, margin=8, num_rolls= 4)

    #if close to end:
    if ans != 0 and 100-score<=6:
        dif = 100-score
        if dif <=3:
            best_num_roll = 10
        else:
            best_num_roll = 4
        ans = zero_strategy(score, opponent_score, margin=dif, num_rolls= best_num_roll)
    

    return ans # Replace this statement
    # END PROBLEM 11
    # END PROBLEM 11
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()