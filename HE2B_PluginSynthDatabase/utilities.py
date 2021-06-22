from presetReader.lkpReader1 import update
from presetReader.lkpReader1 import list_presets
from presetReader.lkpReader1 import load_preset
from presetReader.lkpReader1 import db_connection
from presetReader.lkpReader1 import db_close

#import presetReader.lkpReader1
import pickle
import pandas as pd
from datetime import date


def help_lkp():
    strhelp = """
             ###########################################################################

             These are the commands at your disposition:

             1) <exit> or <q> : close program

             2) <update> "<Preset files path>": Higher level function used to enter and 
             update all presets found in <Preset files path> folder on local PC to the 
             Lokomotiv database table.
             e.g. update /Users/jeannshuti/Admin/Uni/HE2B/PBE/Lokomotiv presets/dbtest

             3) <list> : Lists the names of all presets currently stored in the database
             table.
             e.g. list

             4) <load> <Preset Name> : With a music DAW open and the Lokomotiv preset 
             inserted on one of the tracks, this command will load <"Preset Name"> into
             your Lokomotiv instance through Midi CC.
             e.g. load FlamingJuly
             Or   load 1

             ############################################################################

             """
    print(strhelp)


def startup():
    # Start-up
    startup_str = """
    =============================================================================
     Welcome to Lokomotiv Synthesizer Dataset V1 which uses MySQL database server
     to store your vst presets. Three commands are at your disposition to access
     and update the Lokomotiv database table:

     1) <update> "<Preset files path>": Higher level function used to enter and 
     update all presets found in <Preset files path> folder on local PC to the 
     Lokomotiv database table.
     e.g. update /Users/jeannshuti/Admin/Uni/HE2B/PBE/Lokomotiv presets/dbtest

     2) <list> : Lists the names of all presets currently stored in the database
     table.
     e.g. list

     3) <load> <Preset Name> : With a music DAW open and the Lokomotiv preset 
     inserted on one of the tracks, this command will load <"Preset Name"> into
     your Lokomotiv instance through Midi CC.
     e.g. load FlamingJuly
     Or   load 1

     4) <help> : lists the available commands

     5) <exit> or <q> : close program

     ============================================================================="""

    print(startup_str)


def print_invalid_command():
    print("Command does not exist, type <help> command for more information")


def switch(argument):
    try:
        if argument[0].lower() == "update":
            if len(argument) > 1:
                update("lokomotiv_presets", argument[1])
            else:
                print("Folder path (to .lkp files) was not provided. Please execute <help> "
                      "to see how to use the update command")
        elif argument[0].lower() == "help":
            help_lkp()
        elif argument[0].lower() == "list":
            list_presets("lokomotiv_presets")
        elif argument[0].lower() == "load":
            if len(argument) > 1:
                load_preset(argument[1])
            else:
                print("Missing Argument: An index value or preset name is missing from you command. Please execute"
                      " <help> to see how to use the load command")
        elif argument[0].lower() == "pickle":
            back_up()
        elif argument[0].lower() == "unpickle":
            if len(argument) > 1:
                get_backup(argument[1])
            else:
                print("Missing Argument: Please supply a name for the file you want to unpickle")
        else:
            print_invalid_command()
    except IndexError as e:
        print(e)
    except RuntimeError as e:
        print(e)
    except FileNotFoundError as e:
        print("Missing argument: File specified was not found", e)


# Bonus function to "save" dataset in easy to transport file .pickle
def back_up():
    today = date.today()
    timestamp = today.strftime("%b-%d-%Y")
    # Open db connection
    db = db_connection()
    # Create cursor
    dbcursor = db.cursor()
    # Get data with pandas
    my_data = pd.read_sql("SELECT * FROM synth_plugin_presets.lokomotiv_presets", db)
    fob = open('/Users/jeannshuti/Admin/Uni/HE2B/PBE/Lokomotiv presets/dbBackUp/%s' % timestamp, 'wb')
    pickle.dump(my_data, fob)  # generated the Pickle
    fob.close()
    # Close connection
    db_close(db, dbcursor)
    print("database has been backed up for " + timestamp)


def get_backup(timestamp):
    fob = open('/Users/jeannshuti/Admin/Uni/HE2B/PBE/Lokomotiv presets/dbBackUp/%s' % timestamp, 'rb')
    my_data = pickle.load(fob)  # reading the Pickle
    fob.close()
    print(my_data)
