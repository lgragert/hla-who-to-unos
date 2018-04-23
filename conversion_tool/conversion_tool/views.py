from django.http import HttpResponse
from django.shortcuts import render
import hla
import re
from hla import allele_truncate
from hla import locus_string_geno_list
import conversion_functions
from conversion_functions import convert_allele_to_ag, convert_allele_list_to_ags, gl_string_ags, genotype_ags, allele_code_ags
import reverse_conversion
from reverse_conversion import map_single_ag_to_alleles 


pop_acro_dict = {"AFA": "African American", "API": "Asia/Pacific Islander", "CAU": "Caucasian", "HIS": "Hispanic", 
"NAM": "Native American", "AAFA": "African American", "AFB": "African Black",  "AINDI": "South Asian Indian", 
"AISC": "American Indian-South or Central American", "ALANAM": "Alaska Native", "AMIND": "North American Indian", 
"CARB": "Caribbean Black", "CARHIS": "Caribbean Hispanic", "CARIBI": "Caribbean Indian", "EURACU": "European Caucasian", 
"FILII": "Filipino", "HAWI": "Hawaiian or Pacific Islander", "JAPI": "Japanese", "KORI": "Korean", 
"MENAFC": "Middle Eastern or N. Coast of Africa", "MSWHIS": "Mexican or Chicano HIS", "NCHI": "Chinese", 
"SCAHIS": "South or Central AMerican Hispanic", "SCAMB": "South or Central American Black", 
"SCSEAI": "South East Asian", "VIET": "Vietnamese"}


IMGT_HLA_alleles = []

for i in conversion_functions.allele_to_ag_dict.keys():
    IMGT_HLA_alleles.append(i)
#print(IMGT_HLA_alleles)
def home(request):
    return render(request, 'home.html')

def home_1(request):
    return render(request, 'home_1.html')

def license(request):
    return render(request, 'license.html')    

def allele(request):
    return render(request, 'allele.html')

def allele_list(request):
    return render(request, 'allele_list.html')    

def gl_string(request):
    return render(request, 'gl_string.html')  


def allele_codes(request):
    return render(request, 'allele_codes.html')  

def reverse (request):
    return render(request, 'reverse.html')

#### SINGLE ALLELE
def convert(request):
    uinput = request.GET['userinput']
    uinput = uinput.strip() 
    valid_allele_check = IMGT_HLA_alleles
    
    if uinput in valid_allele_check:
        output = convert_allele_to_ag(uinput)
        ag_eq = output[0]
        bw4_6 = output[1]
        

        return render(request, 'convert.html', {'uinput': uinput, 'conversion': ag_eq, 'bw4_6': bw4_6})   
    else:   
        return render(request, 'allele_rejection.html')    


### LIST of ALLELES
def convert_2(request):
    uinput = request.GET['userinput']
    x = type(uinput)
    allele_list = re.split(r'[;,\s]\s*' , uinput)
    output = convert_allele_list_to_ags(allele_list)
    ag_list = output[0]
    bw46_list = output[1]
    ageps_mapped = ag_list + bw46_list
    ageps_mapped = ' '.join(ageps_mapped)
    ageps_mapped = ageps_mapped.replace(',', ' ')
    ageps_mapped = ageps_mapped.replace("NA", "")
    ageps_mapped = re.sub('\s+', ", ", ageps_mapped)
    ageps_mapped = ageps_mapped.rstrip(", ")
    
    return render(request, 'convert_2.html', {'zipped_list': zip(allele_list, ag_list, bw46_list), 'ags_returned': ageps_mapped})
    
