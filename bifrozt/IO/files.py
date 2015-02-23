"""The functions can be used in various file I/O operations. """


"""
Copyright (c) 2014, Are Hansen - Honeypot Development.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list
of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or other
materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND AN
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY 
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


__author__ = 'Are Hansen'
__date__ = '2014, Oct 11'
__version__ = '0.0.4'


import sys


def readfile(file_obj):
    """Expects that the file_obj is a list containing the absolute path name to the files.
    Each line of these files are opened and read before being appended to the file_lines. 
    The name of the files and its lines are used to create a dictionary object called
    caled file_dict, the file names are set as the keys and the file_lines are set as the
    values. The file_dict object is returned from the function. """
    file_lines = []

    if len(file_obj) == 0:
        print '[ERROR]: Received empty file object'
        sys.exit(1)

    for obj in file_obj:
        with open(obj, 'r') as lines:
            for line in lines.readlines():
                file_lines.append(line)

    if len(file_lines) == 0:
        print '[ERROR]: Reading the file objects did not provide any data'
        sys.exit(1)

    return sorted(file_lines)


def readfiledict(file_obj):
    """Expects that the file_obj is a list containing the absolute path name to the files.
    Each line of these files are opened and read before being appended to the file_lines. 
    The name of the files and its lines are used to create a dictionary object called
    caled file_dict, the file names are set as the keys and the file_lines are set as the
    values. The file_dict object is returned from the function. """
    file_lines = []
    file_dict = {}

    if len(file_obj) == 0:
        print '[ERROR]: Received empty file object'
        sys.exit(1)

    for obj in file_obj:
        with open(obj, 'r') as lines:
            for line in lines.readlines():
                file_lines.append(line)

            file_dict[obj] = file_lines
            file_lines = []

    if len(file_dict) == 0:
        print '[ERROR]: Reading the file objects did not provide any data'
        sys.exit(1)

    return file_dict


def getdata(fdict):
    """Receives a dictionary where the key contains the file name and the value holds a 
    list containing the data of that file. The file name is ignored while the data
    represented within the file is appended to a list object thats returned upon 
    completing its execution. """
    data_list = []

    if len(fdict) == 0:
        print '[ERROR]: File dictionary length is NULL'
        sys.exit(1)

    for data in fdict.values():
        for line in data:
            data_list.append(line.rstrip())

    return data_list


def append_data(data_list, file_name):
    """Itterates over the objects in data_list and appends them to the file_name. Both the
    data_list and file_name is returned from the function as tuple two. """
    with open(file_name, 'a') as outf:
        for data in data_list:
            outf.write('{0}\n'.format(data))

    return data_list, file_name


def write_data(data_list, file_name):
    """Itterates over the objects in data_list and writes them to the file_name. This will
    overwrite any existing file with the same name. Both the data_list and file_name is
    returned from the function as a tuple two."""
    with open(file_name, 'w') as outf:
        for data in data_list:
            outf.write('{0}\n'.format(data))

    return data_list, file_name


def print_fname_data(fdict):
    """DEBUGGING FUNCTION
    Receives a dictionary where the key contains the file name and the value holds a list
    containing the data of that file. The function will first print the name of the file
    folowed by  the data as it was represented within the file. This function does not 
    return anything upon completing its execution. """
    for key, data in file_data.items():
        print(fname)
        for line in data:
            print(line.rstrip())
