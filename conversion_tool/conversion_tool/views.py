from django.http import HttpResponse
from django.shortcuts import render
import hla
import re
from hla import allele_truncate
from hla import locus_string_geno_list
import conversion_functions
from conversion_functions import convert_allele_to_ag, convert_allele_list_to_ags, gl_string_ags, genotype_ags, allele_code_ags



pop_acro_dict = {"AFA": "African American", "API": "Asia/Pacific Islander", "CAU": "Caucasian", "HIS": "Hispanic", 
"NAM": "Native American", "AAFA": "African American", "AFB": "African Black",  "AINDI": "South Asian Indian", 
"AISC": "American Indian-South or Central American", "ALANAM": "Alaska Native", "AMIND": "North American Indian", 
"CARB": "Caribbean Black", "CARHIS": "Caribbean Hispanic", "CARIBI": "Caribbean Indian", "EURACU": "European Caucasian", 
"FILII": "Filipino", "HAWI": "Hawaiian or Pacific Islander", "JAPI": "Japanese", "KORI": "Korean", 
"MENAFC": "Middle Eastern or N. Coast of Africa", "MSWHIS": "Mexican or Chicano HIS", "NCHI": "Chinese", 
"SCAHIS": "South or Central AMerican Hispanic", "SCAMB": "South or Central American Black", 
"SCSEAI": "South East Asian", "VIET": "Vietnamese"}









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


def convert(request):
    uinput = request.GET['userinput']
    uinput = uinput.strip() 
    output = convert_allele_to_ag(uinput)
    ag_eq = output[0]
    bw4_6 = output[1]

    return render(request, 'convert.html', {'uinput': uinput, 'conversion': ag_eq, 'bw4_6': bw4_6})   

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
    edited_probs = []
    for prob in probs:
        prob_string = str(prob)
        x = type(prob_string)
        prob2 = re.sub('[(\)''[\]]', '', prob_string)
        edited_probs.append(prob2)

    locus_list = []
    gl_entry = uinput_1.split("^")
    for i in gl_entry:
        locus = i.split("*")[0]
        locus_list.append(locus)

    
    pop_selected = pop_acro_dict[uinput_2]
    return render(request, 'convert_3.html', {'pop_entry' : pop_selected, 
        'gl_zipped_list': zip(locus_list, gl_entry, ag_list, bw46_list, edited_probs),
        'ags_returned': ageps_mapped})
        



def convert_4(request):
    uinput_1 = request.GET['userinput1']
    uinput_1 = uinput_1.strip()
    allele_codes_list = re.split(r'[;,\s]\s*' , uinput_1)
    allele_codes_list = sorted(allele_codes_list)
    it = iter(allele_codes_list)
    mac_list = [(x, next(it)) for x in it]
    print(mac_list)
    uinput_2 = request.GET['userinput2']
    output = allele_code_ags(allele_codes_list, uinput_2)
    ag_list = output[0::3]
    bw46_list = output[1::3]
    ageps_mapped = ag_list + bw46_list


    ageps_mapped = ' '.join(ageps_mapped)
    ageps_mapped = ageps_mapped.replace(',', ' ')
    ageps_mapped = ageps_mapped.replace("NA", "")
    ageps_mapped = re.sub('\s+', ", ", ageps_mapped)
    ageps_mapped = ageps_mapped.rstrip(", ")

    probs = output[2::3]
    edited_probs = []
    for prob in probs:
        prob_string = str(prob)
        x = type(prob_string)
        prob2 = re.sub('[(\)''[\]]', '', prob_string)
        edited_probs.append(prob2)

    locus_list = []
    
    for i in mac_list:
        locus = i[0].split("*")[0]
        locus_list.append(locus)

        
    pop_selected = pop_acro_dict[uinput_2]
    return render(request, 'convert_4.html', {'pop_entry' : pop_selected, 
        'al_code_zipped_list': zip(locus_list, mac_list, ag_list, bw46_list, edited_probs),
        'ags_returned': ageps_mapped})

