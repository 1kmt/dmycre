#!/usr/bin/env python3

__description__ = """
This tool creates dummy files for program testing.
You can specify the size and number of files to create.
The data is in binary format and can be selected from random numbers, fixed values, and sequential numbers.
"""
__date__ = "2022/08/08"
__version__ = "1.0.0"
__author__ = "ikmt"

"""
_________________________________________________________________
Need package for working
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
python -m pip install numpy
_________________________________________________________________
Required version of Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Available since Python 3.6
v3.6 - formatted string literal (f-string)
v3.2 - to_bytes()
v3.2 - logging.Formatter() (Changed in version 3.2:added style parameter)
_________________________________________________________________
Test environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
OS: windows 10
pip version: 20.0.2
Python version: 3.7.6
_________________________________________________________________
Command line examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
python dmycre.py -l 10 20 100 20000000 -m 10 -rnd
python dmycre.py -l 20 100 -m 30 -fix 09AB -o ./dummy
python dmycre.py -r 1000 1002 -m 30 -seq 00 FF -o ./dummy
_________________________________________________________________
Changelog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2022-08-08 v1.0.0 release
"""

import argparse
import datetime
import logging
import math
import numpy as np
import os


# Constants
SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_BASE_PATH = os.path.expanduser("~/Desktop")
OUTPUT_DIR_NAME = "dummyfiles"


# Configuring logging
log_format_string = "{asctime}[{levelname:.1}] {message}"
date_format_string = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    style="{", 
    fmt=log_format_string, 
    datefmt=date_format_string
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    # Output log to terminal
    log_stream_handler = logging.StreamHandler()
    log_stream_handler.setFormatter(formatter)
    logger.addHandler(log_stream_handler)
    # Check command line arguments
    args = check_argument()
    amount_files = args.howmany
    size_list = get_creation_file_Size_list(args)
    size_list_length = len(size_list)
    # Create an output directory
    output_dir = create_dir(args.output)
    # Start message
    logger.info(f"[{'START':<9}] {__file__}")
    logger.info(f"[{'OUT_DIR':<9}] {output_dir}")

    for i in range(0, size_list_length):
        logger.info(f"[{'MAKE_FILE':<9}] {size_list[i]:0>10d} bytes x {amount_files:d} files")

        for j in range(1, amount_files + 1):
            bin_data = bytes()

            if(args.random):
                bin_data = get_random_data(size_list[i])
            elif(args.fixed is not None):
                bin_data = get_fixed_data(size_list[i], args.fixed)
            elif(args.sequential is not None):
                value_list = args.sequential
                bin_data = get_sequential_data(size_list[i], value_list[0], value_list[1])

            file_name = f"size{size_list[i]:011d}_{j:04d}.dat"
            output_path = os.path.join(output_dir, file_name)
            write(bin_data, output_path)

            show_progress(j, amount_files)

    # End message
    logger.info(f"[{'END':<9}] {__file__}")

    return 0


def check_argument():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-m", "--howmany", 
        type=int, 
        default=1, 
        help="specify the number of files to create"
    )
    parser.add_argument("-o", "--output", 
        type=str, 
        help="change the output directory"
    )
    parser.add_argument("-v", "--version", 
        action="version", 
        version="%(prog)s " + __version__
    )

    size_group = parser.add_mutually_exclusive_group(required=True)
    size_group.add_argument("-l", "--list", 
        type=int, 
        nargs="+", 
        help="specify a list of file sizes (e.g. -l 10 100 200 2000000)"
    )
    size_group.add_argument("-r", "--range", 
        type=int, 
        nargs=2, 
        help="specify a range of file sizes (e.g. -r 10 20)"
    )

    value_group = parser.add_mutually_exclusive_group(required=True)
    value_group.add_argument("-rnd", "--random", 
        action="store_true", 
        help="writes a random number to the file"
    )
    value_group.add_argument("-fix", "--fixed", 
        type=lambda x: int(x, base=16), 
        help="specifies a fixed value to be written to the file (e.g. -fix 09AB)"
    )
    value_group.add_argument("-seq", "--sequential", 
        type=lambda x: int(x, base=16), 
        nargs=2, 
        help="specifies a sequential number to be written to the file (e.g. -seq 00 FF, -seq FF 00)"
    )
    args = parser.parse_args()

    # Check the number of files to create
    if(args.howmany <= 0):
        logger.info("The -m option must be a positive integer.")
        exit(-2)

    return args


