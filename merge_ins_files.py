#!/usr/bin/env python

import os
import sys
import collections


def print_help():
    """
    Print the manual of the program
    """

    print("merge_files.py allow you to easily merge .ins files\nTo use it:>\n\npython merge_files.py <directory_to_save_output> <fileA> <fileB> <fileC> ... \n\nFor all the files:\n\npython merge_files.py <directory_to_save_output> <directory/*.ins>")


def merge_files():
    """
    Given a list of files where position\treads\nposition\treads...\n
    Returns a merged file containing the position and the reads, if the position between two files
    is the same, sums the reads.
    """

    # Ste the variables
    outFile = sys.argv[1]
    inFile  = sys.argv[2:]  # Takes the second argument and the possible ones being after it
    results_dic = {}

    # Run the general loop: Open the files iteratively and load the dictionary with the key = position, value = reads
    for fil in inFile:
        print(fil)
        with open(fil, 'r') as filehandle:
            for line in filehandle:
                line = line.strip().split()
                position = int(line[0])
                if position in results_dic:
                    results_dic[position] += int(line[1])
                else:
                    results_dic[position] = int(line[1])

    # Export to a file:
    fo = open(outFile, 'w')

    od = collections.OrderedDict(sorted(results_dic.items()))
    for k, v in od.iteritems():
        fo.write(str(k)+'\t'+str(v)+'\n')
    fo.close()


def main():
    """ Main function to run the merge_files function """

    # Evaluate arguments and if help required:
    if len(sys.argv) <= 2:
        print_help()
    else:
        merge_files()


if __name__ == '__main__':

    main()
