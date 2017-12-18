from django.shortcuts import render
from rest_framework.schemas import SchemaGenerator
from rest_framework.permissions import AllowAny
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import hla
import conversion_functions
from conversion_functions import convert_allele_to_ag, convert_allele_list_to_ags
from hla import allele_truncate
from . import serializers
from rest_framework_swagger.views import get_swagger_view

class AlleleListApiView(generics.GenericAPIView):
    """Returns antigen for an allele"""
    serializer_class = serializers.AlleleListSerializer
   # def get(self, response, format=None):
       # obj = ["UNOS antigen mapping for WHO HLA alleles"]
       # return Response({'Web Services': obj})

    def post(self, request, format=None):
        """Returns UNOS antigens for a list of alleles."""
        serializer = serializers.AlleleListSerializer(data=request.data)    

        if serializer.is_valid(raise_exception=True):
            allele_list = serializer.data.get('allele_list')
            allele_split = allele_list.split(" ")
            output = conversion_functions.convert_allele_list_to_ags(allele_split)
            ag_list = output[0]
            bw46_list = output[1]
            return Response({'Allele List': allele_list, 'Antigens': ag_list, 'Bw4/6': bw46_list})
        else:
            return Response({"Error": "Check if allele is IMGT/HLA"})
                #serializer.errors, status=status.HTTP_400_BAD_REQUEST)    