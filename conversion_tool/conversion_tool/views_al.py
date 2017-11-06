from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import hla
import conversion_functions
from conversion_functions import convert_allele_to_ag, convert_allele_list_to_ags
from hla import allele_truncate
from . import serializers

class AlleleListApiView(APIView):
    """Returns antigen for an allele"""
    serializer_class = serializers.AlleleListSerializer
    def get(self, response, format=None):
        obj = ["UNOS antigen mapping for WHO HLA alleles"]
        return Response({'Web Services': obj})

    def post(self, request):
        """Returns UNOS antigen for an allele."""
        serializer = serializers.AlleleListSerializer(data=request.data)    

        if serializer.is_valid():
            allele_list = serializer.data.get('allele_list')
            allele_split = allele_list.split(" ")
            output = conversion_functions.convert_allele_list_to_ags(allele_split)
            ag_list = output[0]
            bw46_list = output[1]
            return Response({'Allele List': allele_list, 'Antigens': ag_list, 'Bw4/6': bw46_list})
        else:
            return Response({"Error": "Check if allele is IMGT/HLA"})
                #serializer.errors, status=status.HTTP_400_BAD_REQUEST)    