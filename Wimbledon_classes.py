# Wimbledon_classes.py
# This file contains classes necessary for Wimbledon.py to run.


from graphics import *
from button import Button


class Button:

    """ The button class creates buttons as described in 'Python Programming: An
    Introdution to Computer Science by John Zelle'.""" 

    def __init__(self, win, centre, width, height, label):
        w, h = width/2.0, height/2.0
        x, y = centre.getX(), centre.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(centre, label)
        self.label.draw(win)
        self.deactivate()

    
    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False

    def clicked(self, p):
        "Returns True if button is active and p is inside."
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        "Returns the label string of the button."
        return self.label.getText()

    
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
        self.win = win = GraphWin("Wimbledon Final", 600, 300)
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
        self.sim_match = Button(win, Point(20, 78), 20, 10, "Sim Match")
        self.play_point = Button(win, Point(50, 78), 20, 10, "Play Point")
        self.stop_sim = Button(win, Point(80, 78), 20, 10, "Stop Sim")
        self.quit = Button(win, Point(50, 93), 20, 10, "Quit")


    def update(self, setsA, setsB, gamesA, gamesB, pointsA, pointsB):
        "Updates board, converting points to tennis equivalent if in a game (i.e. 1=15, 2=30....)"
        self.SetsA.setText(setsA)
        self.SetsB.setText(setsB)
        self.GamesA.setText(gamesA)
        self.GamesB.setText(gamesB)
        tennis_points = ["0", "15", "30", "40", "A"]            
        if (gamesA == 6 and gamesB == 6) or (gamesA == 6 and gamesB == 7) or (gamesA == 7 and gamesA == 6) and (pointsA == "" and pointsB == ""):
            self.PointsA.setText(pointsA)
            self.PointsB.setText(pointsB)
        else:
            self.PointsA.setText(tennis_points[pointsA])
            self.PointsB.setText(tennis_points[pointsB])

            
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
                return "Play"
            elif self.stop_sim.clicked(pt):
                return "Stop"
            elif self.quit.clicked(pt):
                return "Quit"


    def button_outside_match(self):
        "Activates sim_match and quit buttons which are necessary when not in the middle of a match. Deactivates others."
        self.sim_match.activate()
        self.play_point.deactivate()
        self.stop_sim.deactivate()
        self.quit.activate()


    def button_in_match(self):
        "Activates play_point and stop_sim buttons which are necessary during a match. Deactivates others."
        self.sim_match.deactivate()
        self.play_point.activate()
        self.stop_sim.activate()
        self.quit.deactivate()


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
