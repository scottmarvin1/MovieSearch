# finalGUIDriver.py
# test various parts of the GUI for the final project in CIS41B
# name : Gregory Marvin

import platform
import os
from moviesearch import MovieSearch

def main() :
    window = MovieSearch() # Instantiate a new MovieSearch Object, the main driver of the application
    # user may keep keep this one open to start new searches.

    # if user is on Mac os then make application the front most process
    if platform.system() == 'Darwin': 
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))    
    
    window.mainloop() # keep the window up until closed by the user
    
main()
