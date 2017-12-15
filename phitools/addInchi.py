#!/usr/bin/env python
# -*- coding: utf-8 -*-

##    Description    Add an InChI field to a SDFile 
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

from rdkit import Chem
from rdkit.Chem import AllChem
from moleculeHelper import *
import os, sys, argparse

def addInchi (args):

    # Read SDF
    suppl = Chem.ForwardSDMolSupplier(args.sdf,removeHs=False, sanitize=False)

    # Create header    
    for mol in suppl:

        if mol is None: continue
        
        args.out.write(Chem.MolToMolBlock(mol,kekulize=False))
        writePropertiesSD(args.out, getProperties(mol))

        try:
            inchi = Chem.MolToInchi(mol)
            inkey = Chem.InchiToInchiKey(inchi)
        except:
            inchi = 'na'
            inkey = 'na'
        if inchi is None : inchi='na'
        if inkey is None : inkey='na'

        args.out.write('>  <inchi>\n'+inchi+'\n\n')
        args.out.write('>  <inchikey>\n'+inkey+'\n\n')
        args.out.write('$$$$\n')

    args.sdf.close()
    args.out.close()

def main ():
    parser = argparse.ArgumentParser(description='Add Inchi into a field for each molecule in the input SD file.')
    parser.add_argument('-f', '--sdf', type=argparse.FileType('rb'), help='SD file', required=True)
    parser.add_argument('-o', '--out', type=argparse.FileType('w'), default='output.sdf', help='Output SD file name (default: output.sdf)')
    args = parser.parse_args()

    addInchi (args)

if __name__ == '__main__':    
    main()