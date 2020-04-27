from graphics import *
from random import random
from button import Button

class Player:
    def __init__(self, name, prob):
        self.name = name
        self.prob = prob
        self.points = 0
        self.games = 0
        self.sets = 0
        self.serving = False
        self.previousSetScore1 = ""
        self.previousTiebreakScore1 = ""
        self.previousSetScore2 = ""
        self.previousTiebreakScore2 = ""
        self.previousSetScore3 = ""
        self.previousTiebreakScore3 = ""
        self.previousSetScore4 = ""
        self.previousTiebreakScore4 = ""



class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        
        self.pointWinner = None
        
        self.cointossToDecideInitialServer()
        
    def cointossToDecideInitialServer(self):
        if random() < 0.5:
            self.player1.serving = True
        else:
            self.player2.serving = True
    
    def playPoint(self):
        self.getPointWinner()
        self.updateScore()
        
    def playGame(self):
        while True:
            self.playPoint()
            if self.isNewGame() or self.isMatchDone():
                break
    
    def isNewGame(self):
        return (self.player1.points == 0) and (self.player2.points == 0)
    
    def playSet(self):
        while True:
            self.playGame()
            if self.isNewSet() or self.isMatchDone():
                break
                
    def isNewSet(self):
        return (self.player1.games == 0) and (self.player2.games == 0)
    
    def playMatch(self):
        while not self.isMatchDone():
            self.playSet()
    
    def getPointWinner(self):
        if self.player1.serving:
            if random() < self.player1.prob:
                self.pointWinner = True
            else:
                self.pointWinner = False
        else:
            if random() < self.player2.prob:
                self.pointWinner = False
            else:
                self.pointWinner = True
                
    def updateScore(self):
        if not self.isInTiebreak():
            self.updateGameScore()
        else:
            self.updateTiebreakScore()
    
    def updateGameScore(self):
        if self.pointWinner:
            if self.player1.points <= 3 and self.player2.points <= 3:
                self.player1.points += 1
            elif self.player1.points == 4:
                self.player1.points += 1
            elif self.player2.points == 4:
                self.player2.points -= 1
        else:
            if self.player1.points <= 3 and self.player2.points <= 3:
                self.player2.points += 1
            elif self.player2.points == 4:
                self.player2.points += 1
            elif self.player1.points == 4:
                self.player1.points -= 1
        if self.isGameDone():
            self.updateSetScore()
    
    def updateSetScore(self):
        if self.player1.points > self.player2.points:
            self.player1.games += 1
        else:
            self.player2.games += 1
        self.player1.points, self.player2.points = 0, 0
        self.changeServer()
        if self.isSetDone():
            self.updateMatchScore()
    
    def updateMatchScore(self):
        if self.player1.games > self.player2.games:
            self.player1.sets += 1
        else:
            self.player2.sets += 1
        if not self.isMatch5Sets():
            self.recordPreviousSetScore()
            self.player1.games, self.player2.games = 0, 0
    
    def updateTiebreakScore(self):
        if self.pointWinner:
            self.player1.points += 1
        else:
            self.player2.points += 1
        if self.isTiebreakDone():
            self.updateMatchScoreAfterTiebreak()
        else:
            self.changeServerInTiebreak()
    
    def updateMatchScoreAfterTiebreak(self):
        if self.player1.points > self.player2.points:
            self.player1.games += 1
            self.player1.sets += 1
        else:
            self.player2.games += 1
            self.player2.sets += 1
        if not self.isMatch5Sets():
            self.recordPreviousSetScore()
            self.recordPreviousTiebreakScore()
            self.changeServerAtEndOfTiebreak()
            self.player1.games, self.player2.games = 0, 0
            self.player1.points, self.player2.points = 0, 0
        
    def isInTiebreak(self):
        if self.player1.games == 6 and self.player2.games == 6:
            return True
        else:
            return False
    
    def changeServer(self):
        self.player1.serving = not self.player1.serving
        self.player2.serving = not self.player2.serving
    
    def changeServerInTiebreak(self):
        points = self.player1.points + self.player2.points
        if points % 2 == 1:
            self.changeServer()
    
    def changeServerAtEndOfTiebreak(self):
        points = self.player1.points + self.player2.points
        if points % 4 == 0 or points % 4 == 1:
            self.changeServer()
    
    def isGameDone(self):
        gameDone = False
        if (self.player1.points == 4 and self.player2.points <= 2):
            gameDone = True
        if (self.player2.points == 4 and self.player1.points <= 2):
            gameDone = True
        if self.player1.points == 5 or self.player2.points == 5:
            gameDone = True
        return gameDone
    
    def isTiebreakDone(self):
        tiebreakDone = False
        if (self.player1.points == 7 and self.player2.points <= 5):
            tiebreakDone = True
        if (self.player2.points == 7 and self.player1.points <= 5):
            tiebreakDone = True
        if (self.player1.points >=6 and self.player2.points >= 6 and abs(self.player1.points - self.player2.points) == 2):
            tiebreakDone = True
        return tiebreakDone
    
    def isSetDone(self):
        setDone = False
        if (self.player1.games == 6 and self.player2.games <=4):
            setDone = True
        if (self.player2.games == 6 and self.player1.games <=4):
            setDone = True
        if (self.player1.games == 7 and self.player2.games == 5):
            setDone = True
        if (self.player2.games == 7 and self.player1.games == 5):
            setDone = True
        return setDone
    
    def isMatchDone(self):
        return self.player1.sets == 3 or self.player2.sets == 3
        
    def isMatch5Sets(self):
        setsPlayed = self.player1.sets + self.player2.sets
        return setsPlayed == 5
    
    def recordPreviousSetScore(self):
        sets = self.player1.sets + self.player2.sets
        if sets == 1:
            self.player1.previousSetScore1 = self.player1.games
            self.player2.previousSetScore1 = self.player2.games
        elif sets == 2:
            self.player1.previousSetScore2 = self.player1.games
            self.player2.previousSetScore2 = self.player2.games
        elif sets == 3:
            self.player1.previousSetScore3 = self.player1.games
            self.player2.previousSetScore3 = self.player2.games
        elif sets == 4:
            self.player1.previousSetScore4 = self.player1.games
            self.player2.previousSetScore4 = self.player2.games

    def recordPreviousTiebreakScore(self):
        sets = self.player1.sets + self.player2.sets
        if sets == 1:
            self.player1.previousTiebreakScore1 = self.player1.points
            self.player2.previousTiebreakScore1 = self.player2.points
        elif sets == 2:
            self.player1.previousTiebreakScore2 = self.player1.points
            self.player2.previousTiebreakScore2 = self.player2.points
        elif sets == 3:
            self.player1.previousTiebreakScore3 = self.player1.points
            self.player2.previousTiebreakScore3 = self.player2.points
        elif sets == 4:
            self.player1.previousTiebreakScore4 = self.player1.points
            self.player2.previousTiebreakScore4 = self.player2.points
        

