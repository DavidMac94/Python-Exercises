from button import Button
from graphics import *
from random import randrange


def main():
    # Create window and buttons
    win = GraphWin("Three Door Monte", 500,400)
    win.setCoords(0, 0, 10, 10)

    door1 = Button(win, Point(2,7), 1.5, 3, "Door 1")
    door2 = Button(win, Point(5,7), 1.5, 3, "Door 2")
    door3 = Button(win, Point(8,7), 1.5, 3, "Door 3")
    play = Button(win, Point(5, 4), 4, 1.5, "Play Game")
    quit_button = Button(win, Point(8, 1), 3, 1, "Quit")
    reset = Button(win, Point(2,1), 3, 1, "Reset")

    # activate play, reset and quit buttons
    play.activate()
    reset.activate()
    quit_button.activate()

    # initialise score counters and displays them
    wins, losses = 0, 0

    Wins = Text(Point(2, 3), str(wins))
    Wins.setTextColor("green")
    Wins.setSize(20)
    Wins.draw(win)

    Losses = Text(Point(8, 3), str(losses))
    Losses.setTextColor("red")
    Losses.setSize(20)
    Losses.draw(win)

    # Get mouse click and enter loop
    pt = win.getMouse()

    while True:
        #Braak loop if quit button is pressed
        if quit_button.clicked(pt):
            break

        # Play a game and update scores if play is pressed
        elif play.clicked(pt):
            correct_door = randrange(1,4)

            play.deactivate()           # activate correct buttons
            reset.deactivate()
            quit_button.deactivate()
            door1.activate()
            door2.activate()
            door3.activate()

            # get a mouse click on one of the doors
            pt = win.getMouse()
            while not (door1.clicked(pt) or door2.clicked(pt) or door3.clicked(pt)):
                pt = win.getMouse()

            # Displays correct answer
            Correct = Text(Point((3 * correct_door) - 1, 5), "Correct")
            Correct.setTextColor("green")
            Correct.draw(win)

            Wrong = Text(Point(2, 5), "Wrong")
            Wrong.setTextColor("red")

            # if guess is wrong, displays 'wrong' underneath guess and updates score counters accordingly
            if not ((correct_door == 1 and door1.clicked(pt)) or (correct_door == 2 and door2.clicked(pt)) or (correct_door == 3 and door3.clicked(pt))):
                if door1.clicked(pt):
                    Wrong.draw(win)
                elif door2.clicked(pt):
                    Wrong.move(3, 0)
                    Wrong.draw(win)
                elif door3.clicked(pt):
                    Wrong.move(6,0)
                    Wrong.draw(win)
                losses += 1
            else:
                wins += 1
            

            play.activate()           # activate correct buttons
            reset.activate()
            quit_button.activate()
            door1.deactivate()
            door2.deactivate()
            door3.deactivate()

            Wins.setText(str(wins))
            Losses.setText(str(losses))

            pt = win.getMouse()

            Correct.undraw()
            Wrong.undraw()
                
                    
                
                

        # Reset scores if reset is pressed
        elif reset.clicked(pt):
            wins, losses = 0, 0
            Wins.setText(str(wins))
            Losses.setText(str(losses))
            
            pt = win.getMouse()

        else:
            pt = win.getMouse()

    win.close()

main()
