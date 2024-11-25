#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Tretor
#  Created by Ingenuity i/o on 2024/11/15
#
# <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
# <html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
# p, li { white-space: pre-wrap; }
# hr { height: 1px; border-width: 0; }
# li.unchecked::marker { content: "\2610"; }
# li.checked::marker { content: "\2612"; }
# </style></head><body style=" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;">
# <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">T<span style=" font-size:13px; color:#2a2a2a;">ool box for background computation and treatments for the karaoke app </span></p></body></html>
#

import signal
import getopt
import time
from pathlib import Path
import traceback
import sys

from Tretor import *

port = 5670
agent_name = "Tretor"
device = None
verbose = False
is_interrupted = False

short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()


def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


def print_usage_help():
    print("Available commands in the terminal:")
    print("	/quit : quits the agent")
    print("	/help : displays this message")

def return_io_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Integer"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"

def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN"

def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        if event == igs.AGENT_KNOWS_US:
            if name == "Tretor":
                print("Il est la le Treator")
    except:
        print(traceback.format_exc())


def on_freeze_callback(is_frozen, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        # add code here if needed
    except:
        print(traceback.format_exc())

# services
def run_pretreatment_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        agent_object.run_pretreatment(sender_agent_name, sender_agent_uuid)
    except:
        print(traceback.format_exc())


def save_melodie_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        output_file = tuple_args[0]
        agent_object.save_melodie(sender_agent_name, sender_agent_uuid, output_file)
    except:
        print(traceback.format_exc())


def play_melodie_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        melodie = tuple_args[0]
        agent_object.play_melodie(sender_agent_name, sender_agent_uuid, melodie)
    except:
        print(traceback.format_exc())


def generate_melodie_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        informations = tuple_args[0]
        out = agent_object.generate_melodie(sender_agent_name, sender_agent_uuid, informations)
        agent_object.outputO = str(out)
        

    except:
        print(traceback.format_exc())


def merge_audios_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        audio_1_path = tuple_args[0]
        audio_2_path = tuple_args[1]
        out = agent_object.merge_audios(sender_agent_name, sender_agent_uuid, audio_1_path, audio_2_path)

        agent_object.outputO = str(out)
        

    except:
        print(traceback.format_exc())


def save_file_informations_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        path_to_json_file = tuple_args[0]
        agent_object.save_file_informations(sender_agent_name, sender_agent_uuid, path_to_json_file)
    except:
        print(traceback.format_exc())


def load_song_infos_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        path_to_json_file = tuple_args[0]
        out = agent_object.load_song_infos(sender_agent_name, sender_agent_uuid, path_to_json_file)

        agent_object.outputO = str(out)

    except:
        print(traceback.format_exc())


def save_score_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        player_id = tuple_args[0]
        score = tuple_args[1]
        song_name = tuple_args[2]
        level = tuple_args[3]
        agent_object.save_score(sender_agent_name, sender_agent_uuid, player_id, score, song_name, level)
    except:
        print(traceback.format_exc())


def compare_audios_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        audio_file_1 = tuple_args[0]
        audio_file_2 = tuple_args[1]
        out = agent_object.compare_audios(sender_agent_name, sender_agent_uuid, audio_file_1, audio_file_2)

        agent_object.outputO = str(out)
        

    except:
        print(traceback.format_exc())


def extract_features_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        input_file = tuple_args[0]
        output_dir = tuple_args[1]
        out = agent_object.extract_features(sender_agent_name, sender_agent_uuid, input_file, output_dir)

        agent_object.outputO = str(out)
        

    except:
        print(traceback.format_exc())


def separate_audio_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        input_file = tuple_args[0]
        output_dir = tuple_args[1]
        out = agent_object.separate_audio(sender_agent_name, sender_agent_uuid, input_file, output_dir)

        agent_object.outputO = str(out)
        

    except:
        print(traceback.format_exc())


def transcribe_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        input_file = tuple_args[0]
        output_dir = tuple_args[1]
        out = agent_object.transcribe(sender_agent_name, sender_agent_uuid, input_file, output_dir)

        agent_object.outputO = str(out)
        

    except:
        print(traceback.format_exc())


def  parse_lrc_file_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        file_name = tuple_args[0]
        path_to_lrc = tuple_args[1]
        out = agent_object. parse_lrc_file(sender_agent_name, sender_agent_uuid, file_name, path_to_lrc)

        agent_object.outputO = str(out)
        

    except:
        print(traceback.format_exc())


def convert_to_wav_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        input_file = tuple_args[0]
        output_dir = tuple_args[1]
        out = agent_object.convert_to_wav(sender_agent_name, sender_agent_uuid, input_file, output_dir)

        agent_object.outputO = str(out)
        

    except:
        print(traceback.format_exc())


def get_frequency_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Tretor)
        note = tuple_args[0]
        octave = tuple_args[1]
        out = agent_object.get_frequency(sender_agent_name, sender_agent_uuid, note, octave)

        agent_object.outputO = str(out)
        

    except:
        print(traceback.format_exc())


