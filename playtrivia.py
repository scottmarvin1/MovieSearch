##
# playtrivia.py
# PlayTrivia class. Manages a round of trivia
# name: Gregory Marvin
##

import tkinter as tk
import tkinter.messagebox as tkmb

class PlayTrivia(tk.Toplevel) :
    def __init__(self, master, chosenMovie) :
        
        tk.Toplevel.__init__(self, master) # override constructor for Toplevel window
        
        self.resizable(False, False)
        
        self.grab_set() # make the trivia game take the focus from DisplayInfo
        
        self.title("Trivia!") # set the title to something, otherwise master's title is recycled
    
        self.protocol("WM_DELETE_WINDOW", self.cancel) # if window is closed, call cancel to clean up
    
        self._master = master # set master for use in PlayTrivia methods
        
        self.initial_focus = self # make the initial focus self
        
        self.chosenMovie = chosenMovie # set the MovieDatat object for use in PlayTrivia methods
        
        # set up labels and entry boxes for question 1, naming an actor or actress
        self.q1Text = tk.StringVar()
        self.q1Answer = tk.StringVar()
        self.q1Text.set("1. Name an actor/actress from %s." %chosenMovie.movie_technical_info['title'])
        self.q1Label = tk.Label(self, textvariable=self.q1Text).grid(row=0, columnspan=2, sticky='w')  
        self.q1Entry = tk.Entry(self, textvariable=self.q1Answer, width=40).grid(row=1, columnspan=2, sticky='w')
        
        # set up labels and entry boxes for question 2, naming a writer or director
        self.q2Text = tk.StringVar()
        self.q2Answer = tk.StringVar()
        self.q2Text.set("2. Name a Director from %s." %chosenMovie.movie_technical_info['title'])
        self.q2Label = tk.Label(self, textvariable=self.q2Text).grid(row=2, columnspan=2, sticky='w')
        self.q2Entry = tk.Entry(self, textvariable=self.q2Answer, width=40).grid(row=3, columnspan=2, sticky='w')
        
        # set up labels and entry boxes for question 3, for the runtime of the movie in minutes
        self.q3Text = tk.StringVar()
        self.q3Answer = tk.StringVar()
        self.q3Text.set("3. How many minutes long is %s?(only digits)" %chosenMovie.movie_technical_info['title'])
        self.q3Label = tk.Label(self, textvariable=self.q3Text).grid(row=4, columnspan=2, sticky='w')
        self.q3Entry = tk.Entry(self, textvariable=self.q3Answer, width=40).grid(row=5, columnspan=2, sticky='w')
        
        # set up labels and entry boxes for question 4, for the MPAA rating
        self.q4Text = tk.StringVar()
        self.q4Answer = tk.StringVar()
        self.q4Text.set("4. What is the MPAA rating for %s?" %chosenMovie.movie_technical_info['title'])
        self.q4Label = tk.Label(self, textvariable=self.q4Text).grid(row=6, columnspan=2, sticky='w')
        self.q4Entry = tk.Entry(self, textvariable=self.q4Answer, width=40).grid(row=7, columnspan=2, sticky='w')
        
        # set up labels and entry boxes for question 5, for the IMDB rating
        self.q5Text = tk.StringVar()
        self.q5Answer = tk.StringVar()
        self.q5Text.set("5. What is the IMDB rating for %s?" %chosenMovie.movie_technical_info['title'])
        self.q5Label = tk.Label(self, textvariable=self.q5Text).grid(row=8, columnspan=2, sticky='w')
        self.q5Entry = tk.Entry(self, textvariable=self.q5Answer, width=40).grid(row=9, columnspan=2, sticky='w')
        
        # create and set up ok and cancel buttons for the game
        self.okButton = tk.Button(self, text="OK", width=10, command=self.ok)
        self.okButton.grid(padx=5, pady=5, row=12, sticky='e')
        self.cancelButton = tk.Button(self, text="Cancel", width=10, command=self.cancel)
        self.cancelButton.grid(padx=5, pady=5, row=12, column=1, sticky='w')
        

        
        if not self.initial_focus:              # if focus is not on a widget, then focus is Dialog 
            self.initial_focus = self
        self.initial_focus.focus_set()          # set the focus                
        
        self.bind("<Return>", self.return_)        # bind() method connects a pressed key event   
        self.bind("<Escape>", self.cancel)         # to a method through a callback               
        
        self.transient(master)
        self.geometry("+%d+%d" % (master.winfo_rootx()+50, master.winfo_rooty()+50))
        self.wait_window(self)        
        
    def apply(self) :
        '''apply method to fetch the answers to the trivia questions'''
        self.resultList = [self.q1Answer.get(), self.q2Answer.get(), self.q3Answer.get(), self.q4Answer.get(), self.q5Answer.get()]
        
    def validate(self) :
        '''validate method to make sure user doesn't leave any blanks in the trivia questions'''
        valid = True # assume true to begin
        
        # just a simple check to ensure no empty entries
        if self.q1Answer.get() == "" or \
           self.q2Answer.get() == "" or \
           self.q3Answer.get() == "" or \
           self.q4Answer.get() == "" or \
           self.q5Answer.get() == "" :
            valid = False
        
        return valid
    
    def checkResults(self) :
        '''checkResults method, compares answered entered by the user to the values in fetched movie data'''
        numCorrect = 0 # initially none are correct, cause none have been checked
        
        # if a supplied actor/actress is in the list of actors generated
        if self.resultList[0].title().strip() in self.chosenMovie.movie_technical_info['actors'].split(', ') :
            numCorrect += 1 # add a point to the correct total
        
        # if a supplied writer/director is in either writer or director list generated    
        if self.resultList[1].title().strip() in self.chosenMovie.movie_technical_info['director'].split(', ') :
            numCorrect += 1 # add a point to the correct total
        
        # if the entered runtime is the same as the generated one
        runtime = self.chosenMovie.movie_technical_info['runtime'].replace(' min', '').strip()   
        if self.resultList[2] == runtime :
            numCorrect += 1 # add a point to the correct total
        
        # if the rating provided matches the rating generated
        if self.resultList[3].upper().strip() == "PG13" : self.resultList[3] = 'PG-13' # insert hyphen if not there
        if self.resultList[3].upper().strip() == self.chosenMovie.movie_technical_info['rated'] :
            numCorrect += 1 # add a point to the correct total
        
        # if the entered IMDB rating matches the generated one
        if self.resultList[4].strip() == self.chosenMovie.movie_technical_info['imdb_rating'] :
            numCorrect += 1# add a point to the correct total
        
        # if the user gets 4 or 5 correct, well done
        if numCorrect > 3 : 
            tkmb.showinfo("Well done!", "You answered %d/5 correct." %numCorrect)
        # if the user gets 2 or 3 correct, not bad
        elif numCorrect <= 3 and numCorrect > 1 :
            tkmb.showinfo("Not bad!", "You answered %d/5 correct." %numCorrect)
        # if the user gets 0 or 1 correct, better luck next time
        else :
            tkmb.showinfo("Better luck next time!", "You answered %d/5 correct.\nUse the info available if you need." %numCorrect)
    
    def ok(self, *args) :
        """[Ok] button to commit change"""
        if not self.validate():                     # if not valid
            self.initial_focus.focus_set()          # put focus back to initial focus
            return
        
        self.apply()                # if everything is valid, then store input data into result
        self.checkResults()         # check the answers entered by the user
        self.cancel()               # go to close window
        
    def return_(self, *args) :
        """Hitting return will run the button that has focus"""
        if self.focus_get() == self.cancelButton:
            self.cancel()
        elif self.focus_get() == self.okButton:
            self.ok()    
        
    def cancel(self, *args) :
        """[Cancel] button to close window"""
        self._master.focus_set()        # set focus back to the master window
        self.destroy()                  # close window            
