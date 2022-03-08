#!/usr/bin/python3

import os, sys
import math
import pandas as pd
import numpy as np
import copy

from optparse import OptionParser

def main():

    parser = OptionParser()
    parser.add_option("-i", "--PAF", help = "PAF file input (required)")
    parser.add_option("-o", "--PAV", help = "PAV file output [default: pangenome_pav_matrix.tsv]")
    (options, args) = parser.parse_args()

    if not options.PAF:
        print("No PAF file found!")
        parser.print_help()
    else:
        paf_file = options.PAF
        pav_file = options.PAV

        paf = pd.read_csv(paf_file, header=None, sep='\t')

        # check if there is only a single reference for the PAV matrix
        ref = np.unique(paf.loc[:, 5])

        if len(ref) == 1:
            queries = paf.loc[:, 0]
            _, query_index = np.unique(queries, return_index=True)
            genomes = list(queries[np.sort(query_index)])

            genome_array = []

            for region in paf.index:
                start = paf.loc[region, 7]
                end = paf.loc[region, 8]

                pblock_set = set(list(paf[(paf[7] == start) & (paf[8] == end)][0]))

                pangenome_block = [i for i, x in enumerate(genomes) if x in pblock_set]

                genome_pav_array = copy.deepcopy(np.zeros(len(genomes), dtype=int))
                for block in pangenome_block:
                    genome_pav_array[block] = 1

                genome_array.append(list(genome_pav_array))

            pangenome_pav_matrix = pd.DataFrame(genome_array, columns=genomes)

            pangenome_pav_matrix = pd.merge(paf, pangenome_pav_matrix, left_index=True, right_index=True)

            columns = ['#Chromosome', 'FeatureStart', 'FeatureStop', 'Sequence_IUPAC_Plus', 'SimilarBlocks', 'Function'] + genomes

            p = pangenome_pav_matrix.rename(columns={5: "#Chromosome", 7: "FeatureStart", 8: "FeatureStop"})
            p['Sequence_IUPAC_Plus'] = '.'
            p['SimilarBlocks'] = '.'
            p['Function'] = '.'

            pangenome_pav_matrix = p[columns].drop_duplicates(subset = columns).sort_values(['FeatureStart', 'FeatureStop'], ascending=[True,True]).reset_index(drop=True)

            if pav_file:
                pangenome_pav_matrix.to_csv(pav_file, sep='\t', index=False, header=True)
            else:
                pangenome_pav_matrix.to_csv('pangenome_pav_matrix.tsv', sep='\t', index=False, header=True)
        else:
            print("Error: Multi-reference PAF file provided. Please provide a PAF file containing only one reference path and multiple query paths.")

if __name__ == "__main__":
    main()
