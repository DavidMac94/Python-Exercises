from graphics import *
from button import Button
from time import sleep
from random import shuffle

class Card:
    '''Creates card object. rank is value in range [1, 13] and suit is
    from ['c', 's', 'd', 'h'].'''

    def __init__(self, rank, suit):
        'Create two instance variables "rank" and "suit"'
        self.rank = rank
        self.suit = suit

    def getRank(self):
        return self.rank

    def getSuit(self):
        return self.suit

    def card_value(self):
        'Return blackjack value of card. (Note ace is 11)'
        rank = self.rank
        if rank == 1:
            value = 11
        elif rank >= 10:
            value = 10
        else:
            value = int(rank)
        return value

    def card_str(self):
        'Returns a short string representing the value of the card'
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
        rank = ranks[self.rank - 1]
        card_string = rank + self.suit
        return card_string

    def card_str_long(self):
        'Returns a long string representing the value of the card'
        ranks = ["Ace", "Deuce", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
        rank = ranks[self.rank - 1]
        if self.suit == "d":
            suit = "Diamonds"
        elif self.suit == "c":
            suit = "Clubs"
        elif self.suit == "h":
            suit = "Hearts"
        else:
            suit = "Spades"
        card_string = rank + " of " + suit
        return card_string



class Deck:
    'Creates a deck of cards (card objects) in a list called "deck".'
    def __init__(self):
        self.deck = []
        for suit in ['c', 'd', 'h', 's']:
            for rank in range(1, 14):
                self.deck.append(Card(rank, suit))

    def shuffle(self):
        'Shuffles deck'
        shuffle
        shuffle(self.deck)

    def dealCard(self):
        'Returns card from top of deck and removes that card from the deck'
        card = self.deck.pop(0)
        return card



class Hand:
    'Hand creates a empty list which cards can be added to represent a blackjack hand'
    def __init__(self):
        self.hand = []

    def add(self, card):
        'Adds card (card object) to hand'
        self.hand.append(card)

    def score(self):
        'Returns blackjack score of hand'
        aces = 0
        for i in self.hand:
            if i.getRank() == 1:
                aces += 1
        total = 0
        for card in self.hand:
            total += card.card_value()
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total
        

    def string(self):
        'Returns a string representing cards in hand'
        string = " ".join([i.card_str() for i in self.hand])
        return string

    



class Chips:

    'This class creates an input box and allows the user to add chips'

    def __init__(self):
        self.win = win = GraphWin("Add Chips", 300, 300)
        self.win.setBackground('blue')
        win.setCoords(0, 5, 4, 0)

        self.chips = Entry(Point(2, 1), 8).draw(win)
        self.chips.setText('0')

        self.add = Button(win, Point(2, 2), 2, 0.8, "Add chips")
        self.add.activate()

        self.exit = Button(win, Point(2,3), 2, 0.8, "Exit")
        self.exit.activate()

    def interact(self):
        'Gets click in input box and takes action accordingly'
        while True:
            pt = self.win.getMouse()
            if self.add.clicked(pt):
                try:
                    a = int(self.chips.getText())
                    if a >= 0:
                        self.win.close()
                        return a  # return chips to be added
                    else:
                        raise ValueError('Negative integer of chips')
                except:
                    # Gives warning and continues if no number is given
                    warning = Text(Point(2,4), 'Enter an integer amount')
                    warning.setFill('red')
                    warning.draw(self.win)
                    pass
            elif self.exit.clicked(pt):
                # exits and returns 0 if quit is clicked and no chips are added
                self.win.close()
                return 0


        

class BlackJackApp:

    'Creates a GUI which allows the user to play a simple version of blackjack'

    def __init__(self):
        
        # Create window
        self.win = GraphWin('Blackjack', 500, 300)
        self.win.setCoords(-0.5, 10.5, 10.5, -0.5)
        self.win.setBackground('blue')
        
        # Create text boxes for lables
        text_data = [ (4, 2, 'DEALER:', 14), (4, 5, 'PLAYER:', 14),
                      (8.7, 4.3, 'CURRENT BET', 14), (0.8, 1.2, 'Please Gamble', 10),
                      (0.8, 1.7, 'Responsibly', 10) ]
        
        text_boxes = []
        for x, y, txt, size in text_data:
            text_boxes.append(Text(Point(x, y), txt))
            text_boxes[-1].setFill('white')
            text_boxes[-1].setSize(size)
            text_boxes[-1].draw(self.win)

        # intialize a variable to track balance through game
        self.balance = 0

        # Create instance variables which can display info to window
        self.message = Text(Point(4, 7.5), '')
        self.message.setSize(22)
        self.message.setFill('white')
        self.message.draw(self.win)
        
        self.dealer_cards_text = Text(Point(4, 3), "")
        self.dealer_cards_text.setFill('white')
        self.dealer_cards_text.setSize(18)
        self.dealer_cards_text.draw(self.win)
        
        self.player_cards_text = Text(Point(4, 6), "")
        self.player_cards_text.setFill('white')
        self.player_cards_text.setSize(18)
        self.player_cards_text.draw(self.win)
        
        self.current_bet_text = Text(Point(8.7, 5.3), "$0")
        self.current_bet_text.setFill('white')
        self.current_bet_text.draw(self.win)
        
        self.balance_text = Text(Point(8.7, 1.5,), "Balance: $" + str(self.balance))
        self.balance_text.setFill('white')
        self.balance_text.draw(self.win)

        # Create buttons
        button_data = [(Point(2.5, 9.2), 2.5, 1, 'HIT'),
                       (Point(5.5, 9.2), 2.5, 1, 'STAND'),
                       (Point(8.7, 0.3), 3, 1, 'ADD CHIPS'),
                       (Point(8.7, 9.2), 2.5, 1, 'BET'),
                       (Point(0.8, 0.3,), 2, 1, 'QUIT') ]
        self.buttons = []
        for point, width, height, label in button_data:
            self.buttons.append(Button(self.win, point, width, height, label))

        # We want to refer to our buttons by name rather than by indexing the
        # the list that contains them
        self.hit = self.buttons[0]
        self.stand = self.buttons[1]
        self.chips = self.buttons[2]
        self.bet = self.buttons[3]
        self.quit = self.buttons[4]

        # Create entry object to allow user to type a bet amount
        self.bet_amount = Entry(Point(8.7, 8), 7)
        self.bet_amount.draw(self.win)

        # Create instance variable representing pause length (in seconds) between actions
        self.pause = 2

        # Activate buttons at launch of game
        self.hand_active(False)
        

    def run(self):
        'Runs Blackjack game'
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                break
            elif self.chips.clicked(pt):
                self.balance += Chips().interact()
                self.balance_text.setText("Balance: $" + str(self.balance))
                # add chips via new window
            elif self.bet.clicked(pt):
                self.play_game()
        self.win.close()
            

    def hand_active(self, active):
        'Activate/deactivates buttons depending on whether hand is in progress'
        if active == True:
            self.hit.activate()
            self.stand.activate()
            self.chips.deactivate()
            self.bet.deactivate()
            self.quit.deactivate()
        if active == False:
            self.hit.deactivate()
            self.stand.deactivate()
            self.chips.activate()
            self.bet.activate()
            self.quit.activate()


    def play_game(self):
        'Plays a game of blackjack, updating text, balances and messages for player'

        # Remove previous cards and messages from diplay
        self.dealer_cards_text.setText('')
        self.player_cards_text.setText('')
        self.dealer_cards_text.setFill('white')
        self.player_cards_text.setFill('white')
        self.message.setText('')
        self.bet_amount.undraw()
        
        # Check if player has enough chips
        self.message.setFill('red')
        try:
            if int(self.bet_amount.getText()) > self.balance:
                self.message.setText('Insufficient Funds')
                self.bet_amount.draw(self.win)
                return
        except:
            self.message.setText('Enter an integer amount')
            self.bet_amount.draw(self.win)
            return

        # Activate in-game buttons
        self.hand_active(True)

        # Update balance and current bet
        current_bet = int(self.bet_amount.getText())
        self.current_bet_text.setText('$' + str(current_bet))
        self.balance -= current_bet
        self.balance_text.setText('Balance: $' + str(self.balance))

        # Get shuffled deck
        deck = Deck()
        deck.shuffle()

        # Create hands for player and dealer
        player = Hand()
        dealer = Hand()

        
        # Deal initial cards and give message with pauses.
        for i in range(2):
            sleep(self.pause)
            card = deck.dealCard()
            dealer.add(card)
            self.message.setFill('white')
            self.message.setText('Dealer draws ' + card.card_str_long())
            self.dealer_cards_text.setText(dealer.string())
            sleep(self.pause)
            card = deck.dealCard()
            player.add(card)
            self.message.setFill('white')
            self.message.setText('Player draws ' + card.card_str_long())
            self.player_cards_text.setText(player.string())

        # Dealer wins if he hits straightaway if he has blackjack


        # Allow user to hit or stand while their score is less than 21 and
        # dealer did not hit blackjack (and so automatically wins).
        while player.score() < 21 and not dealer.score() == 21:
            sleep(self.pause)
            self.message.setFill('white')
            self.message.setText('Hit or Stand?')
            pt = self.win.getMouse()
            if self.hit.clicked(pt):
                card = deck.dealCard()
                player.add(card)
                self.message.setFill('white')
                self.message.setText('Player draws ' + card.card_str_long())
                self.player_cards_text.setText(player.string())
            elif self.stand.clicked(pt):
                self.message.setText('Player stands')
                break


        if player.score() > 21:
            # Player is bust if their score is greater than 21
            sleep(self.pause)
            self.message.setFill('red')
            self.message.setText('Player is bust')

        elif dealer.score() == 21:
            # Dealer wins if they hit blackjack
            sleep(self.pause)
            self.message.setFill('red')
            self.message.setText('Dealer wins with Blackjack')
            
        else:
            # If player is not bust then dealer plays
            while dealer.score() < 17:
                # Dealer sticks after 16
                sleep(self.pause)
                card = deck.dealCard()
                dealer.add(card)
                self.message.setText('Dealer draws ' + card.card_str_long())
                self.dealer_cards_text.setText(dealer.string())

            # Display result of game and update balance if player wins
            if dealer.score() > 21:
                sleep(self.pause)
                self.message.setFill('green')
                self.message.setText('Dealer is bust')
                self.balance += current_bet * 2
                self.balance_text.setText('Balance: $' + str(self.balance))
            elif player.score() <= dealer.score():
                sleep(self.pause)
                self.message.setFill('red')
                self.message.setText('Dealer wins on score')
            else:
                sleep(self.pause)
                self.message.setFill('green')
                self.message.setText('Player wins on score')
                self.balance += current_bet * 2
                self.balance_text.setText('Balance: $' + str(self.balance))

        sleep(self.pause)
        # Remove current bet text and redraw entry box for bet
        self.current_bet_text.setText('')
        self.bet_amount.draw(self.win)
        self.hand_active(False)


BlackJackApp().run()
