import usaddress
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError


class Home(TemplateView):
    template_name = 'parserator_web/index.html'


class AddressParse(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # TODO: Flesh out this method to parse an address string using the
        # parse() method and return the parsed components to the frontend.
        address = request.query_params.get('address')

        if not address:
            return Response({
                'data': None,
                'error': {
                    'message': "Missing 'address' query param "
                }
            }, status.HTTP_400_BAD_REQUEST)
        else:
            try:
                address_components, address_type = self.parse(address)
                return Response({
                    'data': {
                        'input_string': address,
                        'address_components': address_components,
                        'address_type': address_type
                    },
                    'error': None
                })
            except Exception as err:
                return Response({
                    'data': None,
                    'error': {
                        'message': err.__str__()
                    }
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def parse(self, address):
        # TODO: Implement this method to return the parsed components of a
        # given address using usaddress: https://github.com/datamade/usaddress

        try:
            address_parse = usaddress.tag(address)
            address_components = address_parse[0]
            address_type = address_parse[1]
            return address_components, address_type
        except Exception:
            raise
