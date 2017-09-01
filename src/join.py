#!/usr/bin/env python
# -*- coding: utf-8 -*-

##    Description    Inner Join of two CSV tables
##                   
##    Authors:       Inés Martínez (mmartinez4@imim.es)
##                   Manuel Pastor (manuel.pastor@upf.edu)
##
##    Copyright 2015 Manuel Pastor
##
##    This file is part of PhiTools
##
##    PhiTools is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 3.
##
##    PhiTools is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with PhiTools.  If not, see <http://www.gnu.org/licenses/>

import os, sys, argparse

sep = '\t'

def join (args):

    # Open files
    if args.type == 'right':
        fa = args.fileb
        fb = args.filea     
    else:   
        # Left, inner or outer join
        fa = args.filea
        fb = args.fileb 

    # Identify key in both files
    ha = fa.readline().decode("utf-8").rstrip().split(sep)
    nfieldsA = len(ha)
    try:
        indexA = ha.index(args.key)
    except:
        sys.stderr.write('Key not fount in file {}\n'.format(fa.name))
        sys.exit(1)

    hb = fb.readline().decode("utf-8").rstrip().split(sep)
    nfieldsB = len(hb)
    try:
        indexB = hb.index(args.key)
    except:
        sys.stderr.write('Key not fount in file {}\n'.format(fb.name))
        sys.exit(1)

    # Write header in the output file
    header = ha[:]
    tmp = hb[:]
    del tmp[indexB]
    header.extend(tmp)
    args.out.write('{}\n'.format(sep.join(header)))

    # Read the second file in memory and index key
    vIndex = {}
    for line in fb:
        linelist = line.decode("utf-8").rstrip().split(sep)
        if len(linelist) < nfieldsB:
            for i in range(len(linelist), nfieldsB):
                linelist.append('')
        
        if args.soft: key = linelist[indexB][:-3]
        else: key = linelist[indexB]
        
        lineraw = []
        for i in range(len(hb)):
            if i >= len(linelist):
                value = ''
            else:
                value = linelist[i]

            if i!=indexB:
                lineraw.append(value)
        vIndex[key] = lineraw
    fb.close()
    
    # Read the first file
    for line in fa:
        line = line.decode("utf-8").rstrip()
        linelist = line.split(sep)
        if len(linelist) < nfieldsA:
            for i in range(len(linelist), nfieldsA):
                linelist.append('')
                
        key = linelist[indexA]
        if args.soft: k = k[:-3]
        if key not in vIndex.keys():
            if args.type != 'inner':
                args.out.write('{}\n'.format(sep.join([line, ''])))
            continue

        linelist.extend(vIndex[key])
        
        args.out.write('{}\n'.format(sep.join(linelist)))
    fa.close()

    if args.type == 'outer':
        for key in vIndex:
            # For lines in B that weren't found in A fill in the fields corresponding to the first file's header.
            line = sep.join(['' if i != indexA else key for i in range(len(ha))])
            args.out.write('{}\n'.format(sep.join([line, vIndex[key]])))

    args.out.close()

def main ():

    parser = argparse.ArgumentParser(description='Joins the two input files using the column label indicated as a key. The --soft parameter is used when InChiKey-based comparisons are performed, discarding the last 3 chars. By default it performs a left join, but you can also chose right, inner, or outer join.')
    parser.add_argument('-a', '--filea', type=argparse.FileType('rb'), help='First file to join.', required=True)
    parser.add_argument('-b', '--fileb', type=argparse.FileType('rb'), help='Second file to join.', required=True)
    parser.add_argument('-f', '--field', type=str, dest='key', help='Name of the field to be used as a common key.', required=True)
    parser.add_argument('-s', '--soft', action='store_true', help='When InChiKey based comparisons are performed, discard the last 3 chars.')
    parser.add_argument('-t', '--type', action='store', choices=['left', 'right', 'inner', 'outer'], default='left', help='Join type (\'left\', default), \'right\', \'inner\', or \'outer\'')
    parser.add_argument('-o', '--out', type=argparse.FileType('w'), default='output.tsv', help='Output file name (default: output.tsv)')
    args = parser.parse_args()

    join (args)

if __name__ == '__main__':    
    main()