if __name__ == "__main__":

    # catch SIGINT handler before starting agent
    signal.signal(signal.SIGINT, signal_handler)
    interactive_loop = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        igs.error(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-h" or o == "--help":
            print_usage()
            exit(0)
        elif o == "-v" or o == "--verbose":
            verbose = True
        elif o == "-i" or o == "--interactive_loop":
            interactive_loop = True
        elif o == "-p" or o == "--port":
            port = int(a)
        elif o == "-d" or o == "--device":
            device = a
        elif o == "-n" or o == "--name":
            agent_name = a
        else:
            assert False, "unhandled option"

    igs.agent_set_name(agent_name)
    igs.definition_set_description("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: "\2610"; }
li.checked::marker { content: "\2612"; }
</style></head><body style=" font-family:'Asap'; font-size:13px; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">T<span style=" font-size:13px; color:#2a2a2a;">ool box for background computation and treatments for the karaoke app </span></p></body></html>""")
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    if device is None:
        # we have no device to start with: try to find one
        list_devices = igs.net_devices_list()
        list_addresses = igs.net_addresses_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            igs.info("using %s as default network device (this is the only one available)" % str(device))
        elif len(list_devices) == 2 and (list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(device))
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error("No network device passed as command line parameter and several are available.")
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
                print_usage()
            exit(1)

    agent = Tretor()

    igs.observe_agent_events(on_agent_event_callback, agent)
    igs.observe_freeze(on_freeze_callback, agent)

    igs.output_create("output", igs.STRING_T, None)

    igs.service_init("run_pretreatment", run_pretreatment_callback, agent)
    igs.service_init("save_melodie", save_melodie_callback, agent)
    igs.service_arg_add("save_melodie", "output_file", igs.STRING_T)
    igs.service_init("play_melodie", play_melodie_callback, agent)
    igs.service_arg_add("play_melodie", "melodie", igs.STRING_T)
    igs.service_init("generate_melodie", generate_melodie_callback, agent)
    igs.service_arg_add("generate_melodie", "informations", igs.STRING_T)
    igs.service_init("merge_audios", merge_audios_callback, agent)
    igs.service_arg_add("merge_audios", "audio_1_path", igs.STRING_T)
    igs.service_arg_add("merge_audios", "audio_2_path", igs.STRING_T)
    igs.service_init("save_file_informations", save_file_informations_callback, agent)
    igs.service_arg_add("save_file_informations", "path_to_json_file", igs.STRING_T)
    igs.service_init("load_song_infos", load_song_infos_callback, agent)
    igs.service_arg_add("load_song_infos", "path_to_json_file", igs.STRING_T)
    igs.service_init("save_score", save_score_callback, agent)
    igs.service_arg_add("save_score", "player_id", igs.STRING_T)
    igs.service_arg_add("save_score", "score", igs.DOUBLE_T)
    igs.service_arg_add("save_score", "song_name", igs.STRING_T)
    igs.service_arg_add("save_score", "level", igs.STRING_T)
    igs.service_init("compare_audios", compare_audios_callback, agent)
    igs.service_arg_add("compare_audios", "audio_file_1", igs.STRING_T)
    igs.service_arg_add("compare_audios", "audio_file_2", igs.STRING_T)
    igs.service_init("extract_features", extract_features_callback, agent)
    igs.service_arg_add("extract_features", "input_file", igs.STRING_T)
    igs.service_arg_add("extract_features", "output_dir", igs.STRING_T)
    igs.service_init("separate_audio", separate_audio_callback, agent)
    igs.service_arg_add("separate_audio", "input_file", igs.STRING_T)
    igs.service_arg_add("separate_audio", "output_dir", igs.STRING_T)
    igs.service_init("transcribe", transcribe_callback, agent)
    igs.service_arg_add("transcribe", "input_file", igs.STRING_T)
    igs.service_arg_add("transcribe", "output_dir", igs.STRING_T)
    igs.service_init(" parse_lrc_file",  parse_lrc_file_callback, agent)
    igs.service_arg_add(" parse_lrc_file", "file_name", igs.STRING_T)
    igs.service_arg_add(" parse_lrc_file", "path_to_lrc", igs.STRING_T)
    igs.service_init("convert_to_wav", convert_to_wav_callback, agent)
    igs.service_arg_add("convert_to_wav", "input_file", igs.STRING_T)
    igs.service_arg_add("convert_to_wav", "output_dir", igs.STRING_T)
    igs.service_init("get_frequency", get_frequency_callback, agent)
    igs.service_arg_add("get_frequency", "note", igs.STRING_T)
    igs.service_arg_add("get_frequency", "octave", igs.STRING_T)

    igs.start_with_device(device, port)
    # catch SIGINT handler after starting agent
    signal.signal(signal.SIGINT, signal_handler)

    if interactive_loop:
        print_usage_help()
        while True:
            command = input()
            if command == "/quit":
                break
            elif command == "/help":
                print_usage_help()
    else:
        while (not is_interrupted) and igs.is_started():
            time.sleep(2)

    if igs.is_started():
        igs.stop()