#### GENOTYPE LIST STRINGS    
def convert_3(request):
    uinput_1 = request.GET['userinput1']
    uinput_1 = uinput_1.strip()
    uinput_2 = request.GET['userinput2']
    output = gl_string_ags(uinput_1, uinput_2)
    ag_list = output[0::3]
    bw46_list = output[1::3]
    ageps_mapped = ag_list + bw46_list


    ageps_mapped = ' '.join(ageps_mapped)
    ageps_mapped = ageps_mapped.replace(',', ' ')
    ageps_mapped = ageps_mapped.replace("NA", "")
    ageps_mapped = re.sub('\s+', ", ", ageps_mapped)
    ageps_mapped = ageps_mapped.rstrip(", ")
    
    probs = output[2::3]
    #probs = list(probs)
    #print(probs)
    #print(type(probs))
    #edited_probs = []
    #for prob in probs:
       # prob_string = str(prob)
       # x = type(prob_string)
        #prob2 = re.sub('[(\)''[\]]', '', prob_string)
        #prob2 = re.sub('[(\)]', '"', prob_string)
        #prob2 = prob2.replace("'", '')
        #print(type(prob2))
        #edited_probs.append(prob2)
    #print(type(edited_probs))
    probs_dict = {}

    for i in probs:
        for subi in i:
            ags_list = subi[0]
            pb = subi[1]
            probs_dict[ags_list] = pb

    #print(probs_dict)        

    aags = []
    bags = []
    cags = []
    drags = []
    dr345ags = []
    dqags = []

    for i,j in probs_dict.items():
        if re.findall("A", i):
            ji = str(j)
            fi = i + ": " + ji
            aags.append(fi)

        if re.findall("B", i):
            ji = str(j)
            fi = i + ": " + ji 
            bags.append(fi)


        if re.findall("C", i):
            ji = str(j)
            fi = i + ": " + ji 
            cags.append(fi)


        if (re.findall("DR51", i)) or (re.findall("DR52", i)) or (re.findall("DR53", i)):
            ji = str(j)
            fi = i + ": " + ji 
            dr345ags.append(fi)
            

        if re.findall("DQ", i):
            ji = str(j)
            fi = i + ": " + ji 
            dqags.append(fi)       

        if re.findall("DR", i):
            ji = str(j)
            fi = i + ": " + ji 
            drags.append(fi)

    finalAgs = [aags]  + [cags] + [bags] +  [drags] +  [dr345ags] +  [dqags]
    
    finalAglist = [x for x in finalAgs if x != []]
    #print(finalAglist)

    #for i in finalAgs:
       # if len(i) == 0:
           # continue
        #else:
            #finalAglist.append([i])

    #print(finalAglist)            



    #reedited_pros = "\n".join(edited_probs)
    #print(reedited_pros)
    
    locus_list = []
    gl_entry = uinput_1.split("^")
    for i in gl_entry:
        locus = i.split("*")[0]
        locus_list.append(locus)

    dummy = [["A", "B"], ["D"],  ["C"], ["A", "D", "C"], ["D"]]
    pop_selected = pop_acro_dict[uinput_2]
    return render(request, 'convert_3.html', {'pop_entry' : pop_selected, 
        'gl_zipped_list': zip(locus_list, gl_entry, ag_list, bw46_list, finalAglist, dummy),
        'ags_returned': ageps_mapped})
        

##### NMDP ALLELE CODES

