from rest_framework.decorators import api_view
from rest_framework.views import Response


@api_view(http_method_names=['POST', 'GET'])
def recipes_api_list(request):
    return Response({
        'name': 'blabla'
    })
