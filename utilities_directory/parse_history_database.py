"""
This script examines the history.sqlite database and places the results
into an HTML report.
"""

import sqlite3
from utilities_directory.cloudstation_parser_logging import *
tab = '\t'
new_line = '\n'
backslash_marker = '\\'
html_path_reference = 'file:\\\\localhost\\'
location_of_main_gui_script = os.getcwd()

full_list_of_files = []         # List of files including full path.
list_of_live_sessions = []      # Identifies the sessions (in a list).


def parse_history_sqlite_file(source_file_path, destination_folder_path, case_reference_number,
                              investigators_name, investigators_notes, exhibit_reference):
    """
    This script takes the parameters entered into the GUI to find the
    history.SQLite database.
    """
    add_information_message_to_log('History DB script executed at script level.')
    content_of_source_directory = os.walk(source_file_path)
    for paths, dirs, files in content_of_source_directory:
        for each_file in files:
            full_path = os.path.join(paths, each_file)
            full_list_of_files.append(full_path)

        html_report = open(destination_folder_path.strip() + '//History Table.html', 'w+',
                           encoding='UTF-8')

        html_report.write('<html><head><title>CloudStation Parser 1.3</title></head><body><br><br><'
                          'center><br><br><hr width="90%"><h2>CloudStation Parser (History Database'
                          ')</h2></center><br /><div i_d="navigation"><left><b><font size="5">Case '
                          'Information</font></b></left><br /><left><font size="4">Case Reference -'
                          ' {}</font></left><br /><left><font size="4">Exhibit Reference - {}</font'
                          '></left><br /><left><font size="4">Investigator - {}</font></left><br />'
                          '<left><font size="4">Case Notes - {}</font></left><br /><ul><br /><br />'
                          '</ul>'
                          .format(case_reference_number, exhibit_reference, investigators_name,
                                  investigators_notes))

        html_report.write('<p style="font-family:aerial;font-stize:10px;"><h3>Last 50 files recorde'
                          'd within the History database.</h3></></p>')

    for each in full_list_of_files:
        if os.path.basename(each) == 'history.sqlite':
            filepath = os.path.realpath(each)

            html_report.write('<style type="text/css">.tg  {border-collapse:collapse;border-spacing'
                              ':0;}.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px'
                              ' 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:'
                              'normal;}.tg th{font-family:Arial, sans-serif;font-size:14px;font-wei'
                              'ght:normal;padding:10px 5px;border-style:solid;border-width:1px;over'
                              'flow:hidden;word-break:normal;}.tg .tg-g8rd{background-color:#7a8dec'
                              ';color:#333333;text-align:center}.tg .tg-ztj8{background-color:#b3bb'
                              'e7;text-align:center}.tg .tg-bsv2{background-color:#efefef}</style><'
                              'table class="tg"><tr><td class="tg-ztj8">ID<br></td><td class="tg-zt'
                              'j8">Connection ID<br></td><td class="tg-ztj8"><b>Session ID</b><br><'
                              '/td><td class="tg-ztj8">Action<br></td><td class="tg-ztj8">Name<br><'
                              '/td><td class="tg-ztj8">Path<br></td></tr>')

            connection_to_sqlite_db = sqlite3.connect(filepath)
            cursor_connection_to_sqlite_db = connection_to_sqlite_db.cursor()
            try:
                filter_table_entries = cursor_connection_to_sqlite_db.execute("""SELECT
                id, conn_id, session_id, action, name, path FROM history_table ORDER BY id""")
                add_information_message_to_log('Connection to history.sqlite database successful.')

                content_history_db = []
                for each_entry in filter_table_entries:
                    content_history_db.append(each_entry)
                    i_d = each_entry[0]
                    conn_id = each_entry[1]
                    session_id = each_entry[2]
                    action = each_entry[3]
                    name = each_entry[4]
                    path = each_entry[5]
                    html_report.write('<td><center>{}</center></td><td><center>{}</center></td><td>'
                                      '<center><b>{}</b></center></td><td><center>{}</center></td><'
                                      'td>{}</td><td>{'
                                      '}</td></tr>\n'.format(i_d, conn_id, session_id, action, name,
                                                             path))
                return content_history_db
            except IOError:
                add_critical_message_to_log('Unable to connect to the history.sqlite database..')