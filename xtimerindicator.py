#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    #######################################################

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    ##########################################################

    Author: James Rosado
    Copyright: Copyright 2019, xTimerIndicator
    License: GNU General Public License
    Version: 1.0.0
    Email: dev@twmsllc.com
    Status: Production

"""

import time
import sys
import getopt
import os
import signal
from time import strftime
from datetime import datetime
from threading import Thread
import logging

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject, Gio, GLib




logging.basicConfig(filename='.local/xAppInd.log',
    level=logging.INFO)


class App(Gtk.Application):
    """
        Gtk.Application Class. Overall container of application
        ***params: none
        ***attr: none 
        ***methods: do_startup, do_activate, 
                    do_command_line, on_about, on_quit
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.xtimerindicator.app",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs)
        """
            super_init__ for the Gtk.Application class
            Sets general options and flags for Gtk.Application
            ***params: 
                    (Str) application_id: Sets the unique Application ID
                    (Obj) flags : Gio.ApplicationFlags.HANDLES_COMMAND_LINE
                            This allows for cli command options to be used
        """
        #Set's window to None since there is no application window
        self.window = None

        #Add's CLI options for handling in self.do_command_line
        self.add_main_option("start", ord("S"), GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE, "Start Timer", None)
        self.add_main_option("restart", ord("R"), GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE, "Start Timer", None)
        self.add_main_option("stop", ord("P"), GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE, "Start Timer", None)
        self.add_main_option("timer1", ord("1"), GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE, "Start Timer", None)
        self.add_main_option("timer2", ord("2"), GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE, "Start Timer", None)
        self.add_main_option("timer3", ord("3"), GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE, "Start Timer", None)
        
    def do_startup(self):
        """
            Handles basic generic Gtk.App startup procedure, 
            creates 'about' action in case I decide to use that later
        """
        logging.info("App Startup")
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)
   
    def do_activate(self):
        """
            This is where the magic happens. When Application is launched from
            the desktop, the signal 'activate' is passed to the application, and
            this method is run. 
            ***attr: (obj) self.timer1, (obj) self.timer2, (obj) self.timer3
        """
        logging.info("App Activated")
        # this is where we call GObject.threads_init() : This must be called
        # we create any threads
        GObject.threads_init() 

        # Create One AppIndicator instance for each timer displayed       
        self.timer1 = Indicator(1)
        self.timer2 = Indicator(2)
        self.timer3 = Indicator(3)

        # Handle SGINT and SIG_DFL signals so the application can be stopped in
        # terminal using Ctrl+C
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Gtk.Application Main Loop. Nothing actually happens in there, it just
        # keeps the app running
        Gtk.main()
    
    def do_command_line(self, command_line):
        """
            Handles Command line arguments / options that are started by a 
            remote process. The primary application instance should already be
            running, and received the 'activate' signal. These commands are used
            to start, stop, reset timer by briefly opening a second instance, passing
            the commands, and then closing
        """
        options = command_line.get_options_dict()
        options = options.end().unpack()
        logging.info('Command Line Options Received: %s', options)

        #Handles the option --start or -S
        if "start" in options:
            if "timer1" in options:
                logging.info("Start Timer Command Received For Timer 1")
                app.timer3.toggleTimer()
            if "timer2" in options:
                logging.info("Start Timer Command Received For Timer 2")
                app.timer2.toggleTimer()
            if "timer3" in options:
                logging.info("Start Timer Command Received For Timer 3")
                app.timer1.toggleTimer()
            #return here so self.do_activate is not triggered,
            #and commands are instead passed to primary instance
            return 0
    
        #Handles the option --restart or -R
        if "restart" in options:
            if "timer1" in options:
                logging.info("Restart Timer Command Received For Timer 1")
                app.timer3.resetTimer()
            if "timer2" in options:
                logging.info("Restart Timer Command Received For Timer 2")
                app.timer2.resetTimer()
            if "timer3" in options:
                logging.info("Restart Timer Command Received For Timer 3")
                app.timer1.resetTimer()
            #return here so self.do_activate is not triggered,
            #and commands are instead passed to primary instance
            return 0
        
        #Handles the option --stop or -P
        if "stop" in options:
            if "timer1" in options:
                logging.info("Stop Timer Command Received For Timer 1")
                app.timer3.toggleTimer()
            if "timer2" in options:
                logging.info("Stop Timer Command Received For Timer 2")
                app.timer2.toggleTimer()
            if "timer3" in options:
                logging.info("Stop Timer Command Received For Timer 3")
                app.timer1.toggleTimer()
            #return here so self.do_activate is not triggered,
            #and commands are instead passed to primary instance
            return 0
        #if no handled option is selected, then this is the start of a
        # primary instance, therefore self.do_activate is triggered
        self.do_activate()

        return 0

    def on_about(self, action, param):
        """
            Creates an AboutDialog for application. 
            Not currently being used.
        """
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()
        
    def on_quit(self, action, param):
        """
            If I actually have to explain this to you, 
            just stop reading now.
        """
        self.quit()

