from rest_framework import serializers


class AlleleSerializer(serializers.Serializer):
	
	"""Create and return a new instance, given the validated data
	Serializes a name field for testing our APIView."""
	allele = serializers.CharField(max_length=None)
	


class AlleleListSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView."""
    allele_list = serializers.CharField(max_length=None)    

class GlstringSerializer(serializers.Serializer):
	"""Serializes a name field for testing our APIView."""
	gl_string = serializers.CharField(max_length=None)
	pop = serializers.CharField(max_length=None)    

class MACSerializer(serializers.Serializer):
	"""Serializes a name field for testing our APIView."""
	allele_codes_list = serializers.CharField(max_length=None)
	pop = serializers.CharField(max_length=None)    	

#class GlstringSerializer(serializers.Serializer):
	#"""Serilaizes a name field for testing API view."""
	#gl_string = serializers.CharField(max_length=5000)
