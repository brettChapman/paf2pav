#!/usr/bin/python3

import os, sys
import math
import pandas as pd
import numpy as np
import copy
import glob

from optparse import OptionParser

def main():

    parser = OptionParser()
    parser.add_option("-i", "--PAVIN", help = "Multiple PAV file inputs as string using wild-card (e.g. \"*.tsv\") (required)")
    parser.add_option("-o", "--PAVOUT", help = "Merged PAV file output [default: merged_pangenome_pav_matrix.tsv]")
    (options, args) = parser.parse_args()

    if not options.PAVIN:
        print("No PAV files found!")
        parser.print_help()
    else:
        pavin_file = options.PAVIN
        pavout_file = options.PAVOUT

        all_files = sorted(glob.glob(pavin_file))

        columns = pd.read_csv(all_files[0], sep='\t').columns
        pav_list = []
        for filename in all_files:
            df = pd.read_csv(filename, sep='\t')[columns]
            pav_list.append(df)

        pangenome_pav_matrix = pd.concat(pav_list, axis=0, ignore_index=True)

        #filter pav matrix to retain regions where there is at least 1 presence, not all abscent
        col = pangenome_pav_matrix.columns[6:]
        matrix_right = pangenome_pav_matrix[col]

        col = pangenome_pav_matrix.columns[:6]
        matrix_left = pangenome_pav_matrix[col]

        matrix_right = matrix_right[matrix_right == 1].dropna(how='all').fillna(0).astype(int)

        pangenome_pav_matrix = pd.merge(matrix_left, matrix_right, how = 'inner', right_index = True, left_index = True)
        
        if pavout_file:
            pangenome_pav_matrix.to_csv(pavout_file, sep='\t', index=False, header=True)
        else:
            pangenome_pav_matrix.to_csv('merged_pangenome_pav_matrix.tsv', sep='\t', index=False, header=True)

if __name__ == "__main__":
    main()
