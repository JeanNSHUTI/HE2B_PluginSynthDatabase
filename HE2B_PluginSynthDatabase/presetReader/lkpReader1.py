import os
from typing import List, Union

import presetReader.DictLP
import mysql.connector
import struct
from prettytable import PrettyTable
import numpy as np
# from mido import messages
# from mido import ports
# from mido.backends import backend
# from mido.backends.backend import open_output
import mido

BLOCK = 180


# Function used to read lokomotiv synth preset files
def read_lkp_preset(filepaths):
    for lkpfile in range(0, len(filepaths)):
        with open(filepaths[lkpfile], "rb") as lkp:
            data = lkp.read(BLOCK)
            print(data)

            # set preset key and name
            presetReader.DictLP.lokomotive_set[0] = data[0:28].hex()
            presetReader.DictLP.lokomotive_set[1] = data[28:56].decode("ASCII")

            # Split binary data stream and set rest of parameter values
            # format float Big endian
            a = 2
            for byte in range(56, 180, 4):
                # print(data[byte:byte + 4])
                tuple_result = struct.unpack('!f', data[byte:byte + 4])
                presetReader.DictLP.lokomotive_set[a] = tuple_result[0]
                # print(DictLP.lokomotive_set[a])
                a += 1

            # Mapping of synth parameters that are not in range [0..1]
            presetReader.DictLP.lokomotive_set[3] = maprange((0.000, 1.000), (0.000, 5.000),
                                                             presetReader.DictLP.lokomotive_set[3])
            presetReader.DictLP.lokomotive_set[5] = maprange((0.000, 1.000), (0.000, 4.000),
                                                             presetReader.DictLP.lokomotive_set[5])
            presetReader.DictLP.lokomotive_set[19] = maprange((0.000, 1.000), (0.000, 2.000),
                                                              presetReader.DictLP.lokomotive_set[19])
            presetReader.DictLP.lokomotive_set[20] = maprange((0.000, 1.000), (0.000, 2.000),
                                                              presetReader.DictLP.lokomotive_set[20])
            presetReader.DictLP.lokomotive_set[29] = maprange((0.000, 1.000), (0.000, 23.000),
                                                              presetReader.DictLP.lokomotive_set[29])
            presetReader.DictLP.lokomotive_set[30] = maprange((0.000, 1.000), (0.000, 3.000),
                                                              presetReader.DictLP.lokomotive_set[30])
            presetReader.DictLP.lokomotive_set[31] = maprange((0.000, 1.000), (0.000, 2.000),
                                                              presetReader.DictLP.lokomotive_set[31])

            print(presetReader.DictLP.lokomotive_set[0])
            print(presetReader.DictLP.lokomotive_set[1])
            print(presetReader.DictLP.display_preset_name())

            # print(DictLP.lokomotive_set[3])
            # print(DictLP.lokomotive_set[5])
            # print(DictLP.lokomotive_set[19])

            lkp.close()
            add_preset()
    return 1


def maprange(a, b, s):
    (a1, a2), (b1, b2) = a, b
    return round(b1 + ((s - a1) * (b2 - b1) / (a2 - a1)), 6)  # float precision


# Function used to connect to mysql database
def db_connection():
    config = {
        'user': 'root',
        'password': '56955jean',
        'host': 'localhost',
        'database': 'synth_plugin_presets',
        'port': 3306,
        'raise_on_warnings': True,
    }

    try:
        # Connect to db
        dbconn = mysql.connector.connect(**config)
        # print(dbconn)
        return dbconn
    except ConnectionRefusedError as e:
        print(e)
    except ConnectionError as e1:
        print(e1)


# Function used to close connection to mysql database
def db_close(dbconnection, db_cursor):
    if dbconnection or db_cursor:
        dbconnection.close()
        db_cursor.close()
        # print("Connection closed")