class WimbledonApp:
    def __init__(self):
        self.match = None
        self.userAction = None
        
    def run(self):
        self.gui = WimbledonBoard()
        while True:
            self.userAction = self.gui.receiveUserActionBeforeSim()
            if self.userAction == "Sim":
                self.simulateMatch()
            elif self.userAction == "Quit":
                self.gui.close()
                break
    
    def simulateMatch(self):
        self.ReceiveMatch()
        if self.match != None:
            self.gui.updateBoard(self.match)
            self.playMatch()
            self.match = None
    
    def ReceiveMatch(self):
        inputGui = WimbledonInput()
        inputGui.run()
        if inputGui.isValidMatchGiven():
            self.match = inputGui.returnMatch()
        inputGui.close()

    
    def playMatch(self):
        while not self.isMatchSimulationOver():
            self.userAction = self.gui.receiveUserActionDuringSim()
            self.carryOutUserAction()
            self.gui.updateBoard(self.match)
    
    def isMatchSimulationOver(self):
        if self.match.isMatchDone() or self.userAction == "Stop":
            return True
        else:
            return False
    
    def carryOutUserAction(self):
        if self.userAction == "playPoint":
            self.match.playPoint()
        elif self.userAction == "playGame":
            self.match.playGame()
        elif self.userAction == "playSet":
            self.match.playSet()
        elif self.userAction == "playMatch":
            self.match.playMatch()
        
        
        
        

