# Wimbledon.py
# This program requires the graphics.py file from "Python Programming: an
# Introduction to Computer Science" by John Zelle. It also requires classes from
# Wimbledon_classes.py.


from random import random                           # Required to simulate randomness in points
from Wimbledon_classes import Board, WimbledonInput

def main():
    """This program allows the user to simulate a game of tennis on a Wimbledon style
    scoreboard. The user may select the player names and the probability of each
    player winning a point on their service. The user can simulate as many games as
    like and can quit any time by pressing 'Quit'. They may also stop a match at any
    point by pressing 'Stop Sim'."""
    main_board = Board()
    main_board.button_outside_match()     
    while True:
        choice = main_board.interact()          # get button click
        if choice == "Quit":
            break
        elif choice == "Sim":                   # if user clicks sim then sim a game
            InputBox = WimbledonInput("Andy Murray", "Rafael Nadal", 0.73, 0.68)    # some default values
            input_choice = InputBox.interact()  # get button click
            InputBox.close()
            if input_choice == "Return":
                pass
            else:
                # initialize board for match
                PlayerA, PlayerB, probA, probB = InputBox.getValues()
                main_board.set_players(PlayerA, PlayerB)
                serving = initial_server()
                main_board.set_server(serving)
                setsA, setsB, gamesA, gamesB, pointsA, pointsB = 0, 0, 0, 0, 0, 0
                main_board.clear()
                main_board.update(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                
                main_board.button_in_match()
                while True:
                    button_choice = main_board.interact()
                    if button_choice == "Play":
                        setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving = sim_one_point(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving)
                    elif button_choice == "Stop":
                        main_board.button_outside_match()
                        break
                    else:
                        button_choice = main_board.interact()
                    if match_done(setsA, setsB):            # stops loop when match is done
                        main_board.button_outside_match()
                        break

    main_board.close()    
                        
                        


def sim_one_point(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving):
    """Accepts a board, and current score along with current server as parameters.
    Returns score after point along with who is to serve next point. Also updates
    board as necessary."""
    # This function is a little horrible but working. Need to modularize.
    # Outer if loop considers case when players are in a regular game. Else
    # considers case in tiebreak.
    point_winner = play_point(probA, probB, serving) 
    if not in_tiebreak(gamesA, gamesB):
        pointsA, pointsB = update_game_score(pointsA, pointsB, point_winner)
        if not game_done(pointsA, pointsB):
            main_board.update(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
        else:
            gamesA, gamesB = update_set_score(gamesA, gamesB, pointsA, pointsB)
            pointsA, pointsB = 0, 0
            serving = change_server(serving)
            main_board.set_server(serving)
            if not set_done(gamesA, gamesB):
                main_board.update(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
            else:
                setsA, setsB = update_match_score(setsA, setsB, gamesA, gamesB)
                if not match_done(setsA, setsB):
                    set_number = setsA + setsB
                    # "A" + str(set_number) makes first parameter in correct form for
                    # previous_set method
                    main_board.previous_set("A" + str(set_number), gamesA)
                    main_board.previous_set("B" + str(set_number), gamesB)
                    gamesA, gamesB = 0, 0
                    main_board.update(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                else:
                    set_number = setsA + setsB
                    if set_number == 5:       # leaves final set score in on scoreboard if match goes to 5 sets
                        pointsA, pointsB = "", ""
                        main_board.update(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                    else:
                        main_board.previous_set("A" + str(set_number), gamesA)
                        main_board.previous_set("B" + str(set_number), gamesB)
                        gamesA, gamesB, pointsA, pointsB = "", "", "", ""
                        main_board.update(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
    else:
        pointsA, pointsB = update_tiebreak_score(pointsA, pointsB, point_winner)
        if not tiebreak_done(pointsA, pointsB):
            main_board.update(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
            serving = change_server_tiebreak(pointsA, pointsB, serving)
            main_board.set_server(serving)
        else:
            gamesA, gamesB = update_set_score(gamesA, gamesB, pointsA, pointsB)
            setsA, setsB = update_match_score(setsA, setsB, gamesA, gamesB)
            if not match_done(setsA, setsB):
                set_number = setsA + setsB
                main_board.previous_set("A" + str(set_number), gamesA)
                main_board.previous_set("B" + str(set_number), gamesB)
                main_board.previous_set_tiebreak("A" + str(set_number), pointsA)
                main_board.previous_set_tiebreak("B" + str(set_number), pointsB)
                serving = server_end_tiebreak(pointsA, pointsB, serving)
                main_board.set_server(serving)
                pointsA, pointsB, gamesA, gamesB = 0, 0, 0, 0
                main_board.update(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
            else:
                set_number = setsA + setsB
                if set_number == 5:
                    main_board.update(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                else:
                    main_board.previous_set("A" + str(set_number), gamesA)
                    main_board.previous_set("B" + str(set_number), gamesB)
                    main_board.previous_set_tiebreak("A" + str(set_number), pointsA)
                    main_board.previous_set_tiebreak("B" + str(set_number), pointsB)
                    pointsA, pointsB, gamesA, gamesB = "", "", "", ""
                    main_board.update(setsA, setsB, gamesA, gamesB, pointsA, pointsB)

    return setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving
    
def play_point(probA, probB, serving):
    "returns point winner"
    if serving == "A":
        if random() < probA:
            return "A"
        else:
            return "B"
    else:
        if random() < probB:
            return "B"
        else:
            return "A"


def in_tiebreak(gamesA, gamesB):
    "returns true if in tiebreak"
    if gamesA == 6 and gamesB == 6:
        return True
    else:
        return False


def update_game_score(pointsA, pointsB, point_winner):
    "returns game score after point"
    if point_winner == "A":
        if pointsA <= 3 and pointsB <= 3:
            pointsA += 1
        elif pointsA == 4:
            pointsA += 1
        elif pointsB == 4:
            pointsB -= 1
    else:
        if pointsA <= 3 and pointsB <= 3:
            pointsB += 1
        elif pointsB == 4:
            pointsB += 1
        elif pointsA == 4:
            pointsA -= 1

    return pointsA, pointsB


def game_done(scoreA, scoreB):
    "return true if game is done"
    return (scoreA == 4 and scoreB <= 2) or (scoreB == 4 and scoreA <=2) or scoreA ==5 or scoreB == 5


def update_set_score(gamesA, gamesB, pointsA, pointsB):
    "returns set score after game done"
    if pointsA > pointsB:
        gamesA += 1
    else:
        gamesB += 1
    return gamesA, gamesB


def change_server(a):
    "changes server"
    if a == "A":
        return "B"
    else:
        return "A"


def set_done(gamesA, gamesB):
    "returns true if set done"
    return (gamesA == 6 and gamesB <=4) or (gamesB == 6 and gamesA <= 4) or (gamesA == 7 and gamesB == 5) or (gamesB == 7 and gamesA == 5)


def update_match_score(setsA, setsB, gamesA, gamesB):
    "returns match score after game done"
    if gamesA > gamesB:
        setsA += 1
    else:
        setsB += 1
    return setsA, setsB


def match_done(setsA, setsB):
    "returns true if match done"
    return setsA == 3 or setsB == 3


def update_tiebreak_score(pointsA, pointsB, point_winner):
    "update tiebreak score after point"
    if point_winner == "A":
        pointsA += 1
    else:
        pointsB += 1
    return pointsA, pointsB


def tiebreak_done(pointsA, pointsB):
    "Returns true if tiebreak done"
    return (pointsA == 7 and pointsB <= 5) or (pointsB == 7 and pointsA <= 5) or (pointsA >=6 and pointsB >= 6 and abs(pointsA - pointsB) == 2)


def change_server_tiebreak(pointsA, pointsB, serving):
    "changes server after an odd number of points has been played in tiebreak"
    points = pointsA + pointsB
    if points % 2 == 1:
        serving = change_server(serving)
    return serving


def server_end_tiebreak(pointsA, pointsB, serving):
    "changes server if necessary for beginning of next set (player who received first)."
    points_total = pointsA + pointsB
    if points_total % 4 == 0 or points_total % 4 == 1:
        serving = change_server(serving)
    return serving


def initial_server():
    "simulates coinflip to decide who serves first"
    if random()<0.5:
        return "A"
    else:
        return "B"
    
if __name__ == "__main__":
    main()
