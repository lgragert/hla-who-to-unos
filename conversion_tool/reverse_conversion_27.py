#! usr/bin/python 

import os
import re
import requests   
import hla
from hla import allele_truncate

ag_to_allele_dict = {}
UA_eq_dict = {'A1': [' A1'], 'A2': ['A2', 'A0203'], 'A3': ['A3'], 'A9': ['A9', 'A23', 'A24', 'A2403'], 
'A10': ['A10', 'A25', 'A26', 'A34', 'A66', 'A*6601', 'A*6602', 'A43'], 'A11': ['A11'], 
'A19': ['A19', 'A29', 'A30', 'A31', 'A32', 'A33', 'A74'], 'A23': ['A23'], 'A24': ['A24'], 
'A25': ['A25'], 'A26': ['A26'], 'A28': ['A28', 'A68', 'A69'], 'A29': ['A29'], 'A30': ['A30'], 
'A31': ['A31'], 'A32': ['A32'], 'A33': ['A33'], 'A34': ['A34'], 'A36': ['A36'], 'A43': ['A43'], 
'A66': ['A66', 'A*6601', 'A*6602'], 'A68': ['A68'], 'A69': ['A69'], 'A74': ['A74'], 'A80': ['A80'], 
'A0203': ['A0203'], 'A2403': ['A2403'], 'A*6601': ['A*6601', 'A66'], 'A*6602': ['A*6602', 'A66'], 
'B5': ['B5', 'B51', 'B52', 'B78'], 'B7': ['B7'], 'B8': ['B8'], 'B12': ['B12', 'B44', 'B45'], 
'B13': ['B13'], 'B14': ['B14', 'B64', 'B65'], 'B15': ['B15', 'B62', 'B63', 'B75', 'B76', 'B77'], 
'B16': ['B16', 'B38', 'B39'], 'B17': ['B17', 'B57', 'B58'], 'B18': ['B18'], 'B21': ['B21', 'B49', 'B50', 'B4005'], 
'B22': ['B22', 'B54', 'B55', 'B56'], 'B27': ['B27'], 'B35': ['B35'], 'B37': ['B37'], 'B38': ['B38'], 'B39': ['B39', 'B3901', 'B3902', 'B*3905'], 
'B40': ['B40', 'B60', 'B61'], 'B41': ['B41'], 'B42': ['B42'], 'B44': ['B44'], 'B45': ['B45'], 'B46': ['B46'], 'B47': ['B47'], 'B48': ['B48'], 
'B49': ['B49'], 'B50': ['B50', 'B4005'], 'B51': ['B51'], 'B52': ['B52'], 'B53': ['B53'], 'B54': ['B54'], 'B55': ['B55'], 'B56': ['B56'], 
'B57': ['B57'], 'B58': ['B58'], 'B59': ['B59'], 'B60': ['B60'], 'B61': ['B61'], 'B62': ['B62'], 'B63': ['B63'], 'B64': ['B64'], 
'B65': ['B65'], 'B67': ['B67'], 'B70': ['B70', 'B71', 'B72'], 'B71': ['B71'], 'B72': ['B72'], 'B73': ['B73'], 'B75': ['B75'], 'B76': ['B76'], 
'B77': ['B77'], 'B78': ['B78'], 'B81': ['B81'], 'B82': ['B82', 'B*8201'], 'B*0804': ['B*0804'], 'B*1304': ['B*1304'], 'B2708': ['B2708'], 
'B3901': ['B3901'], 'B3902': ['B3902'], 'B*3905': ['B*3905'], 'B4005': ['B4005', 'B50'], 'B5102': ['B5102'], 'B7801': ['B7801', 'B78'], 
'B*8201': ['B*8201', 'B82'], 'DR1': ['DR1'], 'DR2': ['DR2', 'DR15', 'DR16'], 'DR3': ['DR3', 'DR17', 'DR18'], 'DR4': ['DR4'], 
'DR5': ['DR5', 'DR11', 'DR12'], 'DR6': ['DR6', 'DR13', 'DR14', 'DR1403', 'DR1404'], 'DR7': ['DR7'], 'DR8': ['DR8'], 'DR9': ['DR9'], 
'DR10': ['DR10'], 'DR11': ['DR11'], 'DR12': ['DR12'], 'DR13': ['DR13'], 'DR14': ['DR14', 'DR1403', 'DR1404'], 
'DR15': ['DR15'], 'DR16': ['DR16'], 'DR17': ['DR17'], 'DR18': ['DR18'], 'DR103': ['DR103'], 'DR1403': ['DR1403'], 
'DR1404': ['DR1404'], 'DR51': ['DR51'], 'DR52': ['DR52'], 'DR53': ['DR53'], 'C01': ['C01'], 'C02': ['C02'], 
'C03': ['C03', 'C09', 'C10'], 'C04': ['C04'], 'C05': ['C05'], 'C06': ['C06'], 'C07': ['C07'], 'C08': ['C08'], 
'C09': ['C09'], 'C10': ['C10'], 'C12': ['C12'], 'C14': ['C14'], 'C15': ['C15'], 'C16': ['C16'], 'C17': ['C17'], 'C18': ['C18'], 
'DQ1': ['DQ1', 'DQ5', 'DQ6'], 'DQ2': ['DQ2'], 'DQ3': ['DQ3', 'DQ7', 'DQ8', 'DQ9'], 'DQ4': ['DQ4'], 'DQ5': ['DQ5', 'DQ1'], 
'DQ6': ['DQ6', 'DQ1'], 'DQ7': ['DQ7', 'DQ3'], 'DQ8': ['DQ8', 'DQ3'], 'DQ9': ['DQ9', 'DQ3']}



#UNOS_UA_eq_filename = "UNOS_4-10_ag_equivalencies.csv"
#UNOS_UA_eq_file = open(UNOS_UA_eq_filename, 'r')


#for row in UNOS_UA_eq_file:
	#print row
	#if row.startswith("Antigen"):
		#continue
	#else:
		#row = row.strip("\n")
		#row_split = row.split(",")
		#ua_ag = row_split[0]
		#ua_ag_eqs = row_split[1:]
		#ua_ag_eqs = list(filter(None, ua_ag_eqs))
		#UA_eq_dict[ua_ag] = ua_ag_eqs


UNOS_conversion_table_filename = "conversion_table.csv"
UNOS_conversion_table_file = open(UNOS_conversion_table_filename, 'r')
for row in UNOS_conversion_table_file:
	#print row
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


#print ag_to_allele_dict

final_dict = {}
#ag_list = []

#for ag in ag_to_allele_dict.keys():
	#ag_list.append(ag)
d = {}

for ag in ag_to_allele_dict.keys():
	allele_list = []
	d = {}
	if ag in UA_eq_dict.keys():
		
		ag_eqs = UA_eq_dict[ag]
		for ages in ag_eqs:
			ages = ages.strip()
			alleles = ag_to_allele_dict[ages]
			d[ages] = [alleles]


			#allele_list.append(alleles)
		
		#allele_list = [item for sublist in allele_list for item in sublist]
		#allele_list = allele_list.sort()
		#print(type(allele_list))
		final_dict[ag] = d

	else:
		final_dict[ag] = ag_to_allele_dict[ag]		
print final_dict

def map_single_ag_to_alleles(antigen):
	if antigen in final_dict:
		allele_list = final_dict[antigen]

	return allele_list 	