class WimbledonBoard:
    def __init__(self):
        self.win = win = GraphWin("Wimbledon Final", 600, 300, autoflush = "False")
        win.setCoords(0, 100, 100, 0)
        win.setBackground(color_rgb(0 , 80 , 0))
        
        textData = [ (Point(50, 5), "Final", "white", 24), (Point(50, 15), "Rolex", "gold", 18),
                    (Point(13, 30), "PREVIOUS SETS", "white", 10), (Point(78, 30), "SETS", "white", 10),
                    (Point(86.5, 30), "GAMES", "white", 10), (Point(96, 30), "POINTS", "white", 10),
                    (Point(50, 52), "v", "gold", 17)]
        
        textBoxes = []
        for p, text, colour, size in textData:
            textBox = Text(p, text)
            textBox.setFill(colour)
            textBox.setSize(size)
            textBoxes.append(textBox)
            textBoxes[-1].draw(self.win)
        
        entryData = [ (Point(15,15), 5, "19:15", color_rgb (40 , 40 , 40 ), 20, "gold"),
                    (Point(85,15), 5, "3.35", color_rgb (40 , 40 , 40 ), 20, "gold") ]
        
        entryBoxes = []
        for p, length, text, fill, size, colour in entryData:
            entryBox = Entry(p, length)
            entryBox.setText(text)
            entryBox.setFill(fill)
            entryBox.setSize(size)
            entryBox.setTextColor(colour)
            entryBoxes.append(entryBox)
            entryBoxes[-1].draw(self.win)
        
        Strip = Line(Point(0, 23), Point(100, 23))
        Strip.setWidth(4)
        Strip.setFill("purple")
        Strip.draw(win)
        
        rectangleData = [(Point(2, 48), Point(7, 36)), (Point(8, 48), Point(13, 36)),
                        (Point(14, 48), Point(19, 36)), (Point(20, 48), Point(25, 36)),
                        (Point(2, 68), Point(7, 56)), (Point(8, 68), Point(13, 56)),
                        (Point(14, 68), Point(19, 56)), (Point(20, 68), Point(25, 56)),
                        (Point(8, 48), Point(13, 36)), (Point(27, 48), Point(73, 36)),
                        (Point(27, 68), Point(73, 56)), (Point(75, 48), Point(81, 36)),
                        (Point(83, 48), Point(90, 36)), (Point(92, 48), Point(99, 36)),
                        (Point(75, 68), Point(81, 56)), (Point(83, 68), Point(90, 56)),
                        (Point(92, 68), Point(99, 56)) ]
        
        rectangles = []
        for p1, p2 in rectangleData:
            rectangle = Rectangle(p1, p2)
            rectangle.setFill(color_rgb(40, 40, 40))
            rectangles.append(rectangle)
            rectangles[-1].draw(self.win)
        
        
        self.Player1 = Text(Point(50, 42), "")
        self.Player2 = Text(Point(50, 62), "")
        for i in [self.Player1, self.Player2]:
            i.setFill("gold")
            i.setSize(22)
            i.draw(self.win)
        
        self.player1Set1 = Text(Point(4.5, 42), "")
        self.player1Set2 = Text(Point(10.5, 42), "")
        self.player1Set3 = Text(Point(16.5, 42), "")
        self.player1Set4 = Text(Point(22.5, 42), "")
        self.player2Set1 = Text(Point(4.5, 62), "")
        self.player2Set2 = Text(Point(10.5, 62), "")        
        self.player2Set3 = Text(Point(16.5, 62), "")
        self.player2Set4 = Text(Point(22.5, 62), "")
        self.player1Sets = Text(Point(78, 42), "")
        self.player1Games = Text(Point(86.5, 42), "")
        self.player1Points = Text(Point(95.5, 42), "")
        self.player2Sets = Text(Point(78, 62), "")
        self.player2Games = Text(Point(86.5, 62), "")
        self.player2Points = Text(Point(95.5, 62), "")
        
        for i in [self.player1Set1, self.player1Set2, self.player1Set3, self.player1Set4, 
        self.player2Set1, self.player2Set2, self.player2Set3, self.player2Set4,
        self.player1Sets, self.player1Games, self.player1Points, self.player2Sets,
        self.player2Games, self.player2Points]:
            i.setFill("gold")
            i.setSize(20)
            i.draw(self.win)


        self.player1Tiebreak1 = Text(Point(4.5, 51), "")
        self.player1Tiebreak2 = Text(Point(10.5, 51), "")
        self.player1Tiebreak3 = Text(Point(16.5, 51), "")
        self.player1Tiebreak4 = Text(Point(22.5, 51), "")
        self.player2Tiebreak1 = Text(Point(4.5, 71), "")
        self.player2Tiebreak2 = Text(Point(10.5, 71), "")
        self.player2Tiebreak3 = Text(Point(16.5, 71), "")
        self.player2Tiebreak4 = Text(Point(22.5, 71), "")
        
        for i in [self.player1Tiebreak1, self.player1Tiebreak2, self.player1Tiebreak3, self.player1Tiebreak4,
        self.player2Tiebreak1, self.player2Tiebreak2, self.player2Tiebreak3, self.player2Tiebreak4]:
            i.setFill("white")
            i.setSize(10)
            i.draw(self.win)


        self.player1Serving = Oval(Point(70, 40), Point(72,44))
        self.player1Serving.setFill("gold")

        self.player2Serving = self.player1Serving.clone()
        self.player2Serving.move(0, 20)

        #Create buttons
        self.sim = Button(win, Point(14, 78), 20, 10, "Sim Match")
        self.playPoint = Button(win, Point(38, 78), 20, 10, "Play Point")
        self.playGame = Button(win, Point(38, 93), 20, 10, "Play Game")
        self.playSet = Button(win, Point(62, 78), 20, 10, "Play Set")
        self.playMatch = Button(win, Point(62, 93), 20, 10, "Play Match")
        self.stopSim = Button(win, Point(86, 85.5), 20, 10, "Stop Sim")
        self.Exit = Button(win, Point(14, 93), 20, 10, "Quit")
        
        self.buttonChoice = None
    
    def updateBoard(self, match):
        self.Player1.setText(str(match.player1.name))
        self.Player2.setText(str(match.player2.name))
        
        if match.isInTiebreak() or match.isMatchDone():
            self.player1Points.setText(str(match.player1.points))
            self.player2Points.setText(str(match.player2.points))
        else:
            self.player1Points.setText(self.changeToGameScore(match.player1.points))
            self.player2Points.setText(self.changeToGameScore(match.player2.points))
            
        self.player1Games.setText(str(match.player1.games))
        self.player2Games.setText(str(match.player2.games))
        self.player1Sets.setText(str(match.player1.sets))
        self.player2Sets.setText(str(match.player2.sets))
        
        self.player1Serving.undraw()
        if match.player1.serving:
            self.player1Serving.draw(self.win)
        self.player2Serving.undraw()
        if match.player2.serving:
            self.player2Serving.draw(self.win)
        
        self.player1Set1.setText(str(match.player1.previousSetScore1))
        self.player2Set1.setText(str(match.player2.previousSetScore1))
        self.player1Set2.setText(str(match.player1.previousSetScore2))
        self.player2Set2.setText(str(match.player2.previousSetScore2))
        self.player1Set3.setText(str(match.player1.previousSetScore3))
        self.player2Set3.setText(str(match.player2.previousSetScore3))
        self.player1Set4.setText(str(match.player1.previousSetScore4))
        self.player2Set4.setText(str(match.player2.previousSetScore4))
        self.player1Tiebreak1.setText(str(match.player1.previousTiebreakScore1))
        self.player2Tiebreak1.setText(str(match.player2.previousTiebreakScore1))
        self.player1Tiebreak2.setText(str(match.player1.previousTiebreakScore2))
        self.player2Tiebreak2.setText(str(match.player2.previousTiebreakScore2))
        self.player1Tiebreak3.setText(str(match.player1.previousTiebreakScore3))
        self.player2Tiebreak3.setText(str(match.player2.previousTiebreakScore3))
        self.player1Tiebreak4.setText(str(match.player1.previousTiebreakScore4))
        self.player2Tiebreak4.setText(str(match.player2.previousTiebreakScore4))
    
    def changeToGameScore(self, score):
        gameScores = ["0", "15", "30", "40", "A"]
        return gameScores[score]
    
    def receiveUserActionBeforeSim(self):
        self.activateButtonsBeforeSim()
        self.resetButtonChoice()
        while self.buttonChoice == None:
            pt = self.win.getMouse()
            self.setUserActionBeforeSim(pt)
        return self.buttonChoice
    
    def activateButtonsBeforeSim(self):
        self.sim.activate()
        self.Exit.activate()
        self.playPoint.deactivate()
        self.playGame.deactivate()
        self.playSet.deactivate()
        self.playMatch.deactivate()
        self.stopSim.deactivate()
    
    def setUserActionBeforeSim(self, pt):
        if self.sim.clicked(pt):
            self.buttonChoice = "Sim"
        elif self.Exit.clicked(pt):
            self.buttonChoice = "Quit"
        
    def receiveUserActionDuringSim(self):
        self.activateButtonsDuringSim()
        self.resetButtonChoice()
        while self.buttonChoice == None:
            pt = self.win.getMouse()
            self.setUserActionDuringSim(pt)
        return self.buttonChoice
    
    def activateButtonsDuringSim(self):
        self.sim.deactivate()
        self.Exit.deactivate()
        self.playPoint.activate()
        self.playGame.activate()
        self.playSet.activate()
        self.playMatch.activate()
        self.stopSim.activate()
        
    def setUserActionDuringSim(self, pt):
        if self.playPoint.clicked(pt):
            self.buttonChoice = "playPoint"
        elif self.playGame.clicked(pt):
            self.buttonChoice = "playGame"
        elif self.playSet.clicked(pt):
            self.buttonChoice = "playSet"
        elif self.playMatch.clicked(pt):
            self.buttonChoice = "playMatch"
        elif self.stopSim.clicked(pt):
            self.buttonChoice = "Stop"
    
    def resetButtonChoice(self):
        self.buttonChoice = None
    
    def close(self):
        self.win.close()
        


