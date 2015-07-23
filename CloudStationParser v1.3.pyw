"""
This CloudStation parsing application is designed to walk across the
CloudStation directory structure and extract the relevant information.
This is the primary script which configures the GUI before calling the
relevant scripts contained within the 'utilities_directory'.  This
script is given feedback from the other scripts which is displayed
within the GUI.
"""

import time
import tkinter
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Label
from tkinter import filedialog

from utilities_directory.cloudstation_parser_logging import *
from utilities_directory.parse_sys_database import parse_sys_sqlite_file
from utilities_directory.parse_filter_database import parse_filter_sqlite_file
from utilities_directory.parse_event_database import parse_event_db_file
from utilities_directory.parse_history_database import parse_history_sqlite_file


class Application:
    """
    This application constructs the GUI and uses threading to allow the
    GUI to be run independent of the processing thread.  It also calls
    5 other scrips contained within the utilities_directory.
    """
    def process_all_database_files(self, root, normalized_source_file,
                                   normalized_output_directory, case_reference_number,
                                   investigators_name, investigators_notes, exhibit_reference):

        tk.Label(self.root, text='Sys.sqlite processed.', fg='black').place(x=325, y=350)
        tk.Label(self.root, text='Filter.sqlite processed.', fg='black').place(x=325, y=370)
        tk.Label(self.root, text='History.sqlite processed.', fg='black').place(x=325, y=390)
        tk.Label(self.root, text='Event-db.sqlite processed.', fg='black').place(x=325, y=410)

        # Script 1 - parse the sys.sqlite database.
        process_sys_sqlite_database = parse_sys_sqlite_file(normalized_source_file,
                                                            normalized_output_directory,
                                                            case_reference_number,
                                                            investigators_name, investigators_notes,
                                                            exhibit_reference)
        time.sleep(0.25)

        if process_sys_sqlite_database:
            tk.Label(self.root, text='ü', fg='green', font="Wingdings").place(x=475, y=350)
            add_information_message_to_log('Sys.sqlite identified and read.')
        else:
            tk.Label(self.root, text='X', fg='red').place(x=475, y=350)
            add_warning_message_to_log('Sys.sqlite database not identified.')

        # Script 2 - parse the filter.sqlite database.
        process_filter_sqlite_database = parse_filter_sqlite_file(
            normalized_source_file, normalized_output_directory, case_reference_number,
            investigators_name, investigators_notes, exhibit_reference)

        time.sleep(0.25)

        if process_filter_sqlite_database:
            tk.Label(self.root, text='ü', fg='green', font="Wingdings").place(x=475, y=370)
            add_information_message_to_log('Filter.sqlite database identified and read.')
        else:
            tk.Label(self.root, text='X', fg='red').place(x=475, y=370)
            add_warning_message_to_log('Filter.sqlite database not identified')

        # Script 3 - parse the history.sqlite database.
        process_history_sqlite_database = parse_history_sqlite_file(
            normalized_source_file, normalized_output_directory, case_reference_number,
            investigators_name, investigators_notes, exhibit_reference)

        time.sleep(0.25)

        if process_history_sqlite_database:
            tk.Label(self.root, text='ü', fg='green', font="Wingdings").place(x=475, y=390)
            add_information_message_to_log('History.database identified and read.')
        else:
            add_warning_message_to_log('History.sqlite database not identified.')
            tk.Label(self.root, text='X', fg='red').place(x=475, y=390)

        # Script 4 - parse the event-db.sqlite database.
        process_event_sqlite_database = parse_event_db_file(
            normalized_source_file, normalized_output_directory, case_reference_number,
            investigators_name, investigators_notes, exhibit_reference)

        time.sleep(0.25)

        if process_event_sqlite_database:
            tk.Label(self.root, text='ü', fg='green', font="Wingdings").place(x=475, y=410)
            add_information_message_to_log('Event.sqlite database identified and read.')
        else:
            add_warning_message_to_log('Event-db.sqlite database not identified.')
            tk.Label(self.root, text='X', fg='red').place(x=475, y=410)

        time.sleep(0.25)

        messagebox.showinfo(message='Processing complete, please review your output directory.')

    def __init__(self, root):
        """Setup the main structure of the GUI within the Application.
        """
        self.root = root
        self.root.title('CloudStation Information Extractor - v.1.3')
        # main frame to hold all the widgets.
        main_frame = ttk.Frame(self.root, width=850, height=450).pack()
        # frame to cover user defined information.
        ttk.Labelframe(main_frame, borderwidth=5, relief='groove', text='Case Information',
                       width=565, height=100).place(x=10, y=60)

        ttk.Labelframe(main_frame, borderwidth=5, relief='groove', text='File Information',
                       width=810, height=106).place(x=10, y=165)

        ttk.Labelframe(main_frame, borderwidth=5, relief='groove', text='Other Information',
                       width=180, height=80).place(x=660, y=60)

        self.init_widgets()
        add_information_message_to_log('--- Start of new log entry ---')
        add_information_message_to_log('Script framework has initiated.')

        tk.LabelFrame(main_frame, borderwidth=0.5, relief='flat', background='white', width=850,
                      height=43).place(x=0, y=0)
        tk.Label(self.root, text='CloudStation Parser v.1.3', fg='black', bg='white',
                 font="TkDefaultFont 16").place(x=20, y=5)

        tk.Label(self.root, text='View Help Manual', fg='black').place(x=680, y=80)

        tk.Label(self.root, text='View Log File', fg='black').place(x=680, y=110)

        # Displays the python image in the GUI.
        photo = tkinter.PhotoImage(file='resources\\python_logo.gif')
        label = Label(image=photo, bg='white')
        label.image = photo
        label.place(x=690, y=0)
        self.init_widgets()

    def init_widgets(self):
        """ This function constructs the buttons, labels and main
        interface of the GUI and places them in the appropriate
        locations.
        """
        ttk.Button(self.root, command=self.select_source_folder_structure,
                   text='CloudStation Directory',
                   style='Blue.TButton', width='20').place(x=14, y=190)
        ttk.Button(self.root, command=self.select_destination_directory,
                   text='Output Directory',
                   style='Blue.TButton', width='20').place(x=14, y=230)
        ttk.Button(self.root, command=self.execute_main_processing_script,
                   text='Begin Extraction', width='18').place(x=330, y=285)
        ttk.Button(self.root, command=self.cancel_all_processing, text='Close',
                   style='Blue.TButton', width='12').place(x=470, y=285)

        ttk.Button(self.root, command=self.open_help_manual, text='---',
                   style='Blue.TButton', width='3').place(x=800, y=77)

        ttk.Button(self.root, command=self.open_log_file, text='---', style='Blue.TButton',
                   width='3').place(x=800, y=107)

        # These parameters set the Case Information.
        ttk.Label(self.root, text='Case Reference').place(x=15, y=80)
        ttk.Label(self.root, text='Exhibit Reference').place(x=350, y=80)
        ttk.Label(self.root, text='Investigator').place(x=15, y=105)
        ttk.Label(self.root, text='Notes').place(x=15, y=130)

        # These parameters are used to facilitate source and destination
        # directories.
        self.name_source_file = tkinter.Text(self.root, width='80', height='2')
        self.name_source_file.place(x=165, y=185)
        self.destination_directory_name = tkinter.Text(self.root, width='80', height='2')
        self.destination_directory_name.place(x=165, y=225)

        # These parameters allow the user to enter the case information.
        self.user_input_case_reference = tkinter.Text(self.root, width='20', height='1')
        self.user_input_case_reference.place(x=160, y=80)
        self.user_input_exhibit_ref = tkinter.Text(self.root, width='14', height='1')
        self.user_input_exhibit_ref.place(x=447, y=80)
        self.user_input_investigator_name = tkinter.Text(self.root, width='50', height='1')
        self.user_input_investigator_name.place(x=160, y=105)
        self.user_input_investigators_notes = tkinter.Text(self.root, width='50', height='1')
        self.user_input_investigators_notes.place(x=160, y=130)

    @staticmethod
    def open_help_manual():
        os.startfile('Resources\\Help Manual.html')
        add_information_message_to_log('Help file opened.')

    @staticmethod
    def open_log_file():
        """ Opens the log file.
        """
        os.startfile('Resources\\CloudStation Parser Log.txt')
        add_information_message_to_log('Log File Opened.')

    def select_source_folder_structure(self):
        """ Instructs user to select the source CloudStation directory
        structure.
        """
        source = filedialog.askdirectory()
        self.name_source_file.insert(tkinter.INSERT, source)
        add_information_message_to_log('Source directory chosen as {}.'.format(source))

    def select_destination_directory(self):
        """ Instructs user to select the output directory where the
        script will export the files.
        """
        destination = filedialog.askdirectory()
        self.destination_directory_name.insert(tkinter.INSERT, destination)
        add_information_message_to_log('Destination directory chosen as {}.'.format(destination))

    @staticmethod
    def cancel_all_processing():
        """ Cancels the process and closes the GUI.
        """
        root.destroy()
        add_information_message_to_log('Application Closed.')

    def execute_main_processing_script(self):
        """ Obtains the information supplied by the user.
        """
        case_reference_number = self.user_input_case_reference.get(1.0, 2.0)
        investigators_name = self.user_input_investigator_name.get(1.0, 2.0)
        investigators_notes = self.user_input_investigators_notes.get(1.0, 2.0)
        exhibit_reference = self.user_input_exhibit_ref.get(1.0, 2.0)
        raw_source_file_name_1 = self.name_source_file.get(1.0, 2.0)
        raw_destination_file_info = self.destination_directory_name.get(1.0, 2.0)

        # Normalizes the paths to remove unnecessary information.
        normalized_source_file_1 = os.path.normpath(raw_source_file_name_1.rstrip())
        normalized_output_directory = os.path.normpath(raw_destination_file_info.rstrip())

        # Executes the primary thread separate from the GUI thread.
        # Resilience has been added to account for user error and
        # where the directories are inaccessible.
        if len(normalized_source_file_1) > 1:
            if os.path.exists(normalized_source_file_1):
                if len(normalized_output_directory) > 1:
                    if os.path.isdir(normalized_output_directory):
                        run_primary_thread = threading.Thread(
                            target=self.process_all_database_files,
                            args=(root, normalized_source_file_1, normalized_output_directory,
                                  case_reference_number, investigators_name, investigators_notes,
                                  exhibit_reference))
                        run_primary_thread.start()
                    else:
                        messagebox.showwarning('Warning', 'The destination directory does not exist'
                                                          '.')
                else:
                    messagebox.showwarning('Warning', 'You have not selected a valid destination di'
                                                      'rectory.')
            else:
                messagebox.showwarning('Warning', 'The source directory does not exist blah.')
        else:
            messagebox.showwarning('Warning', 'You have not selected a valid Source Directory.')

root = tkinter.Tk()
Application(root)
root.mainloop()