import json
from graphics import *
from time import sleep

class ATM:
    '''ATM performs the operations of an ATM.
    
    The class reads account information from accounts.json.
    This class handles basic operations like withdraw, transfer,
    change pin and view balances. All account balance values are
    stored in pence as integers.'''
    
    def __init__(self):
        self.accounts = None
        self.readAccounts()
        # Initialize interface to be used by ATM.
        self.interface = ATMInterface()

    def readAccounts(self):
        '''Gets account information from accounts.json and
        saves in self.accounts'''
        handle = open('ATMaccounts.json', 'r')
        self.accounts = json.loads(handle.read())
        handle.close()
        
    def writeAccounts(self):
        '''Writes accounts information to accounts.json'''
        handle = open('ATMaccounts.json', 'w')
        handle.write(json.dumps(self.accounts))
        handle.close()
        
    def run(self):
        '''Runs ATM. ATM keeps running until forced close.'''
        while True:
            # Get user and pin from interface
            user, pin = self.interface.access()
            # if user cancels then continue (back to main menu)
            if user == None or pin == None:
                continue
            elif self.access(user, pin):    # correct ID + PIN combo
                self.uIndex = self.userIndex(user)
                while True:
                    self.readAccounts()
                    choice = self.interface.choice()
                    # Get choice of action, get input then take relevant action.
                    if choice == 'cash':
                        cash = self.interface.cash()
                        self.withdraw(cash)
                    elif choice == 'view':
                        self.interface.view(self.accounts['users'][self.uIndex]['main'], self.accounts['users'][self.uIndex]['savings'])
                    elif choice == 'transfer':
                        save, amount = self.interface.transfer()
                        self.accountTransfer(save, amount)
                    elif choice == 'change':
                        newPIN = self.interface.changePIN()
                        self.changePIN(newPIN)
                    elif choice == 'exit':
                        break
            else:
                self.interface.error() # Tell user that ID + PIN incorrect

    def userIndex(self, user):
        '''Returns index of user account in list of accounts'''
        pos = 0
        while pos < len(self.accounts['users']):
            if self.accounts['users'][pos]['userID'] == user:
                break
            pos += 1
        return pos

    def access(self, user, pin):
        '''Returns true if user and ID match, false otherwise'''
        if any((d['userID'] == user) and (d['pin'] == pin) for d in self.accounts['users']):
            return True
        else:
            return False
    
    def accountTransfer(self, save, amount):
        '''Updates account balances from transfer if necessary. If save is None, this means
        user cancelled during transfer and so no action should be taken.'''
        if save != None and amount != None:
            amount = int(amount)
            if amount > 0:
                if save == True:
                    if amount <= self.accounts['users'][self.uIndex]['main']:
                        self.accounts['users'][self.uIndex]['main'] -= int(amount)
                        self.accounts['users'][self.uIndex]['savings'] += int(amount)
                        self.interface.transferDone(save, amount)
                    else:
                        self.interface.insufficient()
                else:
                    if amount <= self.accounts['users'][self.uIndex]['savings']:
                        self.accounts['users'][self.uIndex]['main'] += int(amount)
                        self.accounts['users'][self.uIndex]['savings'] -= int(amount)
                        self.interface.transferDone(save, amount)
                    else:
                        self.interface.insufficient()
            self.writeAccounts()

    def withdraw(self, cash):
        '''Updates cash from account. Gives error message if there is
        insufficient funds.'''
        if cash != None:
            if int(cash) <= self.accounts['users'][self.uIndex]['main']:
                self.accounts['users'][self.uIndex]['main'] -= int(cash)
                self.interface.takeCash()
                self.writeAccounts()
            else:
                self.interface.insufficient()

    def changePIN(self, pin):
        '''Updates pin if user enters matching pins. If they are incorrect then
        an error message is displayed.'''
        if pin not in [None, False]:
            self.accounts['users'][self.uIndex]['pin'] = pin
            self.writeAccounts()
            self.interface.pinUpdated(True)
        elif pin == False:
            self.interface.pinUpdated(False)
        

