Movie Search.
*Requires omdb module for MovieData class*
'pip install omdb' installs the necessary module

Run finalGUIDriver.py to start the application

Movie Search utilizes the OMDB(Open Movie Database) API that accesses data from the
movie rating website imdb.com. In addition some web scraping features were added to
collect more information about a given movie

There is an interactive GUI component that allows communication with the API.
The GUI consists of the following:
	A MovieSearch class that pops up the starting window with a click to begin
	button. This is the main starting point for the application. As long as this
	window remains open, the user can click to start a new search.

	An EnterMovie class that pops up a window that allows the user to enter a movie
	of their choice. The API finds the closest match if possible, and is not case 
	sensitive. There is an ok and cancel button that either commits the movie, or
	closes the window.

	A DisplayInfo class that pops up another window, which contains the majority of
	the information available. There is a set of radio buttons at the top of the 
	window that manages what the listbox below will contain. There is a movie info
	option that displays technical facts about the movie. There is a facts option that
	fills the listbox with interesting facts, goofs in the movie, and things to watch 
	out for in the closing credits. The last option is quotes. This option fills the
	listbox with quotes from the movie. At the bottom of the screen there are two
	buttons, one to click to see the movies poster and one to play trivia. The movie 
	poster pops up in a window to the right of the display info window and is not 
	obstructing so it may be left open until closed by the user.

	A PlayTrivia class that pops up another window with 5 trivia questions based on
	information contained in movie technical info. While the questions may be more 
	generic, they allow for greater flexibility in the number of movies it works for.
	There is an ok and cancel button to commit the questions or cancel and close. 
	there is a pop up info window that shows the number of correct, and either a 
	well done, a not bad, or better luck next time is shown based on the score.


	A MovieData class that gathers all data for given movie. With given parameters, it can provide full plot or summary and load all trivial information about the movie. With default parameters, trivial information is pulled separately through class methods. When load_all parameter is True, trivial information is loaded on creation of object. For each set of trivial information, the imdb page of each movie is scraped.


There is currently limited functionality for TV shows, since the information collected
is tailored more towards movies. Also the quiz will currently mark you incorrect if a 
actor/actress or director's name is McSomething. The quiz compares the name in movie technical info to the .title() version of the provided answer. While this limits the functionality in one sense, allows for more free user input and covers more far more cases
than it hinders.

	 

	


