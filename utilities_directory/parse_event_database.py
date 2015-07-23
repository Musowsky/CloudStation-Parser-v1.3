"""
This script parses the event-db.sqlite database to extract four main
areas: event_table, recycle_bin_table, local_filter_table &
server_filter_table.  The event_table and recycle_bin_table have their
own report, whilst the two filters share the same report.
"""


import re
import sqlite3
from utilities_directory.cloudstation_parser_logging import *

full_list_of_files = []     # list of each file including full path.
list_of_live_sessions = []  # list of each session as a list.


def parse_event_db_file(source_file_path, destination_folder_path, case_reference_number,
                        investigators_name, investigators_notes, exhibit_reference):
    """
    This function takes the parameters supplied by the main GUI to run
    three seperate sections:
    """
    add_information_message_to_log('Event DB script executed at script level.')

    content_of_source_directory = os.walk(source_file_path)

    # Joins the files to their paths.
    for paths, dirs, files in content_of_source_directory:
        for each_file in files:
            full_path = os.path.join(paths, each_file)
            full_list_of_files.append(full_path)

    # Identifies the synchronized files per session.
    for each in full_list_of_files:
        if os.path.basename(each) == 'event-db.sqlite':
            split_up_of_path = re.split(r'[//\\]', each)
            directory_number = split_up_of_path[-3]
            filepath = (os.path.realpath(each))

            html_report = open(''.join([destination_folder_path.strip(),
                                        '//Session ', directory_number, ' - Synchronized Files'
                                        '.html']), 'w+', encoding='UTF-8')

            html_report.write('<html><head><title>CloudStation Parser v1.3</title></head><body><br>'
                              '<br><center><br><br><hr width="90%"><h2>CloudStation Parser - Synchr'
                              'onized Files</h2></center><br /><div id="navigation"><left><b><font '
                              'size="5">Case Information</font></b></left><br /><left><font size="4'
                              '">Case Reference - {}</font></left><br /><left><font size="4">Exhibi'
                              't Reference - {}</font></left><br /><left><font size="4">Investigato'
                              'r - {}</font></left><br /><left><font size="4">Case Notes - {}</font'
                              '></left><br /><ul></br></br></ul>'
                              .format(case_reference_number, exhibit_reference, investigators_name,
                                      investigators_notes))

            html_report.write('<p style="font-family:aerial;font-stize:10px;"><h3>Synchronized File'
                              's in Session {}.</h3></></p>'.format(directory_number))

            html_report.write('<style type="text/css">.tg  {border-collapse:collapse;border-spacing'
                              ':0;}.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px'
                              ' 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:'
                              'normal;}.tg th{font-family:Arial, sans-serif;font-size:14px;font-wei'
                              'ght:normal;padding:10px 5px;border-style:solid;border-width:1px;over'
                              'flow:hidden;word-break:normal;}.tg .tg-g8rd{background-color:#7a8dec'
                              ';color:#333333;text-align:center}.tg .tg-ztj8{background-color:#b3bb'
                              'e7;text-align:center}.tg .tg-bsv2{background-color:#efefef}</style><'
                              'table class="tg"><tr><td class="tg-ztj8">ID<br></td><td class="tg-zt'
                              'j8">Sync_ID<br></td><td class="tg-ztj8">File Size<br></td><td class='
                              '"tg-ztj8">File Modified Time (UTC)<br></td><td class="tg-ztj8">Hash '
                              'Value<br></td><td class="tg-ztj8">File Path<br></td></tr>')

            try:
                connection_to_sqlite_db = sqlite3.connect(filepath)
                cursor_connection_to_sqlite_db = connection_to_sqlite_db.cursor()
                connection_table_entries = cursor_connection_to_sqlite_db.execute("""
                SELECT
                id, fileType, syncID, fileSize, datetime(fileModTime, 'unixepoch', 'localtime'),
                fileCheckSum, path
                from
                event_table""")

                global content_event_db_mainfiles
                content_event_db_mainfiles = []
                for x in connection_table_entries:
                    content_event_db_mainfiles.append(x)
                    id_number = x[0]
                    # file_type = x[1]
                    sync_id = x[2]
                    file_size = x[3]
                    file_mod_time = x[4]
                    hash_value = x[5]
                    path = x[6]
                    html_report.write('<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'
                                      '}</td></tr>\n'.format(id_number, sync_id, file_size,
                                                             file_mod_time, hash_value, path))

            except IOError:
                add_critical_message_to_log('Unable to fully connect to the event-db.sqlite databas'
                                            'e.')
        else:
            # If no event-db.sqlite, the script will break and return
            # an empty statement.
            pass

    # This is the second portion of the script that deals with the
    # server_filter_table per session.
    for each in full_list_of_files:
        if os.path.basename(each) == 'event-db.sqlite':
            split_up_of_path = re.split(r'[//\\]', each)
            directory_number = split_up_of_path[-3]
            filepath = (os.path.realpath(each))

            html_report = open(''.join([destination_folder_path.strip(),
                                        '//Session ', directory_number, ' - Filtered Files'
                                        '.html']), 'w+', encoding='UTF-8')

            html_report.write('<html><head><title>CloudStation Parser 1.3</title></head><body><br><'
                              'br><center><br><br><hr width="90%"><h2>CloudStation Parser - Filtere'
                              'd Files</h2></center><br /><div id="navigation"><left><b><font size'
                              '="5">Case Information</font></b></left><br /><left><font size="4">Ca'
                              'se Reference - {}</font></left><br /><left><font size="4">Exhibit Re'
                              'ference - {}</font></left><br /><left><font size="4">Investigator - '
                              '{}</font></left><br /><left><font size="4">Case Notes - {}</font></l'
                              'eft><br /><ul></br></br></ul>'.format(case_reference_number,
                                                                     exhibit_reference,
                                                                     investigators_name,
                                                                     investigators_notes))

            html_report.write('<p style="font-family:aerial;font-stize:10px;"><h3>Files filtered ou'
                              't during Session {}.</h3></></p>'.format(directory_number))

            html_report.write('<style type="text/css">.tg  {border-collapse:collapse;border-spacing'
                              ':0;}.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px'
                              ' 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:'
                              'normal;}.tg th{font-family:Arial, sans-serif;font-size:14px;font-wei'
                              'ght:normal;padding:10px 5px;border-style:solid;border-width:1px;over'
                              'flow:hidden;word-break:normal;}.tg .tg-g8rd{background-color:#7a8dec'
                              ';color:#333333;text-align:center}.tg .tg-ztj8{background-color:#b3bb'
                              'e7;text-align:center}.tg .tg-bsv2{background-color:#efefef}</style><'
                              'table class="tg"><tr><td class="tg-ztj8">Filter Location<br></td><td'
                              ' class="tg-ztj8">Name<br></td><td class="tg-ztj8">Name<br></td><td c'
                              'lass="tg-ztj8">File Size<br></td><td class="tg-ztj8">File Modified T'
                              'ime (UTC)<br></td><td class="tg-ztj8">Hash Value<br></td><td class="'
                              'tg-ztj8">Path<br></td></tr>')

            # Identifies the filtered files from DiskStation.
            try:
                connection_to_sqlite_db = sqlite3.connect(filepath)
                cursor_connection_to_sqlite_db = connection_to_sqlite_db.cursor()
                connection_table_entries = cursor_connection_to_sqlite_db.execute("""
                SELECT
                id, syncID, name, fileSize, datetime(fileModTime, 'unixepoch', 'localtime'),
                fileCheckSum, path
                from
                server_filter_table""")
                filtered_file_server = 'DiskStation File'

                global content_event_db_serverfiltered
                content_event_db_serverfiltered = []
                for each_entry in connection_table_entries:
                    content_event_db_serverfiltered.append(each_entry)
                    sync_id_server = each_entry[1]
                    name_server = each_entry[2]
                    file_size_server = each_entry[3]
                    file_mod_time_server = each_entry[4]
                    hash_value_server = each_entry[5]
                    path_server = each_entry[6]
                    html_report.write('<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'
                                      '}</td><td>{}</td></tr>\n'
                                      .format(filtered_file_server, sync_id_server, name_server,
                                              file_size_server, file_mod_time_server,
                                              hash_value_server, path_server))
            except IOError:
                add_critical_message_to_log('Cannot connect to the event-db.sqlite database.')

            # This is the second portion of the script that deals with the
            # server_filter_table per session.
            # Identifies the filtered files from the local computer.
            try:
                connection_to_sqlite_db = sqlite3.connect(filepath)
                cursor_connection_to_sqlite_db = connection_to_sqlite_db.cursor()
                connection_table_entries = cursor_connection_to_sqlite_db.execute("""
                SELECT
                syncID, name, fileSize, fileModTime, fileCheckSum, path
                from
                local_filter_table""")
                filtered_file_local = 'Local File'

                global content_event_db_localfiltered
                content_event_db_localfiltered = []
                for y in connection_table_entries:
                    content_event_db_localfiltered.append(y)
                    sync_id_local = y[0]
                    name_local = y[1]
                    file_size_local = y[2]
                    file_mod_time_local = y[3]
                    hash_value_local = y[4]
                    path_local = y[5]
                    html_report.write('<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{'
                                      '}</td><td>{}</td></tr>\n'
                                      .format(filtered_file_local, sync_id_local, name_local,
                                              file_size_local, file_mod_time_local,
                                              hash_value_local, path_local))
            except IOError:
                add_critical_message_to_log('Unable to connect to sys.sqlite database.')

    # This is the third portion of the script that deals with the
    # recycled files (recycle_bin_table).
    for each in full_list_of_files:
        if os.path.basename(each) == 'event-db.sqlite':
            split_up_of_path = re.split(r'[//\\]', each)
            directory_number = split_up_of_path[-3]
            filepath = (os.path.realpath(each))

            html_report = open(''.join([destination_folder_path.strip(),
                                        '//Session ', directory_number, ' - Recycled Files'
                                        '.html']), 'w+', encoding='UTF-8')

            html_report.write('<html><head><title>CloudStation Parser 1.3</title></head><body><br><'
                              'br><center><br><br><hr width="90%"><h2>CloudStation Parser - Recycle'
                              'd Files</h2></center><br /><div id="navigation"><left><b><font size'
                              '="5">Case Information</font></b></left><br /><left><font size="4">Ca'
                              'se Reference - {}</font></left><br /><left><font size="4">Exhibit Re'
                              'ference - {}</font></left><br /><left><font size="4">Investigator - '
                              '{}</font></left><br /><left><font size="4">Case Notes - {}</font></l'
                              'eft><br /><ul></br></br></ul>'.format(case_reference_number,
                                                                     exhibit_reference,
                                                                     investigators_name,
                                                                     investigators_notes))

            html_report.write('<p style="font-family:aerial;font-stize:10px;"><h3>Files Recycled du'
                              'ring Session {}.</h3></></p>'.format(directory_number))

            html_report.write('<style type="text/css">.tg  {border-collapse:collapse;border-spacing'
                              ':0;}.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px'
                              ' 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:'
                              'normal;}.tg th{font-family:Arial, sans-serif;font-size:14px;font-wei'
                              'ght:normal;padding:10px 5px;border-style:solid;border-width:1px;over'
                              'flow:hidden;word-break:normal;}.tg .tg-g8rd{background-color:#7a8dec'
                              ';color:#333333;text-align:center}.tg .tg-ztj8{background-color:#b3bb'
                              'e7;text-align:center}.tg .tg-bsv2{background-color:#efefef}</style><'
                              'table class="tg"><tr><td class="tg-ztj8">ID<br></td><td class="tg-zt'
                              'j8">Path<br></td><td class="tg-ztj8">File Size<br></td><td class="tg'
                              '-ztj8">Hash Value<br></td><td class="tg-ztj8">Deleted Time (UTC)<br>'
                              '</td></tr>')

            try:
                connection_to_sqlite_db = sqlite3.connect(filepath)
                cursor_connection_to_sqlite_db = connection_to_sqlite_db.cursor()
                connection_table_entries = cursor_connection_to_sqlite_db.execute("""
                SELECT
                id, path, fileSize, fileCheckSum, datetime(time, 'unixepoch', 'localtime')
                from
                recycle_bin_table""")
                global content_event_db_recycled_files
                content_event_db_recycled_files = []
                for each_entry in connection_table_entries:
                    content_event_db_recycled_files.append(each_entry)
                    file_id = each_entry[0]
                    path = each_entry[1]
                    filesize = each_entry[2]
                    filechecksum = each_entry[3]
                    time = each_entry[4]
                    html_report.write('<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'
                                      '\n'.format(file_id, path, filesize, filechecksum, time))
            except IOError:
                add_critical_message_to_log('Cannot connect to the event-db.sqlite database.')

    return(content_event_db_mainfiles, content_event_db_localfiltered,
           content_event_db_serverfiltered, content_event_db_recycled_files)