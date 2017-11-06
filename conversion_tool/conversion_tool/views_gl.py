from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import hla
import conversion_functions
from conversion_functions import convert_allele_to_ag, convert_allele_list_to_ags, gl_string_ags, allele_code_ags
from hla import allele_truncate
from . import serializers

class GLstringApiView(APIView):
    """Returns antigen for an allele"""
    serializer_class = serializers.GlstringSerializer
    def get(self, response, format=None):
        obj = ["UNOS antigen mapping for WHO HLA alleles"]
        return Response({'Web Services': obj})

    def post(self, request):
        """Returns UNOS antigen for an allele."""
        serializer = serializers.GlstringSerializer(data=request.data)    

        if serializer.is_valid():
            gl_string = serializer.data.get('gl_string')
            population = serializer.data.get('pop')
            
            output = conversion_functions.gl_string_ags(gl_string, population)
            ags = output[0::3]
            bw4_6_list = output[1::3]
            probs = output[2::3]

            return Response({'Genotype List string': gl_string, 'Race': population, 'Antigens': ags, 'Bw4/6': bw4_6_list, 'Antigen Probabilties': probs})
        else:
            return Response({"Error": "Check if allele is IMGT/HLA"})
                #serializer.errors, status=status.HTTP_400_BAD_REQUEST)    