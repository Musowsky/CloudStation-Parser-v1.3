"""
This script obtains the filter settings from within the filter.sqlite
database.  The results are placed into an HTML report.
"""

import sqlite3

tab = '\t'
new_line = '\n'
backslash_marker = '\\'
html_path_reference = 'file:\\\\localhost\\'
from utilities_directory.cloudstation_parser_logging import *
full_list_of_files = []         # Lists files including its full path.
list_of_live_sessions = []      # Identifies the sessions (in a list).


def parse_filter_sqlite_file(source_file_path, destination_folder_path, case_reference_number,
                             investigators_name, investigators_notes, exhibit_reference):
    """
    This script obtains the filter settings from the filter.sqlite db.
    """
    add_information_message_to_log('Filter DB script executed at script level.')
    content_of_source_directory = os.walk(source_file_path)
    html_report = open(destination_folder_path.strip() + '//Filter Exclusion Settings.html', 'w+',
                       encoding='UTF-8')
    html_report.write('<html><head><title>CloudStation Parser 1.3</title></head><body><br><br><cent'
                      'er><br><br><hr width="90%"><h2>CloudStation Parser (Filter Settings)</h2></c'
                      'enter><br /><div id="navigation"><left><b><font size="5">Case Information</f'
                      'ont></b></left><br /><left><font size="4">Case Reference - {}</font></left><'
                      'br /><left><font size="4">Exhibit Reference - {}</font></left><br /><left><f'
                      'ont size="4">Investigator - {}</font></left><br /><left><font size="4">Case '
                      'Notes - {}</font></left><br /><ul><br /><br /></ul>'
                      .format(case_reference_number, exhibit_reference, investigators_name,
                              investigators_notes))

    # Joins the files to their paths.
    for paths, dirs, files in content_of_source_directory:
        for each_file in files:
            full_path = os.path.join(paths, each_file)
            full_list_of_files.append(full_path)

    # Searches for the filter.sqlite database.
    for each in full_list_of_files:
        if os.path.basename(each) == 'filter.sqlite':
            filepath = os.path.realpath(each)

            html_report.write('<p style="font-family:aerial;font-stize:10px;"><h3>Filter settings c'
                              'ontained within the Filter database.</h3></></p>')

            html_report.write('<style type="text/css">.tg  {border-collapse:collapse;border-spacing'
                              ':0;}.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px'
                              ' 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:'
                              'normal;}.tg th{font-family:Arial, sans-serif;font-size:14px;font-wei'
                              'ght:normal;padding:10px 5px;border-style:solid;border-width:1px;over'
                              'flow:hidden;word-break:normal;}.tg .tg-g8rd{background-color:#7a8dec'
                              ';color:#333333;text-align:center}.tg .tg-ztj8{background-color:#b3bb'
                              'e7;text-align:center}.tg .tg-bsv2{background-color:#efefef}</style><'
                              'table class="tg"><tr><td class="tg-ztj8"><b>Session ID</b><br></td><'
                              'td class="tg-ztj8">Sync_ID<br></td><td class="tg-ztj8">Filter Type<b'
                              'r></td><td class="tg-ztj8">Filter Description<br></td></tr>')

            connection_to_sqlite_db = sqlite3.connect(filepath)
            cursor_connection_to_sqlite_db = connection_to_sqlite_db.cursor()
            try:
                filter_table_entries = cursor_connection_to_sqlite_db.execute("""SELECT
                sess_id, sync_id, filter_type, filter_desc FROM filter_table""")
                add_information_message_to_log('Connection to filter.sqlite database successful.')

                content_filter_db = []
                for each_entry in filter_table_entries:
                    content_filter_db.append(each_entry)
                    sess_id = each_entry[0]
                    sync_id = each_entry[1]
                    filter_type = each_entry[2]
                    filter_desc = each_entry[3]
                    html_report.write('<td><center><b>{}</b></center></td><td><center>{}</center></'
                                      'td><td><center>{}</center></td><td><center>{}</center></td><'
                                      '/tr>\n'.format(sess_id, sync_id, filter_type, filter_desc))
                return content_filter_db
            except IOError:
                add_critical_message_to_log('Unable to connect to the filter.sqlite database')