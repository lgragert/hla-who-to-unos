from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import hla
import conversion_functions
from conversion_functions import convert_allele_to_ag
from hla import allele_truncate
from . import serializers

class AlleleApiView(APIView):
    """Returns antigen for an allele"""
    serializer_class = serializers.AlleleSerializer
    def get(self, response, format=None):
        obj = ["UNOS antigen mapping for WHO HLA alleles"]
        return Response({'Web Services': obj})

    def post(self, request):
        """Returns UNOS antigen for an allele."""
        serializer = serializers.AlleleSerializer(data=request.data)    

        if serializer.is_valid():
            allele = serializer.data.get('allele')
            ag = conversion_functions.convert_allele_to_ag(allele)
            return Response({'Antigen': ag})
        else:
            return Response({"Error": "Check if allele is IMGT/HLA"})
            #serializer.errors, status=status.HTTP_400_BAD_REQUEST)    