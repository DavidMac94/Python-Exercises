from graphics import *
from time import sleep
from button import Button
from re import match

class conferenceApp:
    def __init__(self):
        # self.attendees will be a dictionary containing the records of all attendees
        self.attendees = dict()
        self.readList()
        self.interface = conferenceInterface(self.attendees)

    def readList(self):
        ''' Import attendees from attendees.txt and saves them in self.attendees. 
        Entries in txt file must be in form "<email>, <name>, <company>, <city>"
        and separated by lines.
        '''
        handle = open('ConferenceAttendees.txt', 'r')
        for line in handle.readlines():
            record = line.strip().split(', ')
            self.attendees[record[0]] = {'name': record[1], 'company': record[2], 'city': record[3]}
            handle.close()
    
    def writeList(self):
        '''Writes updated attendee record to file.'''
        handle = open('ConferenceAttendees.txt', 'w')
        for record in self.attendees:
            handle.write('{0}, {1}, {2}, {3}\n'.format(record, self.attendees[record]['name'],
            self.attendees[record]['company'], self.attendees[record]['city']))
        handle.close()
        
    def run(self):
        '''Runs app and takes action acording to user choice. Display of attendees updates as required.'''
        while True:
            choice = self.interface.getChoice() # gets action from user
            if choice == 'quit': break
            
            elif choice == 'add':
                email, record = addInterface().get()
                if email != False:              # addInterface.get returns False if user chooses cancel
                    self.attendees[email] = record
                self.interface.update(self.attendees)   # update display
                
            elif choice.startswith('delete'):
                email = self.interface.getEmail(int(choice[-1]))   # gets email on line of clicked button
                del self.attendees[email]
                self.interface.update(self.attendees)
                
            elif choice.startswith('edit'):
                # deletes old record and gets new record
                oldEmail = self.interface.getEmail(int(choice[-1]))
                newEmail, record = editInterface(oldEmail, self.attendees[oldEmail]).get()
                del self.attendees[oldEmail]
                if newEmail != False:
                    self.attendees[newEmail] = record
                self.interface.update(self.attendees)
                
            elif choice == 'previous':
                # shows previous page of results
                self.interface.prevPage()
                
            elif choice == 'next':
                # shows next page of results
                self.interface.nextPage()
                
            elif choice == 'search':
                self.interface.searchResults()
                
            elif choice == 'view all':
                self.interface.update(self.attendees)
        self.writeList()  
        

