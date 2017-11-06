import os, re, requests, ast

## ast module is used to convert string representation of dictionary to dictionary


#### functions to use the conversion services


def single_allele_map(allele):
	url = "http://transplanttoolbox.org/single_allele/"
	data = {"allele": allele}
	response = requests.post(url, data)
	return response.text

def allele_list_map(allele_list):
	url = "http://transplanttoolbox.org/array/"
	data = {"allele_list": allele_list}
	response = requests.post(url, data)
	return response.text

def gl_string_map(gl_string, pop):
	url = "http://transplanttoolbox.org/gls/"
	data = {"gl_string": gl_string, "pop": pop}
	response = requests.post(url, data)
	return response.text	

def macs_map(allele_codes_list, pop):
	url = "http://transplanttoolbox.org/macs/"
	data = {"allele_codes_list": allele_codes_list, "pop": pop}
	response = requests.post(url, data)
	return response.text




#### Illustration of using the functions defined above

### Mapping antigen for an allele
allele="B*07:02"

Unos_ag = single_allele_map(allele)
d = ast.literal_eval(Unos_ag)
ags = d["Antigen"]
print("Antigen mapping for allele")
print(allele)
print(ags)
print("\n")


#### Mapping list of alleles to UNOS antigen equivalencies

allele_list = "A*01:01 A*01:228Q B*27:96:01 DRB1*07:01"
Unos_ag = allele_list_map(allele_list)
d = ast.literal_eval(Unos_ag)
ags = d["Antigens"]
bw4_6 = d["Bw4/6"]
print("Antigen mapping for list of alleles")
print(allele_list)
print(ags)
print(bw4_6)
print("\n")
### Mapping 5 locus Genotype list string for Caucasian population to UNOS antigen equivalencies

gl_string = "A*02:01g+A*26:01g|A*02:55+A*26:07^C*05:01g+C*01:02g^B*15:01/B*15:02/B*15:03/B*15:04+B*27:05g^DRB1*12:01g+DRB1*01:01^DQB1*03:01g+DQB1*05:01"
pop = "CAU"

Unos_ag = gl_string_map(gl_string, pop)
d = ast.literal_eval(Unos_ag)
ags = d["Antigens"]
bw4_6 = d["Bw4/6"]
print("Antigen mapping for genotype list string")
print(gl_string)
print(ags)
print(bw4_6)
print("\n")

## Mapping 5 locus allele codes for African American population to UNOS antigen equivalencies

allele_codes_list = "A*01:AABJE A*02:HBMC B*08:NMTJ B*13:GR C*04:CYMD C*05:YDYE DRB1*04:AMR DRB1*07:GC DQB1*03:AG DQB1*03:AFYYJ"
pop = "AFA"

Unos_ag = macs_map(allele_codes_list, pop)
d = ast.literal_eval(Unos_ag)
ags = d["Antigens"]
bw4_6 = d["Bw4/6"]

print("Antigen mapping for allele codes")
print(allele_codes_list)
print(ags)
print(bw4_6)
print("\n")