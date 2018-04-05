##
# entermovie.py
# EnterMovie class. Sets up pop up window for selecting movie
# name: Gregory Marvin & Ryan Oliveira
##

import tkinter as tk

class EnterMovie(tk.Toplevel) :
    def __init__(self, master, title="Pick a movie") :
        
        tk.Toplevel.__init__(self, master) # override Toplevel constructor
        
        self.resizable(False, False)
        
        self.grab_set() # grab focus from MovieSearch
        
        self.protocol("WM_DELETE_WINDOW", self.cancel) # if window is closed, call cancel to clean up
        
        self._master = master # set master for use in EnterMovie methods
        self.initial_focus = self # set initial focus to itself
        self.title(title) # set the title with the provided value
        
        # create label and entry box for the user to enter a movie
        self.usersMovie = tk.StringVar()
        self.choice = None
        self.message = tk.Label(self, text="Enter a Movie", fg='black')
        self.message.grid(columnspan=3, sticky='e'+'w')
        self.movieEntry = tk.Entry(self, textvariable=self.usersMovie).grid(row=1, column=0, columnspan=3)
        
        # create ok and cancel buttons for the entered movie
        self.okButton = tk.Button(self, text="OK", width=10, command=self.ok)
        self.okButton.grid(padx=5, pady=5, row=2, sticky='w')
        self.cancelButton = tk.Button(self, text="Cancel", width=10, command=self.cancel)
        self.cancelButton.grid(padx=5, pady=5, row=2, column=2, sticky='w')
        

        if not self.initial_focus:              # if focus is not on a widget, then focus is Dialog 
            self.initial_focus = self
        self.initial_focus.focus_set()          # set the focus                
        
        self.bind("<Return>", self.return_)        # bind() method connects a pressed key event   
        self.bind("<Escape>", self.cancel)         # to a method through a callback               
        
        self.transient(master)
        self.geometry("+%d+%d" % (master.winfo_rootx()+50, master.winfo_rooty()+50))
        self.wait_window(self)
        
    def apply(self) :
        '''apply method, sets the choice selected by the user'''
        self.choice = self.usersMovie.get().strip()
        
    #def getChoice(self) :
    #    return self.choice
    
    def validate(self) :
        '''validate method to make sure user doesn't leave any blanks in the trivia questions'''
        valid = True # assume valid to start off
        
        # if user only enters whitespace or doesnt commit the entered movie, invalid entry
        if self.usersMovie.get().strip() == "" or self.usersMovie.get() == None :
            valid = False
        
        return valid
    
    def ok(self, *args) :
        '''ok method, applies the choice selected and calls to cancel the window'''
        if not self.validate():                     # if not valid
            self.initial_focus.focus_set()          # put focus back to initial focus
            return
        
        # commit entered movie, clean up and close window
        self.apply()
        self.cancel()
        
    def return_(self, *args):
        '''Hitting return will run the button that has focus'''
        if self.focus_get() == self.cancelButton:
            self.cancel()
        elif self.focus_get() == self.okButton:
            self.ok()
      
    def cancel(self, *args):
        '''[Cancel] button to close window'''
        self._master.focus_set()    # set focus back to the master window
        self.destroy()              # close window    
        