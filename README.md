# Python-Exercises
Various programming exercises (mostly from Python Programming: An Introduction to Computer Science)

Wimbledon:
Wimbledon.py accurately simulate a game of tennis on a wimbledon style scoreboard.
The user can choose player names and the probability that each player wins a point on their serve. Once the sim is started,
the program simulates a coinflip to decide who is serving. The user can then press play point to play the next point in
the match until the match is done. The user can also end the sim at any point. The scoreboard has all the same details as the real scoreboard; player names, dot to indicate server,
current set score and previous set scores.

Blackjack:
Blackjack.py implements a simple version of the game blackjack. The user can add funds and then bet an amount of his choosing. The program displays cards in text form and provides a 'running commentary' through messages.
Blackjack rules implemented:
The player plays against a dealer who MUST stick at >16. Both player and dealer are dealt two cards face up initially. The player then plays his hand to completion before the dealer plays. To win, the player must not go bust and have a higher final score than the dealer. The dealer wins in the event of a tie.
Possible improvements include making the game play blackjack as it is played in casino's (split pairs, double down etc). The GUI could also be improved by showing cards visually and by showing chips being bet visually. Possibly add gamble aware settings like max bet, max deposit or max games played before game closes.

Conference:
COnference GUI is a program which keeps track of people attending a conference. It keeps a record of attendees in a file called attendees which the program requires to run. The program allows users to add, edit and delete attendees. The user can also search for attendees. Users can navigate the results by using buttons to change page.
This is obviously a job for a database system but the purpose was to practise using Python lists and dictionaries.
Known Bugs:
Text will extend beyond containers if too long.
Results are shown in order of second name. After that the results will appear in no particular order since records are kept in a (unordered) dictionary. This means the results may appear in a different order in two identical searches.
When no results are displayed, page counter shows page '1 of 0'.
If an attendee is added with a registered email address then the old record will be deleted (the user may want a warning before proceeding).

