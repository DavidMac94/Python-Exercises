# Wimbledon.py
# This program requires the graphics.py file from "Python Programming: an
# Introduction to Computer Science" by John Zelle.

from random import random                           # Required to simulate randomness in points
from graphics import *

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
                main_board.update_score(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                
                main_board.button_in_match()
                while True:
                    button_choice = main_board.interact()
                    # sims point/game/set or match depending on button clicked. Loops until user quits.
                    if button_choice == "Point":
                        setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving = sim_one_point(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving)
                        if not match_done(setsA, setsB):
                            main_board.update_score(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                        else:
                            main_board.update_score_end(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                        main_board.set_server(serving)
                    elif button_choice == "Game":
                        setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving = sim_one_game(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving)
                        if not match_done(setsA, setsB):
                            main_board.update_score(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                        else:
                            main_board.update_score_end(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                        main_board.set_server(serving)
                    elif button_choice == "Set":
                        setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving = sim_one_set(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving)
                        if not match_done(setsA, setsB):
                            main_board.update_score(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                        else:
                            main_board.update_score_end(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                        main_board.set_server(serving)
                    elif button_choice == "Match":
                        setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving = sim_one_match(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving)
                        if not match_done(setsA, setsB):
                            main_board.update_score(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                        else:
                            main_board.update_score_end(setsA, setsB, gamesA, gamesB, pointsA, pointsB)
                        main_board.set_server(serving)
                    elif button_choice == "Stop":
                        main_board.button_outside_match()
                        break
                    if match_done(setsA, setsB):
                        # stops loop when match is done
                        main_board.button_outside_match()
                        break

    main_board.close()    
                        
                        


def sim_one_point(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving):
    """Accepts a board, and current score along with current server as parameters.
    Returns score after point along with who is to serve next point. Records previous
    set score if required."""
    # This function is a little horrible but working. Need to modularize.
    # Outer if loop considers case when players are in a regular game. Else
    # considers case in tiebreak.
    point_winner = play_point(probA, probB, serving) 
    if not in_tiebreak(gamesA, gamesB):
        pointsA, pointsB = update_game_score(pointsA, pointsB, point_winner)
        if game_done(pointsA, pointsB):
            gamesA, gamesB = update_set_score(gamesA, gamesB, pointsA, pointsB)
            pointsA, pointsB = 0, 0
            serving = change_server(serving)
            if set_done(gamesA, gamesB):
                setsA, setsB = update_match_score(setsA, setsB, gamesA, gamesB)
                if not match_done(setsA, setsB):
                    set_number = setsA + setsB
                    # "A" + str(set_number) makes first parameter in correct form for
                    # previous_set method
                    main_board.previous_set("A" + str(set_number), gamesA)
                    main_board.previous_set("B" + str(set_number), gamesB)
                    gamesA, gamesB = 0, 0
    else:
        pointsA, pointsB = update_tiebreak_score(pointsA, pointsB, point_winner)
        if not tiebreak_done(pointsA, pointsB):
            serving = change_server_tiebreak(pointsA, pointsB, serving)
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
                pointsA, pointsB, gamesA, gamesB = 0, 0, 0, 0

    return setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving


def sim_one_game(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving):
    "Sims one game of tennis and returns state of match after game."
    while True:
        setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving = sim_one_point(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving)
        if (pointsA == 0 and pointsB == 0) or match_done(setsA, setsB): break
    return setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving

def sim_one_set(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving):
    "Sims one set of tennis and returns state of match after game."
    while True:
        setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving = sim_one_game(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving)
        if (gamesA == 0 and gamesB == 0) or match_done(setsA, setsB): break
    return setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving


def sim_one_match(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving):
    "Sims one match of tennis and returns state of match after game."
    while not match_done(setsA, setsB):
        setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving = sim_one_set(main_board, probA, probB, setsA, setsB, gamesA, gamesB, pointsA, pointsB, serving)
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


class WimbledonInput:

    """This class creates an input box and allows the user to enter data
    into the following fields: Player 1, Player 2, ProbA, Prob B"""

    def __init__(self, PlayerA, PlayerB, probA, probB):
        self.win = win = GraphWin("Choose Players", 300, 300)
        win.setCoords(0, 9, 4, 0)

        Text(Point(1, 1), "Player 1:").draw(win)
        self.playerA = Entry(Point(2.7, 1), 18).draw(win)
        self.playerA.setText(PlayerA)

        Text(Point(1, 2), "Player 2:").draw(win)
        self.playerB = Entry(Point(2.7,2), 18).draw(win)
        self.playerB.setText(PlayerB)

        Text(Point(1,3), "Prob A*").draw(win)
        self.probA = Entry(Point(2.7,3), 5).draw(win)
        self.probA.setText(str(probA))

        Text(Point(1,4), "Prob B*").draw(win)
        self.probB = Entry(Point(2.7,4), 5).draw(win)
        self.probB.setText(str(probB))

        self.warning1 = Text(Point(2, 8), "*Probability player wins point on serve.").draw(win)
        self.warning2 = Text(Point(2, 8.6), "Enter number in range (0, 1)").draw(win)

        self.sim = Button(win, Point(1, 6), 1.25, .5, "Sim")
        self.sim.activate()

        self.exit = Button(win, Point(3,6), 1.25, .5, "Exit")
        self.exit.activate()

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.sim.clicked(pt):
                try:
                    a = float(self.probA.getText())
                    b = float(self.probB.getText())
                except:
                    self.warning1.setFill("red")
                    self.warning2.setFill("red")
                    continue
                if 0 < a < 1 and 0 < b < 1:
                    return "Sim Match"
                else:
                    self.warning1.setFill("red")
                    self.warning2.setFill("red")
            if self.exit.clicked(pt):
                return "Return"

    def getValues(self):
        A = self.playerA.getText()
        B = self.playerB.getText()
        a = float(self.probA.getText())
        b = float(self.probB.getText())
        return A, B, a, b

    def close(self):
        self.win.close()


class Board:
    """This class creates a wimbledon style scoreboard."""
    
    def __init__(self):
        "Creates scoreboard and initializes some required parameters."
        self.win = win = GraphWin("Wimbledon Final", 600, 300, autoflush = "False")
        win.setCoords(0, 100, 100, 0)
        win.setBackground(color_rgb(0 , 80 , 0))
        
        Final = Text(Point(50, 5), "Final")
        Final.setFill("white")
        Final.draw(win)
        
        Time = Entry(Point(15, 15), 5)
        Time.setText("19:15")
        Time.setFill(color_rgb (40 , 40 , 40 ))
        Time.setSize(20)
        Time.setTextColor("gold")
        Time.draw(win)
        
        Rolex = Text(Point(50, 15), "Rolex")
        Rolex.setFill("gold")
        Rolex.setSize(18)
        Rolex.draw(win)
        
        Match_time = Entry(Point(85, 15), 5)
        Match_time.setText("3.35")
        Match_time.setFill(color_rgb(40 , 40 , 40))
        Match_time.setSize(20)
        Match_time.setTextColor("gold")
        Match_time.draw(win)
        
        Strip = Line(Point(0, 23), Point(100, 23))
        Strip.setWidth(4)
        Strip.setFill("purple")
        Strip.draw(win)
        
        Previous_sets = Text(Point(13, 30), "PREVIOUS SETS")
        Previous_sets.setFill("white")
        Previous_sets.setSize(10)
        Previous_sets.draw(win)

        Sets = Text(Point(78, 30),"SETS")
        Sets.setFill("white")
        Sets.setSize(10)
        Sets.draw(win)

        Games = Text(Point(86.5, 30), "GAMES")
        Games.setFill("white")
        Games.setSize(10)
        Games.draw(win)

        Points = Text(Point(96, 30), "POINTS")
        Points.setFill("white")
        Points.setSize(10)
        Points.draw(win)

        self.pSetsA1_box = Rectangle(Point(2, 48), Point(7, 36))
        self.pSetsA1_box.setFill(color_rgb(40 , 40 , 40))
        self.pSetsA1_box.draw(win)

        self.pSetsA2_box = self.pSetsA1_box.clone()
        self.pSetsA2_box.move(6, 0)
        self.pSetsA2_box.draw(win)

        self.pSetsA3_box = self.pSetsA1_box.clone()
        self.pSetsA3_box.move(12, 0)
        self.pSetsA3_box.draw(win)

        self.pSetsA4_box = self.pSetsA1_box.clone()
        self.pSetsA4_box.move(18, 0)
        self.pSetsA4_box.draw(win)

        self.pSetsB1_box = self.pSetsA1_box.clone()
        self.pSetsB1_box.move(0, 20)
        self.pSetsB1_box.draw(win)

        self.pSetsB2_box = self.pSetsA1_box.clone()
        self.pSetsB2_box.move(6, 20)
        self.pSetsB2_box.draw(win)

        self.pSetsB3_box = self.pSetsA1_box.clone()
        self.pSetsB3_box.move(12, 20)
        self.pSetsB3_box.draw(win)

        self.pSetsB4_box = self.pSetsA1_box.clone()
        self.pSetsB4_box.move(18, 20)
        self.pSetsB4_box.draw(win)

        Player_boxA = Rectangle(Point(27, 48), Point(73, 36))
        Player_boxA.setFill(color_rgb(40 , 40 , 40))
        Player_boxA.draw(win)

        Player_boxB = Player_boxA.clone()
        Player_boxB.move(0, 20)
        Player_boxB.draw(win)

        # Create text box with players name
        self.PlayerA = Text(Point(50, 42), "Andy Murray")
        self.PlayerA.setFill("gold")
        self.PlayerA.setSize(22)
        self.PlayerA.draw(win)

        self.PlayerB = Text(Point(50, 62), "Rafael Nadal")
        self.PlayerB.setFill("gold")
        self.PlayerB.setSize(22)
        self.PlayerB.draw(win)

        Versus = Text(Point(50, 52), "v")
        Versus.setFill("gold")
        Versus.setSize(17)
        Versus.draw(win)

        SetsA_box = Rectangle(Point(75, 48), Point(81, 36))
        SetsA_box.setFill(color_rgb(40 , 40 , 40))
        SetsA_box.draw(win)

        GamesA_box = Rectangle(Point(83, 48), Point(90, 36))
        GamesA_box.setFill(color_rgb(40 , 40 , 40))
        GamesA_box.draw(win)

        PointsA_box = Rectangle(Point(92, 48), Point(99, 36))
        PointsA_box.setFill(color_rgb(40 , 40 , 40))
        PointsA_box.draw(win)

        SetsB_box = SetsA_box.clone()
        SetsB_box.move(0, 20)
        SetsB_box.draw(win)
        
        GamesB_box = GamesA_box.clone()
        GamesB_box.move(0, 20)
        GamesB_box.draw(win)

        PointsB_box = PointsA_box.clone()
        PointsB_box.move(0, 20)
        PointsB_box.draw(win)

        # Create text boxes for previouse set scores
        self.pSetsA1 = Text(Point(4.5, 42), "")
        self.pSetsA1.setFill("gold")
        self.pSetsA1.setSize(20)
        self.pSetsA1.draw(win)

        self.pSetsA2 = self.pSetsA1.clone()
        self.pSetsA2.move(6, 0)
        self.pSetsA2.draw(win)

        self.pSetsA3 = self.pSetsA1.clone()
        self.pSetsA3.move(12, 0)
        self.pSetsA3.draw(win)

        self.pSetsA4 = self.pSetsA1.clone()
        self.pSetsA4.move(18, 0)
        self.pSetsA4.draw(win)

        self.pSetsB1 = self.pSetsA1.clone()
        self.pSetsB1.move(0, 20)
        self.pSetsB1.draw(win)

        self.pSetsB2 = self.pSetsA1.clone()
        self.pSetsB2.move(6, 20)
        self.pSetsB2.draw(win)

        self.pSetsB3 = self.pSetsA1.clone()
        self.pSetsB3.move(12, 20)
        self.pSetsB3.draw(win)

        self.pSetsB4 = self.pSetsA1.clone()
        self.pSetsB4.move(18, 20)
        self.pSetsB4.draw(win)

        # Create text boxes for previous set tiebreak scores
        self.pSets_tie_A1 = Text(Point(4.5, 51), "")
        self.pSets_tie_A1.setFill("white")
        self.pSets_tie_A1.setSize(10)
        self.pSets_tie_A1.draw(win)

        self.pSets_tie_A2 = self.pSets_tie_A1.clone()
        self.pSets_tie_A2.move(6, 0)
        self.pSets_tie_A2.draw(win)

        self.pSets_tie_A3 = self.pSets_tie_A1.clone()
        self.pSets_tie_A3.move(12, 0)
        self.pSets_tie_A3.draw(win)

        self.pSets_tie_A4 = self.pSets_tie_A1.clone()
        self.pSets_tie_A4.move(18, 0)
        self.pSets_tie_A4.draw(win)

        self.pSets_tie_B1 = self.pSets_tie_A1.clone()
        self.pSets_tie_B1.move(0, 20)
        self.pSets_tie_B1.draw(win)

        self.pSets_tie_B2 = self.pSets_tie_A1.clone()
        self.pSets_tie_B2.move(6, 20)
        self.pSets_tie_B2.draw(win)

        self.pSets_tie_B3 = self.pSets_tie_A1.clone()
        self.pSets_tie_B3.move(12, 20)
        self.pSets_tie_B3.draw(win)

        self.pSets_tie_B4 = self.pSets_tie_A1.clone()
        self.pSets_tie_B4.move(18, 20)
        self.pSets_tie_B4.draw(win)

        # Create text boxes for current score
        self.SetsA = Text(Point(78, 42), "")
        self.SetsA.setFill("gold")
        self.SetsA.setSize(20)
        self.SetsA.draw(win)

        self.GamesA = Text(Point(86.5, 42), "")
        self.GamesA.setFill("gold")
        self.GamesA.setSize(20)
        self.GamesA.draw(win)

        self.PointsA = Text(Point(95.5, 42), "")
        self.PointsA.setFill("gold")
        self.PointsA.setSize(20)
        self.PointsA.draw(win)

        self.SetsB = Text(Point(78, 62), "")
        self.SetsB.setFill("gold")
        self.SetsB.setSize(20)
        self.SetsB.draw(win)

        self.GamesB = Text(Point(86.5, 62), "")
        self.GamesB.setFill("gold")
        self.GamesB.setSize(20)
        self.GamesB.draw(win)

        self.PointsB = Text(Point(95.5, 62), "")
        self.PointsB.setFill("gold")
        self.PointsB.setSize(20)
        self.PointsB.draw(win)

        # Creates dots which can be drawn/undrawn to indicate server
        self.ServingA_Dot = Oval(Point(70, 40), Point(72,44))
        self.ServingA_Dot.setFill("gold")

        self.ServingB_Dot = self.ServingA_Dot.clone()
        self.ServingB_Dot.move(0, 20)

        #Create buttons
        self.sim_match = Button(win, Point(14, 78), 20, 10, "Sim Match")
        self.play_point = Button(win, Point(38, 78), 20, 10, "Play Point")
        self.play_game = Button(win, Point(38, 93), 20, 10, "Play Game")
        self.play_set = Button(win, Point(62, 78), 20, 10, "Play Set")
        self.play_match = Button(win, Point(62, 93), 20, 10, "Play Match")
        self.stop_sim = Button(win, Point(86, 85.5), 20, 10, "Stop Sim")
        self.quit = Button(win, Point(14, 93), 20, 10, "Quit")


    def update_score(self, setsA, setsB, gamesA, gamesB, pointsA, pointsB):
        "Updates board, converting points to tennis equivalent if in a game (i.e. 1=15, 2=30....)"
        tennis_points = ["0", "15", "30", "40", "A"]  
        self.SetsA.setText(setsA)
        self.SetsB.setText(setsB)
        self.GamesA.setText(gamesA)
        self.GamesB.setText(gamesB)
        if gamesA == "" and gamesB == "":
            self.PointsA.setText(pointsA)
            self.PointsB.setText(pointsB)
        elif (gamesA == 6 and gamesB == 6) or (gamesA == 6 and gamesB == 7) or (gamesA == 7 and gamesB == 6) or (pointsA == "" and pointsB == ""):
            self.PointsA.setText(pointsA)
            self.PointsB.setText(pointsB)
        else:
            self.PointsA.setText(tennis_points[pointsA])
            self.PointsB.setText(tennis_points[pointsB])


    def update_score_end(self, setsA, setsB, gamesA, gamesB, pointsA, pointsB):
        "Updates board to display (final) result of match."
        set_number = setsA + setsB
        if (gamesA == 6 and gamesB == 7) or (gamesA == 7 and gamesB == 6):
            if not set_number == 5:
                self.previous_set("A" + str(set_number), gamesA)
                self.previous_set("B" + str(set_number), gamesB)
                self.previous_set_tiebreak("A" + str(set_number), pointsA)
                self.previous_set_tiebreak("B" + str(set_number), pointsB)
                pointsA, pointsB, gamesA, gamesB = "", "", "", ""
        else:
            if set_number == 5:
                pointsA, pointsB = "", ""
            else:
                self.previous_set("A" + str(set_number), gamesA)
                self.previous_set("B" + str(set_number), gamesB)
                gamesA, gamesB, pointsA, pointsB = "", "", "", ""
        self.update_score(setsA, setsB, gamesA, gamesB, pointsA, pointsB)

            
    def set_players(self, a, b):
        "Updates board with player names"
        self.PlayerA.setText(a)
        self.PlayerB.setText(b)
            

    def set_server(self, server):
        "updates service dot according to who is to serve next point"
        if server == "A":
            self.ServingA_Dot.undraw()
            self.ServingB_Dot.undraw()
            self.ServingA_Dot.draw(self.win)
        else:
            self.ServingA_Dot.undraw()
            self.ServingB_Dot.undraw()
            self.ServingB_Dot.draw(self.win)


    def previous_set(self, set_num, score):  # set_num is in form "A2"
        "Records previous set score. set_num comes in form 'Pn' where P is player and n is set number."
        if set_num == "A1":
            self.pSetsA1.setText(score)
        elif set_num == "A2":
            self.pSetsA2.setText(score)
        elif set_num == "A3":
            self.pSetsA3.setText(score)
        elif set_num == "A4":
            self.pSetsA4.setText(score)
        elif set_num == "B1":
            self.pSetsB1.setText(score)
        elif set_num == "B2":
            self.pSetsB2.setText(score)
        elif set_num == "B3":
            self.pSetsB3.setText(score)
        elif set_num == "B4":
            self.pSetsB4.setText(score)
            

    def previous_set_tiebreak(self, set_num, score):  # set_num is in form "A2"
        "Records previous set tiebreak score"
        if set_num == "A1":
            self.pSets_tie_A1.setText(score)
        elif set_num == "A2":
            self.pSets_tie_A2.setText(score)
        elif set_num == "A3":
            self.pSets_tie_A3.setText(score)
        elif set_num == "A4":
            self.pSets_tie_A4.setText(score)
        elif set_num == "B1":
            self.pSets_tie_B1.setText(score)
        elif set_num == "B2":
            self.pSets_tie_B2.setText(score)
        elif set_num == "B3":
            self.pSets_tie_B3.setText(score)
        elif set_num == "B4":
            self.pSets_tie_B4.setText(score)


    def interact(self):
        """Return string indicating which button has been clicked
        (At least one button must be active or infinite loop)"""
        while True:
            pt = self.win.getMouse()
            if self.sim_match.clicked(pt):
                return "Sim"
            elif self.play_point.clicked(pt):
                return "Point"
            elif self.play_game.clicked(pt):
                return "Game"
            elif self.play_set.clicked(pt):
                return "Set"
            elif self.play_match.clicked(pt):
                return "Match"
            elif self.stop_sim.clicked(pt):
                return "Stop"
            elif self.quit.clicked(pt):
                return "Quit"


    def button_outside_match(self):
        "Activates sim_match and quit buttons which are necessary when not in the middle of a match. Deactivates others."
        self.sim_match.activate()
        self.quit.activate()
        self.play_point.deactivate()
        self.play_game.deactivate()
        self.play_set.deactivate()
        self.play_match.deactivate()
        self.stop_sim.deactivate()



    def button_in_match(self):
        "Activates play_point and stop_sim buttons which are necessary during a match. Deactivates others."
        self.sim_match.deactivate()
        self.quit.deactivate()
        self.play_point.activate()
        self.play_game.activate()
        self.play_set.activate()
        self.play_match.activate()
        self.stop_sim.activate()


    def clear(self):
        "Resets scoreboard"
        self.SetsA.setText("")
        self.SetsB.setText("")
        self.GamesA.setText("")
        self.GamesB.setText("")
        self.PointsA.setText("")
        self.PointsB.setText("")
        self.pSetsA1.setText("")
        self.pSetsA2.setText("")
        self.pSetsA3.setText("")
        self.pSetsA4.setText("")
        self.pSetsB1.setText("")
        self.pSetsB2.setText("")
        self.pSetsB3.setText("")
        self.pSetsB4.setText("")
        self.pSets_tie_A1.setText("")
        self.pSets_tie_A2.setText("")
        self.pSets_tie_A3.setText("")
        self.pSets_tie_A4.setText("")
        self.pSets_tie_B1.setText("")
        self.pSets_tie_B2.setText("")
        self.pSets_tie_B3.setText("")
        self.pSets_tie_B4.setText("")
        

    def close(self):
        "Closes window"
        self.win.close()

if __name__ == "__main__":
    main()
