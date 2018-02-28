#! usr/bin/python 

import os
import re
import requests   
import operator
import glob
import hla
from hla import allele_truncate, locus_string_geno_list, expand_ac, single_locus_allele_codes_genotype

ag_to_allele_dict = {}

UNOS_conversion_table_filename = "conversion_table.csv"
UNOS_conversion_table_file = open(UNOS_conversion_table_filename, 'r')
for row in UNOS_conversion_table_file:
	expression_character = ""
	if row.startswith("Allele"):
		continue 
	else:
		allele = row.split(',')[0]
		allele_4d = hla.allele_truncate(allele)
		antigen = row.split(',')[1]
		rule = row.split(',') [2]
		bw4_6 = row.split(',')[3]
		
		if antigen in ag_to_allele_dict.keys():
			if allele_4d in ag_to_allele_dict[antigen]:
				continue
			else:	

				ag_to_allele_dict[antigen].append(allele_4d)

		else:
			ag_to_allele_dict[antigen] = [allele_4d]	 


#print(ag_to_allele_dict)



def map_single_ag_to_alleles(antigen):
	if antigen in ag_to_allele_dict:
		allele_list = ag_to_allele_dict[antigen]

	return allele_list 	





