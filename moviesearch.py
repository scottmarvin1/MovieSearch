##
# moviesearch.py
# MovieSearch class. Sets up the main window for the application
# name: Gregory Marvin & Ryan Oliveira
##

import tkinter as tk
from entermovie import EnterMovie
from displayinfo import DisplayInfo

class MovieSearch(tk.Tk, EnterMovie) :
    def __init__(self) :
        super().__init__()
        
        self.title("Movie Search!") # set the title for the window
        
        self.resizable(False, False)
        
        # set up and display a welcome message
        self.message = tk.StringVar()
        self.message.set("Welcome to Movie Search!\n Hope you enjoy!")
        self.welcome = tk.Label(self, padx=5, textvariable=self.message, fg='black')
        self.welcome.grid(row=1, columnspan=3, sticky='ew')
        
        # create button to start the search
        self.begin = tk.Button(self, text="Click to begin!", command=self.selectMovie)
        self.begin.grid(row=3, column=1, ipady = 1)
    
    def runDisplay(self, movieName) :
        '''runDisplay method, creates a new DisplayInfo object which displays the movie info and allows for trivia'''
        newDisplayWindow = DisplayInfo(self, movieName) # create new DisplayWindow object
    
    def selectMovie(self) :
        '''selectMovie method, creates new EnterMovie object to pop up an entry window for the user'''
        newSearchWindow = EnterMovie(self) # create new EnterMovie object
        
        # if the user enters a choice, try to display the data
        if newSearchWindow.choice != None :
            self.runDisplay(newSearchWindow.choice) # call the runDisplay method to show the info and play trivia
        
        
   
        
    