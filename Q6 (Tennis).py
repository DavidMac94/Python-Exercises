# This program fully sims a game of tennis. Required inputs are probabilities of player winning a point on serve (in range (0, 1)) and
# the number of sets (odd) in the match.
# Serving is decided by a cointoss and correctly alternated throughout the match (i.e. after every game including tiebreak).

from random import random           # we need random to randomise points in the match.

def main():
    probA, probB, sets = get_inputs()
    setsA, setsB, score = simNsets(probA, probB, sets)
    output_result(setsA, setsB, score)


def get_inputs():
    print("This program simulates a game of tennis. The program requires the probability of each player winning a point on their serve and the number of sets.")
    A = float(input("Enter the probability of player A winning a point on their serve: "))
    B = float(input("Enter the probability of player B winning a point on their serve: "))
    n = int(input("Enter the number of sets: "))
    return A, B, n


# simNsets accepts the probability of each player winning a point on serve and the number of sets in the match.
# The function has three outputs: the number of sets won by each player and a list containing a sequence of strings containing the set scores. 
def simNsets(probA, probB, sets):
    setsA, setsB = 0, 0
    score = []
    # coinflip to decide who serves first
    if random() < 0.5:
        serving = "A"
    else:
        serving = "B"

    while not matchdone(setsA, setsB, sets):
        gamesA, gamesB, tieA, tieB = simset(probA, probB, serving)
        if gamesA > gamesB:
            setsA += 1
            change_server(gamesA, gamesB, serving)                  # changes server at the end of the set if required.
        else:
            setsB += 1
            change_server(gamesA, gamesB, serving)
        score.append(score_string(gamesA, gamesB, tieA, tieB))      # score_string create a string containing a set score.
    return setsA, setsB, score


# match is done when a player has won over half the sets to be played. matchdone returns True when the match is done and false otherwise.
def matchdone(A, B, n):
    return A > n // 2 or B > n // 2


# change_server chnages the server if the number of games played in the previous set is odd.
def change_server(gamesA, gamesB, serving):
    if (gamesA + gamesB) % 2 == 0:
        pass
    else:
        if serving == "A":
            serving = "B"
        else:
            serving ="A"


def score_string(gamesA, gamesB, tieA, tieB):
    string = str(gamesA) + "-" + str(gamesB)
    if tieA > 0 or tieB > 0:
        string += " (" + str(tieA) + "-" + str(tieB) +")"
    return string


# simset simulates one set and returns 4 values: games won by A, games won by B, tiebreak points won by A and tiebreak points won by B.
# If no tiebreak was required then the tiebreak scores are 0. 
def simset(probA, probB, serving):
    gamesA, gamesB = 0, 0
    while not setdone(gamesA, gamesB):                      # keeps playing games until set is won or scores reach 6-6. 
        if serving == "A":
            serverwin = simgame(probA)
            if serverwin:
                gamesA += 1
            else:
                gamesB += 1
            serving = "B"                                   # swaps server after every game.
        else:
            serverwin = simgame(probB)
            if serverwin:
                gamesB += 1
            else:
                gamesA += 1
            serving = "A"
    if gamesA == 6 and gamesB == 6:                         # begins tiebreak if score reaches 6-6
        tieA, tieB = simtiebreak(probA, probB, serving)
        if tieA > tieB:
            gamesA += 1
        else:
            gamesB += 1
        return gamesA, gamesB, tieA, tieB                   # returns values from set if tiebreak was required                  
    else:
        return gamesA, gamesB, 0, 0                         # returns scores from set if no tiebreak was required


# setdone returns true when scores are either 6-4, 6-3, 6-2, 6-1, 6-0, 7-5 (or reverse) or 6-6.
def setdone(gamesA, gamesB):
    return (gamesA == 6 and gamesB <=4) or (gamesB == 6 and gamesA <= 4) or (gamesA == 7 and gamesB == 5) or (gamesB == 7 and gamesA == 5) or (gamesA == 6 and gamesB == 6)
    

# simgame simulates one game of tennis and requires the servers probability of winning a point as input. Returns true if server wins game, false otherwise.
# server and returner keep track of scores. In tennis terms: 0=0, 1=15, 2=30, 3=40, 4=Ad. Scoring is standard until one player reaches 4.
# The two elifs then return the player to 3 (Deuce) if they lose the point and to 5 (win the game) if they win.
def simgame(prob):
    server, returner = 0, 0
    while not gamedone(server, returner):
        if server <= 3 and returner <= 3:
            if random() < prob:                     # condition is true (server wins point) with probability prob as required
                server += 1
            else:
                returner += 1
        elif server == 4:
            if random() < prob:
                server += 1
            else:
                server -= 1
        elif returner == 4:
            if random() < prob:
                returner -= 1
            else:
                returner += 1
    if server > returner:
        return True
    else:
        return False


# returns true when game is done, false otherwise
def gamedone(scoreA, scoreB):
    return (scoreA == 4 and scoreB <= 2) or (scoreB == 4 and scoreA <=2) or scoreA ==5 or scoreB == 5
    

# simtiebreak simulates a tiebreak and requires as usual the two probabilities of players winning a point on serve and whos serves first in the tiebreak.
# 
def simtiebreak(probA, probB, serving):
    scoreA, scoreB = 0, 0
    while not tiebreakdone(scoreA, scoreB):
        if serving == "A":
            if random() < probA:
                scoreA += 1
            else:
                scoreB += 1
            if (scoreA + scoreB) % 2 == 1:          # swaps service on odd points.
                serving = "B"
        else:
            if random() < probB:
                scoreB += 1
            else:
                scoreA += 1
            if (scoreA + scoreB) % 2 == 1:
                serving = "A"
    return scoreA, scoreB


# tiebreakdone returns true when a player has won the tiebreak. This is when a player has 7 or more points AND is ahead by 2 or more points.
def tiebreakdone(scoreA, scoreB):
    return (scoreA == 7 and scoreB <= 5) or (scoreB == 7 and scoreA <= 5) or (scoreA >=6 and scoreB >= 6 and abs(scoreA - scoreB) == 2)


# outputs result of match
def output_result(setsA, setsB, score):
    if setsA > setsB:
        print("Player A wins", setsA, "to", setsB)
    else:
        print("Player B wins", setsB, "to", setsA)
    print("The score is ", end="")
    for i in score:
        print(i, end=" ")
    Exit = input("\nPress any key to quit")
    

main()
    
    
