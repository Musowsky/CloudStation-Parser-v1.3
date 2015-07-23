"""
This script reads two tables within the sys.sqlite database then joins
them together before putting them into an HTML report.
"""

import sqlite3
from tkinter import messagebox
tab = '\t'
new_line = '\n'
backslash_marker = '\\'
html_path_reference = 'file:\\\\localhost\\'
from utilities_directory.cloudstation_parser_logging import *

full_list_of_files = []     # Lists files including its full path.
list_of_live_sessions = []  # Identifies the sessions (in a list).


def parse_sys_sqlite_file(source_file_path, destination_folder_path, case_reference_number,
                          investigators_name, investigators_notes, exhibit_reference):
    add_information_message_to_log('Sys DB script executed at script level.')

    html_report = open(destination_folder_path.strip() + '//CloudStation Report.html', 'w+',
                       encoding='UTF-8')
    html_report.write('<html><head><title>CloudStation Parser 1.3</title></head><body><br><br><cent'
                      'er><br><br><hr width="90%"><h2>CloudStation Parser (Sys Database)</h2></cent'
                      'er><br /><div i_d="navigation"><left><b><font size="5">Case Information</fon'
                      't></b></left><br /><left><font size="4">Case Reference - {}</font></left><br'
                      ' /><left><font size="4">Exhibit Reference - {}</font></left><br /><left><fon'
                      't size="4">Investigator - {}</font></left><br /><left><font size="4">Case No'
                      'tes -{}</font></left><br /><ul><br /><br /></ul>'
                      .format(case_reference_number, exhibit_reference, investigators_name,
                              investigators_notes))

    html_report.write('<p style="font-family:aerial;font-stize:10px;"><h3>Device & user information'
                      ' relating to each session.</h3></></p>')

    html_report.write('<style type="text/css">.tg  {border-collapse:collapse;border-spacing:0;}.tg '
                      'td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-styl'
                      'e:solid;border-width:1px;overflow:hidden;word-break:normal;}.tg th{font-fami'
                      'ly:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;bord'
                      'er-style:solid;border-width:1px;overflow:hidden;word-break:normal;}.tg .tg-g'
                      '8rd{background-color:#7a8dec;color:#333333;text-align:center}.tg .tg-ztj8{ba'
                      'ckground-color:#b3bbe7;text-align:center}.tg .tg-bsv2{background-color:#efef'
                      'ef}</style><table class="tg"><td class="tg-ztj8">Connection ID<br></td><td c'
                      'lass="tg-ztj8">Server Name<br></td><td class="tg-ztj8">IP Address<br></td><t'
                      'd class="tg-ztj8">Server Port<br></td><td class="tg-ztj8">Quickconn Mode<br>'
                      '</td><td class="tg-ztj8">Username<br></td><td class="tg-ztj8">DiskStation ID'
                      ' (DS_ID)<br></td><td class="tg-ztj8"><b>Session ID</b><br></td><td class="tg'
                      '-ztj8">DiskStation Directory<br></td><td class="tg-ztj8">Synchronization Tim'
                      'e (UTC)<br></td><td class="tg-ztj8">Local Directory<br></td><td class="tg-zt'
                      'j8">Sync ID<br></td><td class="tg-ztj8">Computer Name<br></td></tr>')

    content_of_source_directory = os.walk(source_file_path)
    for paths, dirs, files in content_of_source_directory:
        for each_file in files:
            full_path = os.path.join(paths, each_file)
            full_list_of_files.append(full_path)

    for each in full_list_of_files:
        if os.path.basename(each) == 'sys.sqlite':
            filepath = os.path.realpath(each)
            connection_to_sqlite_db = sqlite3.connect(filepath)
            cursor_connection_to_sqlite_db = connection_to_sqlite_db.cursor()
            try:
                # Standard SQLite command which joins the tables.
                content_sys_sqlite_db = []
                connection_table_entries = cursor_connection_to_sqlite_db.execute("""
                SELECT connection_table.id,
                      connection_table.conn_mode,
                      connection_table.server_name,
                      connection_table.server_ip,
                      connection_table.server_port,
                      connection_table.quickconn_mode,
                      connection_table.username,
                      connection_table.ds_id,
                      session_table.id AS id1,
                      session_table.share_name,
                      session_table.conn_id,
                      datetime(session_table.ctime, 'unixepoch', 'localtime'),
                      session_table.sync_folder,
                      session_table.view_id,
                      connection_table.session,
                      connection_table.computer_name
                    FROM connection_table
                      LEFT JOIN session_table ON connection_table.id = session_table.conn_id""")
                add_information_message_to_log('Connection to the sys.sqlite database successful.')

                for each_entry in connection_table_entries:
                    content_sys_sqlite_db.append(each_entry)
                    connection_id = each_entry[0]
                    server_name = each_entry[2]
                    ip_address = each_entry[3]
                    server_port = each_entry[4]
                    quickconn_mode = each_entry[5]
                    username = each_entry[6]
                    ds_id = each_entry[7]
                    i_d = each_entry[8]
                    synology_directory = each_entry[9]
                    ctime = each_entry[11]
                    local_directory = each_entry[12]
                    sync_id = each_entry[13]
                    computer_name = each_entry[15]

                    html_report.write('<td><center>{}</center></td><td>{}</td><td>{}</td><td>{}</td'
                                      '><td>{}</td><td>{}</td><td>{}</td><td><center><b>{}</b></cen'
                                      'ter></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}<'
                                      '/td></tr>\n'
                                      .format(connection_id, server_name, ip_address, server_port,
                                              quickconn_mode, username, ds_id, i_d,
                                              synology_directory, ctime, local_directory, sync_id,
                                              computer_name))

                return content_sys_sqlite_db

            except IOError:
                add_critical_message_to_log('Unable to connect to the sys.sqlite database.')
                messagebox.showwarning('Unable to connect to the sys.sqlite database.')
            html_report.close()