from django.http import HttpResponse
from django.shortcuts import render
import hla
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
    output = convert_allele_to_ag(uinput)
    ag_eq = output[0]
    bw4_6 = output[1]

    return render(request, 'convert.html', {'uinput': uinput, 'conversion': ag_eq, 'bw4_6': bw4_6})   

def convert_2(request):
    uinput = request.GET['userinput']
    allele_list = uinput.split(" ")
    output = convert_allele_list_to_ags(allele_list)
    ag_list = output[0]
    bw46_list = output[1]
    return render(request, 'convert_2.html', {'zipped_list': zip(allele_list, ag_list, bw46_list)})
    
    
def convert_3(request):
    uinput_1 = request.GET['userinput1']
    uinput_2 = request.GET['userinput2']
    output = gl_string_ags(uinput_1, uinput_2)
    ag_list = output[0::3]
    bw46_list = output[1::3]
    probs = output[2::3]
    print(probs)
    c = type(ag_list)
    #print(c)
    gl_entry = uinput_1.split("^")
    pop_selected = pop_acro_dict[uinput_2]
    return render(request, 'convert_3.html', {'pop_entry' : pop_selected, 'gl_zipped_list': zip(gl_entry, ag_list, bw46_list, probs)})
        
def convert_4(request):
    uinput_1 = request.GET['userinput1']
    allele_codes_list = uinput_1.split(" ")
    it = iter(allele_codes_list)
    mac_list = [(x, next(it)) for x in it]
    uinput_2 = request.GET['userinput2']
    output = allele_code_ags(allele_codes_list, uinput_2)
    ag_list = output[0::3]
    bw46_list = output[1::3]
    probs = output[2::3]
    pop_selected = pop_acro_dict[uinput_2]
    return render(request, 'convert_4.html', {'pop_entry' : pop_selected , 'al_code_zipped_list': zip(mac_list, ag_list, bw46_list, probs)})