# Function used to post to mysql database
def add_preset():
    # Query
    query = """INSERT INTO synth_plugin_presets.lokomotiv_presets (pkey, pname, bpm_sync, lfo_type_select, lfo_speed, 
                lfo_target_select, lfo_amount, osc_hardsync_amount, osc_pw_amount, osc_saw_detune_amount, 
                sub_osc_waveform, osc_noise_amount, osc_saw_amount, osc_pulse_amount, sub_osc_amount, env_attack, 
                env_decay, env_sustain, env_release, phonic_type,  filter_type_select, cutoff_amount, resonance_amount,
                kb_tracking_amount, envelope_amount, drive_pre_post_switch, drive_amount, amp_env_gate_select, 
                amp_volume, pitch_bend_range, mod_wheel_target_select,  velocity_target_select, portamento_speed)
                VALUES ('%s', "%s", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )""" \
                                    % (presetReader.DictLP.lokomotive_set[0], presetReader.DictLP.lokomotive_set[1],
                                       presetReader.DictLP.lokomotive_set[2], presetReader.DictLP.lokomotive_set[3],
                                       presetReader.DictLP.lokomotive_set[4], presetReader.DictLP.lokomotive_set[5],
                                       presetReader.DictLP.lokomotive_set[6], presetReader.DictLP.lokomotive_set[7],
                                       presetReader.DictLP.lokomotive_set[8], presetReader.DictLP.lokomotive_set[9],
                                       presetReader.DictLP.lokomotive_set[10], presetReader.DictLP.lokomotive_set[11],
                                       presetReader.DictLP.lokomotive_set[12],
                                       presetReader.DictLP.lokomotive_set[13], presetReader.DictLP.lokomotive_set[14],
                                       presetReader.DictLP.lokomotive_set[15],
                                       presetReader.DictLP.lokomotive_set[16], presetReader.DictLP.lokomotive_set[17],
                                       presetReader.DictLP.lokomotive_set[18],
                                       presetReader.DictLP.lokomotive_set[19], presetReader.DictLP.lokomotive_set[20],
                                       presetReader.DictLP.lokomotive_set[21],
                                       presetReader.DictLP.lokomotive_set[22], presetReader.DictLP.lokomotive_set[23],
                                       presetReader.DictLP.lokomotive_set[24],
                                       presetReader.DictLP.lokomotive_set[25], presetReader.DictLP.lokomotive_set[26],
                                       presetReader.DictLP.lokomotive_set[27],
                                       presetReader.DictLP.lokomotive_set[28], presetReader.DictLP.lokomotive_set[29],
                                       presetReader.DictLP.lokomotive_set[30],
                                       presetReader.DictLP.lokomotive_set[31], presetReader.DictLP.lokomotive_set[32])

    # Open db connection
    db = db_connection()
    # Create cursor
    dbcursor = db.cursor()
    # Execute query
    dbcursor.execute(query)
    # Commit
    db.commit()
    # Close connection
    db_close(db, dbcursor)


# Function used to fetch all file paths for .lkp file in given directory
def get_lkp_filepaths(directory, filetype):
    print(directory)
    file_paths: List[Union[bytes, str]] = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(filetype.lower()):
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

    print(file_paths)
    return file_paths


# Function used to update Database
# Function truncates table and "re-adds" all presets
# Slow but evades having to search for recently edited/new files
def update(db_table, file_paths):
    table_truncate(db_table)
    # Collect filepaths in array
    full_file_paths = get_lkp_filepaths(file_paths, ".lkp")
    # full_file_paths = get_lkp_filepaths("/Users/jeannshuti/Admin/Uni/HE2B/PBE/Lokomotiv presets/dbtest", ".lkp")

    # Read and add preset file
    try:
        if read_lkp_preset(full_file_paths):
            # Check how many files have been updated
            query1 = "SELECT id FROM synth_plugin_presets.%s" % db_table
            # Open db connection
            db = db_connection()
            # Create cursor
            dbcursor = db.cursor()
            # Execute query

            dbcursor.execute(query1)
            dbcursor.fetchall()
            rowcount = dbcursor.rowcount
            db_close(db, dbcursor)
            print(str(rowcount) + " files have been uploaded successfully")
    except TypeError as e:
        print("Error executing MySQL commands for <update> : ", e)
        # raise RuntimeError("Error executing MySQL commands for <update> : ", sys.exc_info()[0])


