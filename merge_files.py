#!/usr/bin/env python

import os
import sys
import collections

def find_files(directory):
    """
    List all the files from a given directory
    """

    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(os.getcwd(),f)) and os.path.join(os.getcwd(), f).endswith('.blast'):
            yield os.path.join(os.getcwd(), f)


def merge_files(experiment_name, directory_to_save = '~/'):
    """
    Given a list of files where position\treads\nposition\treads...n
    Returns a merged file containing the position and the reads, if the position between two files
    is the same, sums the reads.
    """

    results_dic = {}

    # Open the files iteratively and load the dictionary with the key = position, value = reads
    for fil in find_files('.'):
        with open(fil, 'r') as filehandle:
            for line in filehandle:
                line = line.strip().split()
                position = int(line[8])
                if position in results_dic:
                    results_dic[position] += 1
                else:
                    results_dic[position] = 1

    # Export to a file:
    fo = open(directory_to_save+experiment_name+'.ins', 'w')

    od = collections.OrderedDict(sorted(results_dic.items()))
    for k, v in od.iteritems():
        fo.write(str(k)+'\t'+str(v)+'\n')
    fo.close()


if __name__ == '__main__':

    merge_files(sys.argv[1])