class conferenceInterface:
    def __init__(self, attendees):
        '''Creates GUI for the conference APP. '''
        self.win = GraphWin('Python Conference', 1200, 500)
        self.win.setCoords(0, 17, 10, -1)
        self.win.setBackground(color_rgb(242, 236, 236))
        
        # Draw text
        text_data = [ (Point(5, 0), 'Conference Attendees', 'black', 28, 'courier', 'normal'),
                      (Point(1, 3.9), 'Name', 'darkgray', 16, 'arial', 'bold'), 
                      (Point(3, 3.9), 'Email', 'darkgray', 16, 'arial', 'bold'),
                      (Point(5, 3.9), 'Company', 'darkgray', 16, 'arial', 'bold'),
                      (Point(7, 3.9), 'City', 'darkgray', 16, 'arial', 'bold')]
        text_boxes = []
        for p, txt, col, size, font, style in text_data:
            title = Text(p, txt)
            title.setFill(col)
            title.setSize(size)
            title.setFace(font)
            title.setStyle(style)
            text_boxes.append(title)
            text_boxes[-1].draw(self.win)
        
        # Make text boxes to output data. data_boxes[i][j] is record i while j indicates info from record (1=email,
        # 0=name, 2=company, 3=city).
        pos = 5
        self.data_boxes = []
        for i in range(10):
            self.data_boxes.append([Text(Point(1 + (2 * j), pos), '') for j in range(4)])
            pos += 1
        for i in range(10):
            for j in range(4):
                self.data_boxes[i][j].draw(self.win)
        
        # Make next/previous buttons
        self.prev = Button(self.win, Point(3.5, 15.5), 2, 1, 'Previous')
        self.nex = Button(self.win, Point(6.5, 15.5), 2, 1, 'Next')
        
        # Make edit/delete buttons. Note both are stored in self.edit_buttons
        pos = 5
        self.edit_buttons = []
        for i in range(10):
            self.edit_buttons.append([Button(self.win, Point(8.5, pos), 0.8, 0.8, 'Edit'), Button(self.win, Point(9.5, pos), 0.8, 0.8, 'Delete')])
            pos += 1
        
        # Make add button
        self.add = Button(self.win, Point(9, 3.6), 1.8, 1.2, 'Add Attendee')
        self.add.activate()
        
        # Make quit button
        self.ext = Button(self.win, Point(0.6, 0), 1, 1, 'Exit')
        self.ext.activate()
        
        # Draw lines to separate rows and columns
        lines = []
        for i in range(9):
            lines.append(Line(Point(0, 5.5 + i), Point(10, 5.5 + i)))
            lines[-1].setFill('darkgray')
            lines[-1].draw(self.win)
        for i in range(4):
            lines.append(Line(Point(2 + 2 * i, 3.4), Point(2 + 2 * i, 14.6)))
            lines[-1].setFill('darkgray')
            lines[-1].draw(self.win)
        lines.append(Line(Point(0, 4.4), Point(10, 4.4)))
        lines[-1].setWidth(2)
        lines[-1].draw(self.win)
        lines.append(Line(Point(0, 14.6), Point(10, 14.6)))
        lines[-1].setWidth(2)
        lines[-1].draw(self.win)
        
        # Draw search bar
        self.searchBar = Entry(Point(4, 2), 30)
        self.searchBar.draw(self.win)
        
        # Make search button
        self.search = Button(self.win, Point(6, 2), 1, 1, 'Search')
        self.search.activate()
        
        # Make view all button
        self.viewAll = Button(self.win, Point(7.2, 2), 1, 1, 'View All')
        self.viewAll.activate()
        
        # Initialize page number and text box to display page number.
        self.page = 1
        self.pageNum = Text(Point(5, 15.5), '')
        self.pageNum.draw(self.win)

        # self.records keeps a permanent list of records. self.results keeps search records we want to show.
        self.records = self.listRecords(attendees)
        self.results = self.records[:]
        self.output()

    
    def listRecords(self, dic):
        '''Creates a list (of lists) containing records from the dictionary. The order is name, email, 
        company, city. The list is then ordered by surname.'''
        lst = [[dic[email]['name'], email, dic[email]['company'], dic[email]['city']] for email in dic]
        lst.sort(key = lambda x: x[0].split()[-1].lower())
        return lst
    
    def output(self):
        'Displays first page of attendees and activates buttons accordingly'
        for i in range(min(len(self.results), 10)):
            self.edit_buttons[i][0].activate()
            self.edit_buttons[i][1].activate()
            for j in range(4):
                self.data_boxes[i][j].setText(self.results[i][j])
        if len(self.results) > 10:
            self.nex.activate()
        self.displayPage()
    
    def nextPage(self):
        ' Displays next page of attendees and updates buttons.'
        self.fresh()
        self.page += 1
        self.prev.activate()
        num = 10
        if len(self.results) < self.page * 10:
            num = len(self.results) % 10
        for i in range(num):
            self.edit_buttons[i][0].activate()
            self.edit_buttons[i][1].activate()
            for j in range(4):
                self.data_boxes[i][j].setText(self.results[i + ((self.page - 1) * 10)][j])
        if len(self.results) > self.page * 10:
            self.nex.activate()
        else:
            self.nex.deactivate()
        self.displayPage()
        
    def prevPage(self):
        ' Displays previous page of attendees and updates buttons.'
        self.fresh()
        self.page -= 1
        self.nex.activate()
        num = 10
        for i in range(num):
            self.edit_buttons[i][0].activate()
            self.edit_buttons[i][1].activate()
            for j in range(4):
                self.data_boxes[i][j].setText(self.results[i + ((self.page - 1) * 10)][j])
        if self.page != 1:
            self.prev.activate()
        else:
            self.prev.deactivate()
        self.displayPage()
            
    def update(self, attendees):
        'Updates display of attendees'
        # Converts to list of attendees. If we receive a dictionary (new) then we save to 
        # self.records first.
        if type(attendees) is dict:
            self.records = self.listRecords(attendees)
            self.results = self.records[:]
        else:
            self.results = attendees
        self.page = 1
        self.fresh()
        self.output()
        
    def fresh(self):
        'Resets all text and buttons on display'
        self.prev.deactivate()
        self.nex.deactivate()
        for i in range(10):
            self.edit_buttons[i][0].deactivate()
            self.edit_buttons[i][1].deactivate()
            for j in range(4):
                self.data_boxes[i][j].setText('')
        
    def getChoice(self):
        'Gets choice of what action to take from user.'
        while True:
            pt = self.win.getMouse()
            if self.ext.clicked(pt):
                return 'quit'
            elif self.add.clicked(pt):
                return 'add'
            elif self.prev.clicked(pt):
                return 'previous'
            elif self.nex.clicked(pt):
                return 'next'
            elif [i[0].clicked(pt) for i in self.edit_buttons].count(True) == 1:    # if any edit buttons clicked
                pos = 0
                while True:
                    if self.edit_buttons[pos][0].clicked(pt): break
                    pos += 1
                return 'edit' + str(pos)
            elif [i[1].clicked(pt) for i in self.edit_buttons].count(True) == 1:    # if any delete buttons are clicked
                pos = 0
                while True:
                    if self.edit_buttons[pos][1].clicked(pt): break
                    pos += 1
                return 'delete' + str(pos)
            elif self.prev.clicked(pt):
                return 'previous'
            elif self.nex.clicked(pt):
                return 'next'
            elif self.search.clicked(pt):
                return 'search'
            elif self.viewAll.clicked(pt):
                return 'view all'      
        return choice
    
    def displayPage(self):
        self.pageNum.setText(str(self.page) + ' of ' + str(((len(self.results)-1) // 10)+1))
    
    def getEmail(self, pos):
        "Returns email in position 'pos'."
        return self.data_boxes[pos][1].getText()
    
    def searchResults(self):
        search = self.searchBar.getText()
        results = []
        for attendee in self.records:
            searchFound = False
            for i in range(4):
                if search.lower() in attendee[i].lower():
                    searchFound = True
                    break
            if searchFound == True:
                results.append(attendee)
        self.update(results)
        

class addInterface:
    'Creates GUI for adding a new attendee'
    def __init__(self):
        self.win = GraphWin('Add Attendee', 400, 250)
        self.win.setBackground(color_rgb(242, 236, 236))
        self.win.setCoords(0, 10, 10, 0)
        
        # Create text
        txt_boxes = []
        txt_data = [ (Point(2, 1), 'Name', 'darkgray'),
                     (Point(2, 3), 'Email', 'darkgray'),
                     (Point(2, 5), 'Company', 'darkgray'),
                     (Point(2, 7), 'City', 'darkgray') ]
        for p, txt, col in txt_data:
            txt_boxes.append(Text(p, txt))
            txt_boxes[-1].setFill(col)
            txt_boxes[-1].draw(self.win)
        
        #Create buttons
        self.add = Button(self.win, Point(3,9), 3, 1, 'Add')
        self.cancel = Button(self.win, Point(7, 9), 3, 1, 'Cancel')
        
        #Create entry boxes
        self.entry_boxes = []
        entry_data = [ (Point(7, 1), 20), (Point(7, 3), 20),
                       (Point(7, 5), 20), (Point(7, 7), 20) ]
        for p, w in entry_data:
            self.entry_boxes.append(Entry(p, w))
            self.entry_boxes[-1].draw(self.win)
        
        # initialize msg variable which will be used to report errors in input
        self.msg = None
        
                            
    def get(self):
        '''Gets new attendee. Returns email and a dictionary containing record of attendee. If
        the user chooses to cancel then the method returns False, "".'''
        self.add.activate()
        self.cancel.activate()
        while True:
            pt = self.win.getMouse()
            if self.add.clicked(pt) and self.empty():
                email = self.entry_boxes[1].getText()
                name = self.entry_boxes[0].getText()
                company = self.entry_boxes[2].getText()
                city = self.entry_boxes[3].getText()
                self.win.close()
                return email, {'name': name, 'company': company, 'city': city}
            elif self.add.clicked(pt):
                self.error()
            elif self.cancel.clicked(pt):
                self.win.close()
                return False, ''
        self.win.close
    
    def error(self):
        '''Displays error if a field is empty (that is there must be at least one non-whitepace
        character in each field'''
        if self.msg == None:
            self.msg = Text(Point(5, 8), 'Please fill in all fields')
            self.msg.setFill('red')
            self.msg.draw(self.win)
    
    def empty(self):
        'Returns True if all 4 fields are non-empty, False otherwisde'
        email = match('\S', self.entry_boxes[1].getText())
        name = match('\S', self.entry_boxes[0].getText())
        company = match('\S', self.entry_boxes[2].getText())
        state = match('\S', self.entry_boxes[3].getText())
        
        if email and name and company and state:
            return True
        else:
            return False


class editInterface(addInterface):
    '''GUI for editing an attendee inherited from the add interface. We then place the
    old data in the relevant fields so that the user can edit it.'''
    def __init__(self, email, record):
        addInterface.__init__(self)
        self.entry_boxes[1].setText(email)
        self.entry_boxes[0].setText(record['name'])
        self.entry_boxes[2].setText(record['company'])
        self.entry_boxes[3].setText(record['city'])
    

if __name__ == '__main__': conferenceApp().run()
