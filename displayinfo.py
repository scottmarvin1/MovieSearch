##
# displayinfo.py
# DisplayInfo class. Pop up window with radio buttons to select an option
# name: Gregory Marvin
##

import tkinter as tk
import tkinter.messagebox as tkmb
from PIL import ImageTk, Image
import requests
import textwrap
from movieData import MovieData
from playtrivia import PlayTrivia

class DisplayInfo(tk.Toplevel) :
    def __init__(self, master, movieName, title="Displaying Info") :
        
        tk.Toplevel.__init__(self, master) # override the Toplevel window constructor
        
        # DisplayInfo takes the focus from its master
        self.grab_set() 
        
        self.resizable(True, True) # allow the window to be resizable
    
        # if window is closed call the cancel method to clean up
        self.protocol("WM_DELETE_WINDOW", self.cancel)
    
        # set master so it can be accessed by methods of DisplayInfo
        self._master = master
        
        # set the title with the provided value
        self.title(title)
        
        # create label to indicate that the user should select an option
        self.optionLabel = tk.Label(self, text="Select an option:").grid(row=0, column=0, columnspan=2, sticky='nsw')
        
        # create control variable for the radiobuttons
        self.controlVar = tk.StringVar()
        # create a radiobutton for showing movie info in listbox
        self.rbMovieInfo = tk.Radiobutton(self, 
                                          text="Movie Info", 
                                          variable=self.controlVar, 
                                          value='info', 
                                          command=self.updateListBox).grid(row=1, column=0, sticky='nsew')
        # create a radiobutton for showing movie facts in listbox
        self.rbRandomFacts = tk.Radiobutton(self, 
                                            text="Interesting Facts", 
                                            variable=self.controlVar, 
                                            value='facts', 
                                            command=self.updateListBox).grid(row=1, column=1, sticky='nsew')
        # create a radiobutton for showing movie quotes in listbox
        self.rbReviews = tk.Radiobutton(self, 
                                        text="Quotes", 
                                        variable=self.controlVar, 
                                        value='quotes', 
                                        command=self.updateListBox).grid(row=1, column=2, sticky='nsew')
        
        # create label to show name of movie entered by the user
        self.movie = tk.StringVar()
        self.movie.set(movieName)
        self.movieLabel = tk.Label(self, textvariable=self.movie).grid(row=5, columnspan=2, sticky='nsw')
        
        # create a vertical and horizontal scrollbar to scroll through if beyond the boundary of the ListBox widget
        self.yscroll = tk.Scrollbar(self, orient=tk.VERTICAL)
    
        # create ListBox to store the results of the search
        self.contentContainer = tk.Listbox(self, 
                                        height=10, 
                                        width=60, 
                                        yscrollcommand=self.yscroll.set)
        self.contentContainer.grid(row=6, columnspan=3, sticky='nsew') # position across the whole window on row 6 
        
        # connect the scrollbar to the ListBox
        self.yscroll.config(command=self.contentContainer.yview)
        self.yscroll.grid(row=6, column=4, sticky='nsew')
        
        # create labels and buttons to start a game of trivia
        self.trivia = tk.StringVar()
        self.trivia.set("Would you like to play some trivia?")
        self.triviaLabel = tk.Label(self, textvariable=self.trivia).grid(row=7, column=0, columnspan=2, sticky='nsew')
        self.playTrivia = tk.Button(self, text="play", command=self.playTrivia).grid(row=7, column=2, sticky='nsew')
        
        # create labels and buttons to view the selected movies poster
        self.poster = tk.StringVar()
        self.poster.set("Click to see the movie's poster")
        self.poterLabel = tk.Label(self, textvariable=self.poster).grid(row=8, column=0, columnspan=2, sticky='nsew')
        self.seePoster = tk.Button(self, text="click!", command=self.viewPoster)
        self.seePoster.grid(row=8, column=2, sticky='nsew')
        
        # set up so window and widgets are resizable(listbox stays the same height)
        self.grid_columnconfigure(0 , weight=1)
        self.grid_columnconfigure(1 , weight=1)
        self.grid_columnconfigure(2 , weight=1)
        self.grid_rowconfigure(0 , weight=1)
        self.grid_rowconfigure(1 , weight=1)
        self.grid_rowconfigure(2 , weight=1)
        self.grid_rowconfigure(3 , weight=1)
        self.grid_rowconfigure(4 , weight=1)
        self.grid_rowconfigure(5 , weight=1)
        self.grid_rowconfigure(6 , weight=1)
        self.grid_rowconfigure(7 , weight=1)
        self.grid_rowconfigure(8 , weight=1)
        
        # set up so window appears down and right from the movie search window
        self.geometry("+%d+%d" % (master.winfo_rootx()+50, master.winfo_rooty()+50))
        
        # fetch the data in a thread so the DisplayInfo window pops up immediately
        self.id = self.after(100, self.fetchData, movieName)
        
    def fetchData(self, movieName) :
        '''fetchData method, creates new MovieData object for web scraping and accessing API'''
        try :
            self.chosenMovie = MovieData(movieName, load_all_data=True) # gets data for provided movie
            self.getInfo() # get movie info
            self.getFacts() # get movie facts
            self.getQuotes() # get quotes from the movie
            
        except KeyError :
            print("Error, no movie with that name")
            tkmb.showerror("Uh-oh!", "Could not find anything by that name...\nClick ok and then press click to begin.")
            self.cancel()
            
    
    def viewPoster(self) :
        '''viewPoster method, creates pop up window with the movie poster'''
        def close() :
            '''local close method, eliminates the possibility an empty window is left after the 'x' is clicked'''
            self.popUpPoster.destroy()
            
        # create a Toplevel window so existance is independent of DisplayInfo window
        self.popUpPoster = tk.Toplevel()
        self.popUpPoster.resizable(False, False)
        self.popUpPoster.title("Movie Poster") # set title
        # cause window to pop up beyond DisplayInfo window so it is not obstructing
        self.popUpPoster.geometry("+%d+%d" % (self._master.winfo_rootx()+700, self._master.winfo_rooty()))
        self.popUpPoster.protocol("WM_DELETE_WINDOW", close) # if the window is closed, clean up and close
        try :
            # try to fetch the byte stream of the .jpg image at the url provided
            self.getImage = requests.get(self.chosenMovie.movie_technical_info['poster'], stream=True)
            # raise any exceptions
            self.getImage.raise_for_status() 
            # create tk PhotoImage object that tkinter can use
            self.poster = ImageTk.PhotoImage(data = self.getImage.content)
            # create a label to store the picture
            self.imageWindow = tk.Label(self.popUpPoster, image=self.poster)
            self.imageWindow.grid() # puts the picture to the window
            
        # handle common exceptions that may arise
        except requests.exceptions.HTTPError as e :
            print('HTTP Error:', e)
        except requests.exceptions.ConnectionError as e :
            print('Connection Error:', e)
        except requests.exceptions.Timeout as e :
            print('Timeout Error:', e)
        except requests.exceptions.RequestException as e :
            print('Request Exception:', e)
            tkmb.showerror("Hmm...", "It doesn't look like an image could be found.")
            self.popUpPoster.destroy()

    def playTrivia(self) :
        '''playTrivia method, creates a new instance of the PlayTrivia class to manage a round of trivia'''
        if len(self.infoList) > 40 and \
           (self.chosenMovie.movie_technical_info['director'] != "N/A" or \
            self.chosenMovie.movie_technical_info['runtime'] != "N/A" or \
            self.chosenMovie.movie_technical_info['rated'] != "N/A" or \
            self.chosenMovie.movie_technical_info['imdb_rating'] != "N/A") :
            # start new game of trivia
            self.newGame = PlayTrivia(self, self.chosenMovie) 
        
        else :
            tkmb.showerror("Sorry...", "Not enough information to play trivia.")
    
    def getInfo(self) :
        '''getInfo method, gets the info generated by the MovieData class'''
        # header and value with prefixed tab on the following line to aid in readability
        # for each value in getInfo. Hard coded headers to make them more meaningful than
        # the dictionary keys, otherwise possible loop to cut down lines of code.
        try :
            self.infoList = ['Title:']
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['title'])
            
            self.infoList.append('Type:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['type'])
            
            self.infoList.append('Plot:')
            # textwrap object used to wrap plot within default listbox boundary for improved readability
            wrap = textwrap.TextWrapper(width=75)
            plot = wrap.wrap(text=self.chosenMovie.movie_technical_info['plot'])
            for row in plot :
                self.infoList.append('\t' + row)
            
            self.infoList.append('Main Actors:')
            # split comma separated list and put each value on new line to improve readability
            self.actorsList = self.chosenMovie.movie_technical_info['actors'].split(', ')
            for actor in self.actorsList :
                self.infoList.append('\t' + actor)
                
            self.infoList.append('Directed by:')
            # split comma separated list and put each value on new line to improve readability
            self.directorsList = self.chosenMovie.movie_technical_info['director'].split(', ')
            for director in self.directorsList :
                self.infoList.append('\t' + director)
            #self.infoList.append('\t' + self.chosenMovie.movie_technical_info['director'])
            
            self.infoList.append('Written by:')
            # split comma separated list and put each value on new line to improve readability
            self.writersList = self.chosenMovie.movie_technical_info['writer'].split(', ')
            for writer in self.writersList :
                self.infoList.append('\t' + writer)
                
            self.infoList.append('Production company:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['production'])
                
            self.infoList.append('Runtime:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['title'] + ' is ' + self.chosenMovie.movie_technical_info['runtime'] + ' long')
            
            self.infoList.append('Film release date:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['released'])
            
            self.infoList.append('DVD release date:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['dvd'])
            
            self.infoList.append('Country of origin:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['country'])
            
            self.infoList.append('Languages available:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['language'])
            
            self.infoList.append('Genre:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['genre'])
            
            self.infoList.append('MPAA Rating:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['rated'])
            
            self.infoList.append('Box Office earnings:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['box_office'])
            
            self.infoList.append('Awards:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['awards'])
            
            self.infoList.append('metacritic.com Metascore:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['metascore'])
            
            self.infoList.append('IMDB Rating:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['imdb_rating'])
            
            self.infoList.append('Number of IMDB votes:')
            self.infoList.append('\t' + self.chosenMovie.movie_technical_info['imdb_votes'])
            
        except AttributeError :
            print("Error, one or more values could not be found")
        except KeyError :
            print("Error, one or more values could not be found")
        
    def getFacts(self) :
        '''getFacts method, gets the facts generated by the MovieData class'''
        self.factList = [] # create empty list to concatenate fetched lists
        # create textwrap object to fit facts in the listbox for improved readability
        wrapper = textwrap.TextWrapper(width=75)
        
        try :
            # get trivia entries wrapped to fit in the listbox
            triviaList = [trivia for entry in self.chosenMovie.trivia for trivia in wrapper.wrap(text=entry)]
            self.factList += triviaList # concatenate to factlist
            
            # get goofs wrapped to fit in the listbox
            goofList = [goof for entry in self.chosenMovie.goofs for goof in wrapper.wrap(text=entry)]
            self.factList += goofList # concatenate to factlist
            
            # get credits wrapped to fit in the listbox
            creditList = [credit for entry in self.chosenMovie.crazycredits for credit in wrapper.wrap(text=entry)]
            self.factList += creditList # concatenate to factlist
            
        except AttributeError :
            self.factList.append("Error, no facts could be found...")
            
    def getQuotes(self) :
        '''getQuotes method, gets the quotes generated by the MovieData class'''
        #self.quoteList = []
        # create textwrap object to fit quotes in the listbox for improved readability
        wrapper = textwrap.TextWrapper(width=75) 
        try :
            # fill the quoteList with quotes from the movie that are wrapped to fit in the listbox
            self.quoteList = [quote for entry in self.chosenMovie.quotes for quote in wrapper.wrap(text=entry)]
        except AttributeError :
            self.quoteList = ["Error, no quotes found..."]
    
    def updateListBox(self) :      
        '''updateListBox method, fills the listbox based off the radio button selected at the top of window'''
        if self.controlVar.get() == 'info' :
            # if the ListBox is not empty, clear it out to display the results of the new search
            if self.contentContainer.size() != 0 :
                self.contentContainer.delete(0, self.contentContainer.size()) # starts at first item, and goes to the last one(inclusive)            
            # fill the listbox with movie information
            for item in self.infoList :
                self.contentContainer.insert(tk.END, item)
            
        elif self.controlVar.get() == 'facts' :
            # if the ListBox is not empty, clear it out to display the results of the new search
            if self.contentContainer.size() != 0 :
                self.contentContainer.delete(0, self.contentContainer.size()) # starts at first item, and goes to the last one(inclusive)            
            # fill the listbox with movie facts
            for fact in self.factList :
                self.contentContainer.insert(tk.END, fact)
        
        elif self.controlVar.get() == 'quotes' :
            # if the ListBox is not empty, clear it out to display the results of the new search
            if self.contentContainer.size() != 0 :
                self.contentContainer.delete(0, self.contentContainer.size()) # starts at first item, and goes to the last one(inclusive) 
            # fill the listbox with the movie's quotes    
            for quote in self.quoteList :
                self.contentContainer.insert(tk.END, quote)
    
    def cancel(self, *args):
        '''[Cancel] button to close window'''
        # check if any of the threads are still running
        if self.id is not None :        
            self.after_cancel(self.id)  # if there is an after thread, cancel it    
        
        self._master.focus_set()        # set focus back to the master window
        self.destroy()                  # close window           
        
        
