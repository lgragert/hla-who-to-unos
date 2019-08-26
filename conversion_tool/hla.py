import os

import re
import requests
import operator




def allele_truncate(allele):
	expression_character = ""
	if (allele.endswith("N")) or (allele.endswith("L")) or (allele.endswith("Q")) or (allele.endswith("S")):
		expression_character = allele[-1]
	allele_fields = allele.split(':')
	allele_group = allele_fields[0]
	protein_ind = allele_fields[1]
	if protein_ind.endswith("L") or protein_ind.endswith("Q") or protein_ind.endswith("S") or protein_ind.endswith("N"): 
		protein_ind = re.sub('[LQNS]', "", protein_ind)
	if expression_character:
		allele_t = allele_group + ":" + protein_ind + expression_character
	else:
		allele_t = allele_group + ":" + protein_ind 
	return allele_t	



def locus_string_geno_list(locus_string):
	genotype_list = []

	genotype_pipe_list = locus_string.split("|")
	for genotype in genotype_pipe_list:
		allele_list = genotype.split("+")
		allele_list1 = allele_list[0].split("/")
		allele_list2 = allele_list[1].split("/")
		for allele1 in allele_list1:
			for allele2 in allele_list2:
				genotype = allele1 + "+" + allele2
				genotype_list.append(genotype)		

	return genotype_list






def expand_ac(allele_code):
	url = "https://hml.nmdp.org/mac/api/decode?imgtHlaRelease=3.37.0&typing="
	response = requests.get(url + allele_code)
	return(response.text)




def single_locus_allele_codes_genotype(allele_code_pair_list):
    genotype_list = []
    MAC_1 = allele_code_pair_list[0]
    MAC_2 = allele_code_pair_list[1]

    MAC_1_locus = MAC_1.split("*")[0]
    MAC_2_locus = MAC_2.split("*")[0]

    if MAC_1_locus == MAC_2_locus:
        MAC_1_expanded = expand_ac(MAC_1)
        MAC_1_expanded_split = MAC_1_expanded.split("/")
        MAC_2_expanded = expand_ac(MAC_2)
        MAC_2_expanded_split = MAC_2_expanded.split("/")
        
        for i in MAC_1_expanded_split:
            for j in MAC_2_expanded_split:
                genotype = i + "+" + j
                genotype_list.append(genotype)
        return genotype_list

    else:

        print("Allele codes should be from same locus")    


	
