#!/usr/bin/env python
"""
Parse ChEMBL->PubChem ID map.
"""

__author__ = "Steven Kearnes"
__copyright__ = "Copyright 2014, Stanford University"
__license__ = "3-clause BSD"

import argparse
import cPickle
import gzip


def get_args():
    """
    Get command-line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input filename.')
    parser.add_argument('output', help='Output filename.')
    return parser.parse_args()


def main(args):
    """
    Parse ChEMBL->PubChem ID map.

    Parameters
    ----------
    args : Argparse.Namespace
        Argparse arguments.
    """
    mapping = {}
    missing = []

    # parse ID map
    if args.input.endswith('.gz'):
        f = gzip.open(args.input)
    else:
        f = open(args.input)
    for line in f:
        if line.startswith('SID'):
            fields = line.split()
            field_dict = {fields[i]: fields[i+1]
                          for i in xrange(0, len(fields)-1, 2)}
            try:
                mapping[field_dict['ChEMBL:']] = int(field_dict['CID:'])
            except KeyError:
                missing.append(field_dict['ChEMBL:'])
    f.close()
    print len(mapping), 'matched records'
    print len(missing), 'unmatched records'

    # save to pickle
    if args.output.endswith('.gz'):
        f = gzip.open(args.output, 'wb')
    else:
        f = open(args.output, 'wb')
    cPickle.dump({'mapping': mapping, 'missing': missing}, f,
                 cPickle.HIGHEST_PROTOCOL)
    f.close()

if __name__ == '__main__':
    main(get_args())