def get_creation_file_Size_list(args):
    """List the sizes of the files to be created."""
    size_list = []
    size_list = args.list
    if(args.range):
        size_range_list = sorted(args.range)
        size_list = list(range(size_range_list[0], (size_range_list[1] + 1)))
    # The file size must be a positive integer.
    if(min(size_list) <= 0):
        logger.info("The --list and --range option must be a list of positive integers.")
        exit(-2)

    return size_list


def create_dir(dir_path, batch=False):
    """Create a directory"""
    abs_dir_path = ""
    if(dir_path):
        abs_dir_path = os.path.abspath(dir_path)
    else:
        dt = datetime.datetime.today()
        now = dt.strftime("%Y%m%d_%Hh%Mm%S")
        path = os.path.join(OUTPUT_BASE_PATH, OUTPUT_DIR_NAME + "_" + now)
        abs_dir_path = os.path.abspath(path)

    # Add a suffix if the same filename already exists.
    if(os.path.isfile(abs_dir_path)):
        for i in itertools.count(1):
            if(not os.path.isfile(abs_dir_path + f"({i})")):
                abs_dir_path += f"({i})"
                break
    
    if(not os.path.isdir(abs_dir_path)):
        os.makedirs(abs_dir_path)

    return abs_dir_path


def get_random_data(size):
    """Return a random number of the specified size."""
    return np.random.bytes(size)


def get_fixed_data(size, fixed_value):
    """Repeats a fixed value to get the specified size."""
    hex_string = f"{fixed_value:x}"
    #if(len(hex_string) / 2 != 0):
    #	hex_string = hex_string.rjust(len(hex_string) + 1, "0")
    bin_data = int(hex_string, base=16).to_bytes(int(math.ceil(len(hex_string) / 2)), "big")

    while(len(bin_data) < size):
        # Double, quadruple, octuple, and so on.
        bin_data = bin_data + bin_data
    
    bin_data = bin_data[:size]

    return bin_data


def get_sequential_data(size, start_value, end_value):
    """Repeats a sequential value to get the specified size."""
    bin_data = bytes()

    if(start_value <= end_value):
        range_size = end_value - start_value
        if(range_size > size):
            end_value = start_value + size
        
        for i in range(start_value, end_value + 1):
            hex_string = f"{i:x}"
            byte_data = i.to_bytes(int(math.ceil(len(hex_string) / 2)), "big")
            bin_data = bin_data + byte_data
    else:
        range_size = start_value - end_value
        if(range_size > size):
            end_value = start_value - size

        for i in range(start_value, end_value - 1, -1):
            hex_string = f"{i:x}"
            byte_data = i.to_bytes(int(math.ceil(len(hex_string) / 2)), "big")
            bin_data = bin_data + byte_data

    while(len(bin_data) < size):
        # Double, quadruple, octuple, and so on.
        bin_data = bin_data + bin_data
    
    bin_data = bin_data[:size]

    return bin_data


def write(data, file_path):
    """Writing Binary Data to File
    Continue processing even if an exception occurs.
    """
    try:
        with open(file_path, "wb") as wfp:
            wfp.write(data)
    except PermissionError as e:
        print("")
        logger.error(f"PermissionError:{file_path}")
        logger.error("Permission denied. Are you using a file?")
    except OSError:
        print("")
        logger.error(f"OSError:{file_path}")
        logger.error("Failed to write to the file.")


def show_progress(current, total):
    """Show progress bar"""
    max_width = 40
    out = ("█" * int((max_width / total) * current))
    percent = (100 / total) * current
    print(
        f"\rPROGRESS|{('█' * max_width) if(len(out) >= max_width) else out:<{max_width}s}|"
        + f" {current:>4d}/{total:<4d} ( {percent:.1f}% )",
        end=""
    )

    if(percent >= 100 or len(out) >= max_width):
        print("")


# Execute a script from the Command Line
if __name__ == "__main__":
    main()
