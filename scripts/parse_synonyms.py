#!/usr/bin/env python
"""
Parse ChEMBL->PubChem ID map.

The map is available at
ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-Synonym-filtered.gz.
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
    parser.add_argument('-i', '--input', required=1,
                        help='Input filename.')
    parser.add_argument('-s', '--source', required=1,
                        help='Source to map to PubChem CIDs.')
    parser.add_argument('-o', '--output', required=1,
                        help='Output filename.')
    return parser.parse_args()


def main(args):
    """
    Parse ChEMBL->PubChem ID map.

    Parameters
    ----------
    args : Argparse.Namespace
        Argparse arguments.
    """
    mapping = read_mapping(args.input, args.source)
    print len(mapping), 'records'

    # save to pickle
    if args.output.endswith('.gz'):
        f = gzip.open(args.output, 'wb')
    else:
        f = open(args.output, 'wb')
    cPickle.dump(mapping, f, cPickle.HIGHEST_PROTOCOL)
    f.close()


def read_mapping(filename, source):
    """
    Read ID map.

    Parameters
    ----------
    filename : str
        Map filename.
    source : str
        Source to map to CIDs.
    """
    mapping = {}
    if filename.endswith('.gz'):
        f = gzip.open(filename)
    else:
        f = open(filename)
    for line in f:
        cid, other = line.split('\t')
        if other.startswith(source):
            if other in mapping:
                if not isinstance(mapping[other], list):
                    mapping[other] = [mapping[other]]
                mapping[other].append(cid)
            else:
                mapping[other] = cid
    f.close()
    return mapping

if __name__ == '__main__':
    main(get_args())
