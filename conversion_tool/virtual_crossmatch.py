#! usr/bin/python


import os, re
import requests
import hla 
import itertools
from hla import allele_truncate, locus_string_geno_list, expand_ac, single_locus_allele_codes_genotype

import conversion_functions_for_VXM
from conversion_functions_for_VXM import  gl_string_ags, genotype_ags, allele_code_ags


UA_eq_dict = {}



UNOS_UA_eq_filename = "UNOS_UA_ag_equivalencies.csv"
UNOS_UA_eq_file = open(UNOS_UA_eq_filename, 'r')

for row in UNOS_UA_eq_file:
	if row.startswith("Antigen"):
		continue
	else:
		row = row.strip("\n")
		row_split = row.split(",")
		ua_ag = row_split[0]
		ua_ag_eqs = row_split[1:]
		ua_ag_eqs = list(filter(None, ua_ag_eqs))
		UA_eq_dict[ua_ag] = ua_ag_eqs
#print(UA_eq_dict)

def vxm_gls(donor_gl_string, donor_ethnicity, recipient_UA_list):
	conflicts = []
	ag_probs = {}
	donor_ags = []
	output = gl_string_ags(donor_gl_string, donor_ethnicity)
	for i in output:
		ag_list = i[0].split("+")
		for j in ag_list:
			if j in ag_probs.keys():
				ag_probs[j] += i[1]
			else:
				ag_probs[j] = i[1]
	print(ag_probs)

	for k in ag_probs.keys():
		donor_ags.append(k)

	UA_list = []
	for ag in recipient_UA_list:
		if ag in UA_eq_dict.keys():
			UA_list.append(UA_eq_dict[ag])
		else:
			UA_list.append([ag])	


	recepient_ags = [item for sublist in UA_list for item in sublist]



	for ag in donor_ags:
		if ag in recepient_ags:
			conflicts.append(ag)
		
	conflict_ag_probs = {}

	for i in conflicts:
		conflict_ag_probs[i] = ag_probs[i]


	for i,j in conflict_ag_probs.items():
		if j > 1.00:
			j = 1.00
			conflict_ag_probs[i] = j

	print(conflict_ag_probs)


	return(donor_ags, recepient_ags, conflicts, conflict_ag_probs)








def vxm_allele_codes(allele_codes_list, donor_ethnicity, recepient_UA_list):
	conflicts = []
	ag_probs = {}
	donor_ags = []
	output = allele_code_ags(allele_codes_list, donor_ethnicity)
	for i in output:
		ag_list = i[0].split("+")
		for j in ag_list:
			if j in ag_probs.keys():
				ag_probs[j] += i[1]
			else:
				ag_probs[j] = i[1]
	print(ag_probs)

	for k in ag_probs.keys():
		donor_ags.append(k)

	UA_list = []
	for ag in recepient_UA_list:
		if ag in UA_eq_dict.keys():
			UA_list.append(UA_eq_dict[ag])
		else:
			UA_list.append([ag])	


	recepient_ags = [item for sublist in UA_list for item in sublist]



	for ag in donor_ags:
		if ag in recepient_ags:
			conflicts.append(ag)
		
	conflict_ag_probs = {}

	for i in conflicts:
		conflict_ag_probs[i] = ag_probs[i]


	for i,j in conflict_ag_probs.items():
		if j > 1.00:
			j = 1.00
			conflict_ag_probs[i] = j

	print(conflict_ag_probs)


	return(donor_ags, recepient_ags, conflicts, conflict_ag_probs)