class ATMInterface:
    '''This class provides an inteface to be used with the ATM class. 
    
    The interface is a close approximation to a real life ATM. The user
    has buttons down the side of the screen as well as a keypad. The user
    uses the keypad followed by enter to information. During input, the
    user can press clear to clear the input or cancel to terminate the
    operation.'''
    
    def __init__(self):
        
        # Make buttons for keypad. self.keypad[i] represents the buttons.
        # for i in [0, 9].  
        self.win = GraphWin('ATM', 800, 600)
        self.win.setCoords(0, 30, 40, 0)
        self.win.setBackground('darkgray')
        
        buttons_data = [ (Point(17.4, 28), 2.2, 2.2, '0'), (Point(14.4, 25), 2.2, 2.2, '1'),
                         (Point(17.4, 25), 2.2, 2.2, '2'), (Point(20.4, 25), 2.2, 2.2, '3'),
                         (Point(14.4, 22), 2.2, 2.2, '4'), (Point(17.4, 22), 2.2, 2.2, '5'),
                         (Point(20.4, 22), 2.2, 2.2, '6'), (Point(14.4, 19), 2.2, 2.2, '7'),
                         (Point(17.4, 19), 2.2, 2.2, '8'), (Point(20.4, 19), 2.2, 2.2, '9') ]
        self.keypad = []
        for p, w, h, label in buttons_data:
            button = Button(self.win, p, w, h, label)
            button.activate()
            self.keypad.append(button)
        
        # Make buttons for enter, clear and cancel.
        self.enter = Button(self.win, Point(24.5, 19), 4.4, 2.2, 'ENTER')
        self.clear = Button(self.win, Point(24.5, 22), 4.4, 2.2, 'CLEAR')
        self.cancel = Button(self.win, Point(24.5, 25), 4.4, 2.2, 'CANCEL')
        self.enter.activate()
        self.clear.activate()
        self.cancel.activate()
        
        # Make buttons for side of screen. Indexing starts from top left and
        # snakes down to bottom right.
        buttons_data = [ (Point(6, 5.2), 7, 2, ''), (Point(34, 5.2), 7, 2, ''),
                         (Point(6, 8.4), 7, 2, ''), (Point(34, 8.4), 7, 2, ''),
                         (Point(6, 11.6), 7, 2, ''), (Point(34, 11.6), 7, 2, ''),
                         (Point(6, 14.8), 7, 2, ''), (Point(34, 14.8), 7, 2, '') ]
        self.buttons = []
        for p, w, h, label in buttons_data:
            button = Button(self.win, p, w, h, label)
            self.buttons.append(button)
        
        # Make Screen
        screen = Rectangle(Point(10,1), Point(30, 17))
        screen.setFill('black')
        screen.draw(self.win)
        
        # Make text boxes
        self.welcome = Text(Point(20, 2), 'The Bank of Python')
        self.welcome.setSize(24)
        self.welcome.setFill('white')
        self.welcome.setFace('courier')
        self.welcome.draw(self.win)
        
        self.msg = Text(Point(20, 7), '')
        self.msg.setSize(28)
        self.msg.setFill('white')
        self.msg.draw(self.win)
        
        # Make text boxes to display pin as user types.
        enter_data = [ (Point(17, 10), ''), (Point(19, 10), ''),
                         (Point(21, 10), ''), (Point(23, 10), '') ]
        self.accessText = []
        for p, label in enter_data:
            text = Text(p, label)
            text.setSize(28)
            text.setFill('white')
            text.setStyle('bold')
            text.draw(self.win)
            self.accessText.append(text)
        
        # Make text boxes to display balances.
        balance_data = [ (Point(20, 6), ''), (Point(20, 9), '') ]
        self.balances = []
        for p, text in balance_data:
            balance = Text(p, text)
            balance.setSize(20)
            balance.setFill('white')
            balance.draw(self.win)
            self.balances.append(balance)
        
        # Make text boxes to display options. The strings put in these 
        # boxes will require manipulation to be aligned closely with button.
        options_data = [ (Point(14.5, 5.2), ''), (Point(25.5, 5.2), ''),
                         (Point(14.5, 8.4), ''), (Point(25.5, 8.4), ''),
                         (Point(14.5, 11.6), ''), (Point(25.5, 11.6), ''),
                         (Point(14.5, 14.8), ''), (Point(25.5, 14.8), '') ]
        self.options = []
        for p, text in options_data:
            text = Text(p, text)
            text.setFill('green')
            text.draw(self.win)
            self.options.append(text)
        
        # Make text boxes to display amounts as user types. self.amount[i]
        # is the amount for i in [0,4] and then the decimal point and pound symbol
        # are stored at index 5 and 6.
        amount_data = [ (Point(16, 10), ''), (Point(18, 10), ''),
                        (Point(20, 10), ''), (Point(24, 10), ''), 
                        (Point(26, 10), ''), (Point(22, 10), ''),
                        (Point(14, 10), '') ]
        self.amount = []
        for p, text in amount_data:
            text = Text(p, text)
            text.setFill('white')
            text.setSize(36)
            text.setStyle('bold')
            text.draw(self.win)
            self.amount.append(text)
        
        # Give user sample ID/pin to test program.
        
        self.sample = Text(Point(5, 28), 'Test Account Details\nUser ID: 0000\nPin: 0000')
        self.sample.draw(self.win)

    def access(self):
        '''Gets user ID and PIN from user. If the user cancels
        during either input process then getDigits returns None.'''
        
        self.msg.setText('Enter ID')
        user = self.getDigits()
        if user != None:
            self.msg.setText('Enter Pin')
            pin = self.getDigits()
        else:
            pin = None
        self.clearScreen()
        return user, pin

    def choice(self):
        '''Gets choice of action from user and returns it in a string.'''
        
        for i in [0,2,4,6,7]:
            self.buttons[i].activate()
        # Text is formatted to align nicely with button.
        self.options[0].setText('{:20}'.format('Withdraw Cash'))
        self.options[2].setText('{:20}'.format('View Balances'))
        self.options[4].setText('{:28}'.format('Transfer'))
        self.options[6].setText('{:25}'.format('Change Pin'))
        self.options[7].setText('{:>30}'.format('Exit'))
        while True:
            pt = self.win.getMouse()
            if self.buttons[0].clicked(pt):
                choice = 'cash'
                break
            elif self.buttons[2].clicked(pt):
                choice = 'view'
                break
            elif self.buttons[4].clicked(pt):
                choice = 'transfer'
                break
            elif self.buttons[6].clicked(pt):
                choice = 'change'
                break
            elif self.buttons[7].clicked(pt):
                choice = 'exit'
                break
        self.clearScreen()
        return choice

    def cash(self):
        '''Gets amount of cash the user would like to withdraw. Returns
        None if user cancels during any stage of input.'''
        
        # cashOptions[5] is empty string to allow us to index more easily
        # later in method.
        cashOptions = ['5', '100', '10', '300', '20','', '50']
        for i in range(8):
            self.buttons[i].activate()
        for i in [0,2,4,6]:
            self.options[i].setText('{:30}'.format('£' + cashOptions[i]))
        for i in [1,3]:
            self.options[i].setText('{:>30}'.format('£' + cashOptions[i]))
        self.options[5].setText('{:>22}'.format('Enter Amount'))
        self.options[7].setText('{:>23}'.format('Main Menu'))
        
        while True:
            pt = self.win.getMouse()
            
            # If one of the cash option buttons is clicked then the choice
            # is stored in buttonClick. Otherwise buttonClick is None.
            if True in [self.buttons[i].clicked(pt) for i in [0,1,2,3,4,6,]]:
                buttonClick = [self.buttons[i].clicked(pt) for i in range(7)].index(True)
            else:
                buttonClick = None
            
            if buttonClick != None:
                cash = int(cashOptions[buttonClick]) * 100
                break
            elif self.buttons[5].clicked(pt):
                # call getAmount method to get user defined cash amount.
                self.clearScreen()
                cash = self.getAmount()
                # if cash is None (i.e. the user cancels during input then
                # we take no action.
                if cash!= None:
                    cash = int(cash)
                break
            elif self.buttons[7].clicked(pt):
                cash = None
                break
        self.clearScreen()       
        return cash

    def getDigits(self):
        '''Returns 4 digit number from user. Entered using keypad.'''
        
        pos = 0
        while True:
            pt = self.win.getMouse()
            
            # If a keypad number is clicked then it is stored in keypadClick.
            # Otherwise keypadClick is None.
            if True in [self.keypad[i].clicked(pt) for i in range(10)]:
                keypadClick = [self.keypad[i].clicked(pt) for i in range(10)].index(True)
            else:
                keypadClick = None
            
            # Gets available input from user depending on how many digit they have
            # already entered. They cannot click enter if they have not typed 4 digits,
            # they cannot click a digit if they have already entered 4 etc..
            # At any stage they can click cancel as usual to cancel input (which 
            # returns None).
            if pos == 0:
                if keypadClick != None:
                    self.accessText[pos].setText(str(keypadClick))
                    pos += 1
                elif self.cancel.clicked(pt):
                    digits = None
                    break
            elif 0 < pos < 4:
                if keypadClick != None:
                    self.accessText[pos].setText(str(keypadClick))
                    pos += 1
                elif self.cancel.clicked(pt):
                    digits = None
                    break
                elif self.clear.clicked(pt):
                    for i in range(4):
                        self.accessText[i].setText('')
                        pos = 0
            elif pos == 4:
                if self.cancel.clicked(pt):
                    digits = None
                    break
                elif self.clear.clicked(pt):
                    for i in range(4):
                        self.accessText[i].setText('')
                        pos = 0
                elif self.enter.clicked(pt):
                    digits = ''
                    for i in range(4):
                        digits += self.accessText[i].getText()
                    break
        self.clearScreen()
        return digits

    def getAmount(self):
        '''Gets amount entered by user up to £999.99. Similar to getDigits except
        that as digits are entered it pushes the existing digits one place to the
        left as in a real life ATM. Of cours it also allows the user to enter an amount
        which is less than 5 digits.'''
        
        self.msg.setText('Enter Amount')
        self.amount[5].setText('.')
        self.amount[6].setText('£')
        pos = 0
        while True:
            pt = self.win.getMouse()
            if True in [self.keypad[i].clicked(pt) for i in range(10)]:
                keypadClick = [self.keypad[i].clicked(pt) for i in range(10)].index(True)
            else:
                keypadClick = None
            if pos == 0:
                if keypadClick != None:
                    self.amount[4].setText(str(keypadClick))
                    pos += 1
                elif self.cancel.clicked(pt):
                    cash = None
                    break
            elif 0 < pos < 5:
                if keypadClick != None:
                    # The following code does the 'pushing' of the digits.
                    for i in range(pos):
                        self.amount[4-pos+i].setText(self.amount[5-pos+i].getText())
                    self.amount[4].setText(str(keypadClick))
                    pos += 1
                elif self.cancel.clicked(pt):
                    cash = None
                    break
                elif self.enter.clicked(pt):
                    cash = ''
                    for i in range(5):
                        cash += self.amount[i].getText()
                    break
                elif self.clear.clicked(pt):
                    for i in range(5):
                        self.amount[i].setText('')
                        pos = 0
            elif pos == 5:
                if self.cancel.clicked(pt):
                    cash = None
                    break
                elif self.clear.clicked(pt):
                    for i in range(5):
                        self.amount[i].setText('')
                        pos = 0
                elif self.enter.clicked(pt):
                    cash = ''
                    for i in range(5):
                        cash += self.amount[i].getText()
                    break
        self.clearScreen()
        return cash
    
    def insufficient(self):
        '''Displays message to user that they have insufficient funds.'''
        self.msg.setText('Insufficient Funds')
        sleep(2)
        self.clearScreen()
        
    def takeCash(self):
        '''Displays message to user to take their cash.'''
        self.msg.setText('Please take your cash')
        sleep(2)
        self.clearScreen()
        
    def view(self, main, savings):
        '''Displays account balances.'''
        
        main = '{0:.2f}'.format(main/100)
        savings = '{0:.2f}'.format(savings/100)
        self.buttons[7].activate()
        self.options[7].setText('{:>27}'.format('Main Menu'))
        self.balances[0].setText('Main Balance: £' + main)
        self.balances[1].setText('Savings Balance: £' + savings)
        while True:
            pt = self.win.getMouse()
            if self.buttons[7].clicked(pt):
                break
        self.clearScreen()

    def transfer(self):
        '''Gets amount and type of transfer. save is True if user chooses to
        transfer to savings and False otherwise. If the user cancels at any
        stage then None, None is returned.'''
        for i, text in [(1, 'Main to Savings'),(3, 'Savings to Main')]:
            self.buttons[i].activate()
            self.options[i].setText('{:>20}'.format(text))
        self.buttons[7].activate()
        self.options[7].setText('{:>23}'.format('Main Menu'))
        while True:
            pt = self.win.getMouse()
            if self.buttons[1].clicked(pt):
                self.clearScreen()
                amount = self.getAmount()
                save = True
                break
            elif self.buttons[3].clicked(pt):
                self.clearScreen()
                amount = self.getAmount()
                save = False
                break
            elif self.buttons[7].clicked(pt):
                amount = None
                save = None
                break
        self.clearScreen()
        return save, amount    

    def clearScreen(self):
        '''Clears screen of any text'''
        self.msg.setText('')
        for i in range(4):
            self.accessText[i].setText('')
        for i in range(7):
            self.amount[i].setText('')
        for i in range(8):
            self.options[i].setText('')
            self.buttons[i].deactivate()
        for i in range(2):
            self.balances[i].setText('')

    def transferDone(self, save, amount):
        '''Displays message to user that their transfer has been done,'''
        
        if save == True:
            self.balances[0].setText('£' + '{0:.2f}'.format(amount/100) + ' transferred to savings')
        else:
            self.balances[1].setText('£' + '{0:.2f}'.format(amount/100) + ' transferred to main')
        sleep(3)
        self.clearScreen()

    def changePIN(self):
        '''Returns PIN that user enters. User must enter twice to successfully change
        PIN. If user cancels then None is returned. If the pins do not match then False
        is returned.'''
        self.msg.setText('Enter New PIN')
        pin1 = self.getDigits()
        if pin1 != None:
            self.msg.setText('Re-enter New PIN')
            pin2 = self.getDigits()
            if pin2!= None:
                if pin1 == pin2:
                    pin = pin1
                else:
                    pin = False
            else:
                pin = None
        else:
            pin = None
        self.clearScreen()
        return pin
    
    def pinUpdated(self, true):
        '''Displays message to user that either their pin has been updated successfully
        or that the pins entered did not match.'''
        
        if true == True:
            self.msg.setText('Pin Updated')
        else:
            self.msg.setText('Pins Do Not Match')
        sleep(2)
        self.clearScreen()

    def error(self):
        '''Displays message to user that their pin is incorrect.'''
        
        self.msg.setText('Incorrect PIN')
        sleep(2)
        self.clearScreen()


if __name__ == '__main__': ATM().run()
