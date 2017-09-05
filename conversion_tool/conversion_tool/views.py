from django.http import HttpResponse
from django.shortcuts import render
import hla
from hla import allele_truncate
from hla import locus_string_geno_list
import conversion_functions
from conversion_functions import convert_allele_to_ag, convert_allele_list_to_ags, gl_string_ags, genotype_ags, allele_code_ags

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
    return render(request, 'convert_2.html', {'uinput': allele_list, 
    'conversion': ag_list, 'bw4_6': bw46_list})
    
    
def convert_3(request):
    uinput_1 = request.GET['userinput1']
    uinput_2 = request.GET['userinput2']
    output = gl_string_ags(uinput_1, uinput_2)
    ag_list = output[0::3]
    bw46_list = output[1::3]
    probs = output[2::3]
    return render(request, 'convert_3.html', {'uinput_1': uinput_1, 'uinput_2': uinput_2,
    'conversion': ag_list, 'bw4_6': bw46_list, 'ag_probs': probs})
        
def convert_4(request):
    uinput_1 = request.GET['userinput1']
    allele_codes_list = uinput_1.split(" ")
    uinput_2 = request.GET['userinput2']
    output = allele_code_ags(allele_codes_list, uinput_2)
    ag_list = output[0::3]
    bw46_list = output[1::3]
    probs = output[2::3]
    return render(request, 'convert_4.html', {'uinput_1': allele_codes_list, 'uinput_2': uinput_2, 
    'ag_display': ag_list,'bw4_6': bw46_list, 'ag_probs': probs })

