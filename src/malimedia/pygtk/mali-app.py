#!/usr/bin/env python

# example table.py
import pygtk
pygtk.require('2.0')
import gtk
import subprocess

class Table:
    # Our callback.
    # The data passed to this method is printed to stdout
    def callback(self, widget, cmd=None):
        print "%s" % cmd[1]
        if cmd[0] == 1:
            cmd = '/home/<user>/scrapy/runscraper.sh'
            subprocess.call(cmd, shell=True)
        elif cmd[0] == 2:
            cmd = 'python /home/<user>/MaliMedia/Automation/Python/lib/python/run.py'
            subprocess.call(cmd, shell=True)

    # This callback quits the program
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # Set the window title
        self.window.set_title("Mali Media app")

        # Set a handler for delete_event that immediately
        # exits GTK.
        self.window.connect("delete_event", self.delete_event)

        # Sets the border width of the window.
        self.window.set_border_width(20)

        # Create a 2x2 table
        table = gtk.Table(2, 2, True)

        # Put the table in the main window
        self.window.add(table)

        # Create first button
        button = gtk.Button("Start scraping")

        # When the button is clicked, we call the "callback" method
        # with a pointer to "button 1" as its argument
        button.connect("clicked", self.callback, (1, "Starting scraping..."))

        # Insert button 1 into the upper left quadrant of the table
        table.attach(button, 0, 1, 0, 1)

        button.show()

        # Create second button

        button = gtk.Button("Run run.py")

        # When the button is clicked, we call the "callback" method
        # with a pointer to "button 2" as its argument
        button.connect("clicked", self.callback, (2, "Running run.py..."))

        # Insert button 2 into the upper right quadrant of the table
        table.attach(button, 1, 2, 0, 1)

        button.show()

        # Create "Quit" button
        button = gtk.Button("Quit")

        # When the button is clicked, we call the main_quit function
        # and the program exits
        button.connect("clicked", lambda w: gtk.main_quit())

        # Insert the quit button into the both lower quadrants of the table
        table.attach(button, 0, 2, 1, 2)

        button.show()

        table.show()
        self.window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    Table()
    main()