class Indicator():
    """
        This class is used to create AppIndicator instances using the method
        AppIndicator3.Indicator.new() . Because of the way this is called, these
        instances are NOT children of the Indicator class, they are children of
        the App instance. 
        These are instantiated as app.timer1, app.timer2, and app.timer3
        ***methods: create_menu, toggleTimer, resetTimer, show_seconds, stop
    """
    def __init__(self, timerNo):
        """
            This is the initiation for AppIndicator instances
            Threads are started from within these instances
            ***attr: 
                (str) self.app - Indicator ID no
                (bool) self.isStopped - Is true if the timer is stopped
                (int) self.lastTime - The datetime last time timer was stopped 
                (obj) self.update - A Thread starts here to update timer
        """
        self.app = 'xTimerIndicator-' + str(timerNo)
        iconpath = "/home/usirius/Documents/timer_icon_white.png"
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath,
            AppIndicator3.IndicatorCategory.COMMUNICATIONS)       
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ATTENTION)
        #Assigns menu created by method create_menu to indicator instance
        self.indicator.set_menu(self.create_menu())
        #Sets initial timer label
        self.indicator.set_label("00:00", self.app)
        #Allows the middle mouse button to start/stop timer
        self.indicator.set_secondary_activate_target(self.item_1)
        logging.info('This Instance\'s ID = %s', self.app)  

        #declaring this defined as True ensures timer is stopped when app starts
        self.isStopped = True
        #Set lastTime to False since when this timer starts, 
        # it will be it's first start
        self.lastTime = False
        # Ensure timer seconds are defined
        self.seconds = ''
        # This is where the MultiThreading magic begins
        # target of thread is the method show_seconds:
        self.update = Thread(target=self.show_seconds)
        # daemonize the thread to make the indicator stoppable
        self.update.setDaemon(True)
        self.update.start()

    def create_menu(self):
        """
            Creates the menu for the AppIndicator
            AppIndicator only accepts Gtk.Menu type menus,
            no Gio.menu types allowed :(
        """
        self.menu = Gtk.Menu()
        logging.info('Current Menu being created is %s', self.menu)
        # menu item 1
        self.item_1 = Gtk.MenuItem('Start / Stop')
        self.menu.append(self.item_1)
        self.item_1.connect('activate', self.toggleTimer)

        # menu item 2
        self.item_2 = Gtk.MenuItem('Reset Timer')
        self.menu.append(self.item_2)
        self.item_2.connect('activate', self.resetTimer)

        # separator
        self.menu_sep = Gtk.SeparatorMenuItem()
        self.menu.append(self.menu_sep)

        # menu item_quit
        self.item_quit = Gtk.MenuItem('Quit')
        self.item_quit.connect('activate', self.stop)
        self.menu.append(self.item_quit)

        # allows menu to actually render
        self.menu.show_all()
        return self.menu

    def toggleTimer(self, *args):
        """
            This method is used to toggle the timer's state between
            isStopped and not isStopped. This method stored the stoppedTime 
            when this is called, but it does not directly start or stop the timer.
            This method only toggles the flag isStopped. The timer itself is handled
            resetTimer and the Thread.
        """
        logging.info('%s has been toggled.' , self)
        logging.info('isStopped = %s', self.isStopped)
        #if the timer is not already stopped when this is triggered, 
        #isStopped is set to true, the stoppedTime is recoreded, and lastTime is 
        #set to equal stoppedTime
        if not self.isStopped:
            self.isStopped = not self.isStopped
            self.stoppedTime = datetime.now()
            self.lastTime = self.stoppedTime
            logging.info('lastTime = %s' , self.lastTime)
        #if the timer is stopped when this is triggered,
        #isStopped is set to false, and a new update Thread is started in order
        # to start the timer. 
        else:
            self.isStopped = not self.isStopped
            self.update = Thread(target=self.show_seconds)
            self.update.setDaemon(True)
            self.update.start()
            
    def resetTimer(self, *args):
        #if the timer is not stopped, isStopped is set to true, the application then waits
        #for the currently running timer thread to stop, and then it sets isStopped
        #false, and then the timer is started again from 0
        if not self.isStopped:
            self.isStopped = True
            self.update.join()
            self.isStopped = False
            self.lastTime = False
            self.update = Thread(target=self.show_seconds)
            self.update.setDaemon(True)
            self.update.start()
        #if the timer stopped, then isStopped is set to False, and a new timer thread
        # is started to start timer
        else:
            self.isStopped = False
            self.lastTime = False
            self.update = Thread(target=self.show_seconds)
            self.update.setDaemon(True)
            self.update.start()

    def show_seconds(self):
        """
            This method is called whenever a new timer thread is started. This method
            never runs in the main thread, rather it is run in a seperate thread 
            in order to handle the actual timer, and the actual process of updating
            the AppIndicator label. Everytime the timer starts or stops,
            the thread is killed and a new one starts.
        """
        #only calculates starttime if the timer is actually started.
        if not self.isStopped:
            #if the timer had been run in a previous thread, lastTime will
            #be set, and the start time will be adjusted to compensate.
            if self.lastTime:
                logging.info('Previous Stop Time: %s', self.seconds.seconds)
                #new startTime is based on the current time - the self.seconds
                #variable, so that the timer essentially resumes from where it was
                startTime = datetime.now() - self.seconds
                logging.info('Start Time = %s', startTime)
                logging.info('Current Time = %s', datetime.now())
            #if the timer had not been run previously, or it had been reset
            #startTime is equal to the current time.
            else:
                startTime = datetime.now()
                logging.info('Start Time = %s', startTime)
        #The actual timer runs in a While loop, with a 1 second sleep. As long as
        # the timer's isStopped value is false, the loop will continue to run.
        # When the method toggleTimer or resetTimer is run, the loop will end, and the
        # thread will die a slow and painful death, only to be reincarnated the next
        # time the timer is started. 
        while not self.isStopped:
            currentTime = datetime.now()  
            self.seconds = currentTime - startTime
            #number of minutes calculated by floor dividing seconds by 60,
            # and the string is padded to 2 characters
            minString = str(self.seconds.seconds // 60).zfill(2)
            #the Second string is the remainder ( % 60 ) of dividing seconds by 60,
            # and then padding to 2 characters
            secString = str(self.seconds.seconds % 60).zfill(2)
            mention = minString + ":" + secString
            # Here's a fun fact. Did you know that the child threads aren't allowed to 
            # make any changes to the actual GUI? "What good is it then?" you may ask.
            # That's where the GObject.idle_add comes in. This essentially passes the
            # self.indicator.set_label method back to the main thread, and tells it to
            # process the label update as soon as it has a chance to.
            GObject.idle_add(
                self.indicator.set_label,
                mention, self.app,
                priority=GObject.PRIORITY_DEFAULT
                )
            # the 1 second sleep is taking place at the end of the while loop instead of
            # the beginning. This allows the main thread a chance to apply the update, 
            # before the next iteration of the while loop
            time.sleep(1)

    def stop(self, source):
        """
            Stop means stop. If I have to explain this to you, then you have bigger
            problems than reading my comments is capable of solving. Please seek 
            professional help.
        """
        Gtk.main_quit()

if __name__ == "__main__":
    """
    This is the main function. Oooooo!
    Such Function! Verrry modular! Much WOW!!
    """
    app = App()
    logging.debug("App Run")
    #runs the app. Duh.
    app.run(sys.argv)