def convert_4(request):
    uinput_1 = request.GET['userinput1']
    uinput_1 = uinput_1.strip()
    allele_codes_list = re.split(r'[;,\s]\s*' , uinput_1)
    allele_codes_list = sorted(allele_codes_list)
    it = iter(allele_codes_list)
    mac_list = [(x, next(it)) for x in it]
    stringy_mac_list = [ "%s %s" % x for x in mac_list ] ### changes list of tuples to list of 
    comma_stringy_mac_list = [] ### Adds commas to allele code pairs
    for i in stringy_mac_list:
        ix = ", ".join(i.split(" "))
        comma_stringy_mac_list.append(ix)

    uinput_2 = request.GET['userinput2']
    output = allele_code_ags(allele_codes_list, uinput_2)
    #print(output)
    ag_list = output[0::3]
    bw46_list = output[1::3]
    ageps_mapped = ag_list + bw46_list


    ageps_mapped = ' '.join(ageps_mapped)
    ageps_mapped = ageps_mapped.replace(',', ' ')
    ageps_mapped = ageps_mapped.replace("NA", "")
    ageps_mapped = re.sub('\s+', ", ", ageps_mapped)
    ageps_mapped = ageps_mapped.rstrip(", ")

    probs = output[2::3]
    
    probs_dict = {}

    for i in probs:
        for subi in i:
            ags_list = subi[0]
            pb = subi[1]
            probs_dict[ags_list] = pb

    #print(probs_dict)        

    aags = []
    bags = []
    cags = []
    drags = []
    dr345ags = []
    dqags = []

    for i,j in probs_dict.items():
        if re.findall("A", i):
            ji = str(j)
            fi = i + ": " + ji
            aags.append(fi)

        if re.findall("B", i):
            ji = str(j)
            fi = i + ": " + ji 
            bags.append(fi)


        if re.findall("C", i):
            ji = str(j)
            fi = i + ": " + ji 
            cags.append(fi)


        if (re.findall("DR51", i)) or (re.findall("DR52", i)) or (re.findall("DR53", i)):
            ji = str(j)
            fi = i + ": " + ji 
            dr345ags.append(fi)
            

        if re.findall("DQ", i):
            ji = str(j)
            fi = i + ": " + ji 
            dqags.append(fi)       

        if re.findall("DR", i):
            ji = str(j)
            fi = i + ": " + ji 
            drags.append(fi)

    finalAgs = [aags]  + [cags] + [bags] +  [drags] +  [dr345ags] +  [dqags]
    
    finalAglist = [x for x in finalAgs if x != []]
    #print(finalAglist)



    #edited_probs = []
    #for prob in probs:
        #prob_string = str(prob)
       # x = type(prob_string)
        #prob2 = re.sub('[(\)''[\]]', '', prob_string)
        #edited_probs.append(prob2)

    #print(edited_probs)
    #print(type(edited_probs))
    locus_list = []
    
    for i in mac_list:
        locus = i[0].split("*")[0]
        locus_list.append(locus)

        
    pop_selected = pop_acro_dict[uinput_2]
    return render(request, 'convert_4.html', {'pop_entry' : pop_selected, 
        'al_code_zipped_list': zip(locus_list, comma_stringy_mac_list, ag_list, bw46_list, finalAglist),
        'ags_returned': ageps_mapped})


### REVERSE MAPPING
def convert_5(request):
    uinput = request.GET['userinput']
    uinput = uinput.strip() 
    output = reverse_conversion.map_single_ag_to_alleles(uinput)
    #ag_list = output.split(",")
    ag_list = []
    for i in output.keys():
        ag_list.append(i)
    ags_eq = ag_list
    #print(ags_eq)
    alleles_ouput = []

    for i in output.values():
        i = [item for sublist in i for item in sublist]
        #i = ", ".join(i)
        alleles_ouput.append(i)

    #print(alleles_ouput)


    allele_list = [item for sublist in alleles_ouput for item in sublist]
    #allele_list = [item for sublist in allele_list for item in sublist]
    #print(allele_list)
    alleles_mapped = ' '.join(allele_list)
    #print(alleles_mapped)
    alleles_mapped = alleles_mapped.replace(',', ' ')
    #ageps_mapped = ageps_mapped.replace("NA", "")
    alleles_mapped = re.sub('\s+', ", ", alleles_mapped)
    alleles_mapped = alleles_mapped.rstrip(", ")


    

    return render(request, 'convert_5.html', {'uinput': uinput, 'conversion': alleles_ouput, 'alleles_returned': alleles_mapped, "ags_e": ags_eq, 
        'reverse_zipped': zip(ags_eq, alleles_ouput)}) 





