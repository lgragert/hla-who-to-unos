#! bin/python

import os, re, pandas, xlsxwriter

antigen_filename = "UNOS_antigens_to_alleles.csv"
antigen_file = open(antigen_filename, 'r')


a_locus = {}
b_locus = {}
c_locus = {}
dr_locus = {}
dr345_locus = {}
dqa_locus = {}
dqb_locus = {}



writer = pandas.ExcelWriter('UNOS_antigens_to_alleles.xlsx', engine='xlsxwriter')


for row in antigen_file:
	if row.startswith("UNOS_Antigen"):
		continue
	else:
		row = row.strip("\n")
		antigen = row.split(",")[0]
		alleles_list = row.split(",")[1:]
		alleles_list = "| ".join(alleles_list)

		if row.startswith("A"):
			a_locus[antigen] = alleles_list

		elif row.startswith("B"):
			b_locus[antigen] = alleles_list

		elif row.startswith("C"):
			c_locus[antigen] = alleles_list

		elif (re.findall("DR51", antigen) or re.findall("DR52", antigen) or re.findall("DR53", antigen)):
			dr345_locus[antigen] = alleles_list

		elif re.findall("DR", antigen):
			dr_locus[antigen] = alleles_list

		elif re.findall("DQA", antigen):
			dqa_locus[antigen] = alleles_list

		

		else:
			dqb_locus[antigen] = alleles_list


dict_list = [a_locus, b_locus, c_locus, dr_locus, dr345_locus, dqa_locus, dqb_locus]
sheet_names = ["A", "B", "C", "DRB1", "DRB345", "DQA1", "DQB1"]


for dictionary in dict_list:
	df = pandas.DataFrame.from_dict(dictionary, orient='index')
	df.index.name = "UNOS Antigen"
	
	
	
	df.columns = ["IMGT/HLA allele"]
	
	#df = df.rename(columns=lambda x: x.replace(str(), "IMGT/HLA allele"))

	if dictionary == a_locus:
		sheetn = "A"
	if dictionary == b_locus:
		sheetn = "B"	

	if dictionary == c_locus:
		sheetn = "C"
	if dictionary == dr_locus:
		sheetn = "DRB1"	
	if dictionary == dqb_locus:
		sheetn = "DQB1"		
	if dictionary == dr345_locus:
		sheetn = "DRB345"
	if dictionary == dqa_locus:
		sheetn = "DQA1"	

		
	df.to_excel(writer, sheet_name = sheetn)	


workbook = writer.book
format1 = workbook.add_format({'align': 'left', 'text_wrap': True})
format2 = workbook.add_format({'align': 'center'})

minus_sheet_names = ["A", "B", "C", "DRB1", "DRB345", "DQB1"]

for sheet in minus_sheet_names:
	
	ws = writer.sheets[sheet]
	ws.set_column('A:A', 20, format1)
	ws.set_column('B:B', 400, format1)
	#ws.set_column('I:I', 30, format1)
	#ws.add_format({'align': 'left'})

#

wsdqa = writer.sheets["DQA1"]
wsdqa.set_column('A:A', 20, format2)
wsdqa.set_column('B:B', 40, format2)
#worksheet = writer.sheets['A']
#header = workbook.add_format({'bold': True})
#index = workbook.add_format({'align': "left"})


#worksheet.set_row(0, None, header)
#worksheet.set_column(0,0, None, index)



writer.save()