def table_truncate(table):
    # If table is not empty, truncate before updating presets in db
    # queries
    query1 = "SELECT COUNT(*) FROM synth_plugin_presets.%s" % table
    query2 = "TRUNCATE TABLE synth_plugin_presets.%s" % table

    # Open db connection
    db = db_connection()
    # Create cursor
    dbcursor = db.cursor()
    dbcursor.execute(query1)
    res = dbcursor.fetchone()
    rowcount = res[0]

    if rowcount:
        print(rowcount)
        dbcursor.execute(query2)

    # Close connection
    db_close(db, dbcursor)


# Method collects all presets from db and print them
def list_presets(dbtable):
    # query
    query1 = "SELECT date_created, id, pname FROM synth_plugin_presets.%s" % dbtable
    # query1 = "SELECT date_created, id, pname FROM synth_plugin_presets.%s LIMIT 100" % dbtable
    # Pretty table headings for output printing
    preset_table = PrettyTable(["Date updated", "Preset ID", "Preset Name"])
    # Left align city names
    preset_table.align["Preset Name"] = "l"

    # Open db connection
    db = db_connection()
    # Create cursor
    dbcursor = db.cursor()

    try:
        # Execute query
        dbcursor.execute(query1)
        records = dbcursor.fetchall()
        record_count = dbcursor.rowcount

        print("Collected " + str(record_count) + " presets: ")

        for row in records:
            preset_table.add_row([row[0], row[1], row[2]])

        print(preset_table)

    except mysql.connector.Error as e:
        print("Error reading presets from MySQL table: ", e)

    finally:
        if db.is_connected():
            db_close(db, dbcursor)


# Method used to find preset selected by user and load
# it into synth in DAW
def load_preset(identifier):
    # Collect data
    # Check if identifier is a preset id or name
    if identifier.isnumeric():
        query = "SELECT * FROM synth_plugin_presets.lokomotiv_presets WHERE id = %s" % identifier
    else:
        identifier = identifier + "%"
        query = "SELECT * FROM synth_plugin_presets.lokomotiv_presets WHERE pname LIKE '%s'" % identifier

    # Open db connection
    db = db_connection()
    # Create cursor
    dbcursor = db.cursor()
    try:
        dbcursor.execute(query)
        preset_record = dbcursor.fetchall()
        # print(len(preset_record))
        print(preset_record[0])

        # Convert preset param values to MIDI CC
        cc_values = convert_to_midi(preset_record[0])
        print(cc_values)

        # send data to DAW
        send_to_daw(cc_values, identifier)
    except IndexError as e:
        raise IndexError("Error executing MySQL commands for <load>. Verify name/index of preset you are "
                         "trying to load: ", e)


# mapping function to covert read lkp values
# to MIDI CC values between 0 and 127
def convert_to_midi(preset):
    cc_preset_array = np.zeros(len(preset) - 4)
    i = 0
    # first parameter at index 4
    for param in range(4, len(preset)):
        # Skip values that have already been mapped
        if type(preset[param]) is float:
            cc_preset_array[i] = round(maprange((0.000, 1.000), (0.000, 127.000), preset[param]))
        else:
            cc_preset_array[i] = preset[param]
        i = i + 1
    return cc_preset_array


def send_to_daw(midi_cc_values, identifier):
    # MIDI comm
    mdo = mido.Backend()
    ports = mdo.get_output_names()

    print(ports)
    port = mdo.open_output('Gestionnaire IAC IAC Bus 1')
    # Midi learn in DAW -> first parameter
    cc = 83

    for param in range(0, len(midi_cc_values)):
        print(midi_cc_values[param])
        msg = mido.Message('control_change', channel=0, control=cc, value=int(midi_cc_values[param]))
        port.send(msg)
        cc = cc + 1
    print(cc)

    print("loaded " + identifier + " successfully.")

    # msg = mido.Message('control_change', channel=0, control=108, value=127)