class WimbledonInput:
    def __init__(self):
        self.win = win = GraphWin("Choose Players", 300, 300)
        win.setCoords(0, 9, 4, 0)

        Text(Point(1, 1), "Player 1:").draw(win)
        self.playerA = Entry(Point(2.7, 1), 18).draw(win)

        Text(Point(1, 2), "Player 2:").draw(win)
        self.playerB = Entry(Point(2.7,2), 18).draw(win)

        Text(Point(1,3), "Prob A*").draw(win)
        self.probA = Entry(Point(2.7,3), 5).draw(win)

        Text(Point(1,4), "Prob B*").draw(win)
        self.probB = Entry(Point(2.7,4), 5).draw(win)

        self.warning1 = Text(Point(2, 8), "*Probability player wins point on serve.").draw(win)
        self.warning2 = Text(Point(2, 8.6), "Enter number in range (0, 1)").draw(win)

        self.sim = Button(win, Point(1, 6), 1.25, .5, "Sim")
        self.sim.activate()

        self.Exit = Button(win, Point(3,6), 1.25, .5, "Exit")
        self.Exit.activate()
        
        self.ValidMatchGiven = None
        self.ValidUserChoiceGiven = None
    
    def run(self):
        while not self.ValidUserChoiceGiven:
            self.checkUserChoice()
        self.close()
    
    def checkUserChoice(self):
        pt = self.win.getMouse()
        if self.sim.clicked(pt) and self.isValidInput():
            self.ValidMatchGiven = True
            self.ValidUserChoiceGiven = True
        elif self.sim.clicked(pt) and (not self.isValidInput()):
            self.displayErrorMessage()
        elif self.Exit.clicked(pt):
            self.ValidUserChoiceGiven = True
    
    def isValidInput(self):
        try:
            a = float(self.probA.getText())
            b = float(self.probB.getText())
            if 0 < a < 1 and 0 < b < 1:
                return True
            else:
                return False
        except:
            return False
        
    def isValidMatchGiven(self):
        return self.ValidMatchGiven
    
    def displayErrorMessage(self):
        self.warning1.setFill("red")
        self.warning2.setFill("red")
    
    def returnMatch(self):
        player1 = Player(self.playerA.getText(), float(self.probA.getText()))
        player2 = Player(self.playerB.getText(), float(self.probB.getText()))
        return Match(player1, player2)
    
    def close(self):
        self.win.close()

def main():
    WimbledonApp().run()

if __name__ == "__main__": main()