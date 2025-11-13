from django.http import JsonResponse


def Pratos(request):
    if request.method == 'GET':
        prato = {
            'id': '1',
            'nome': 'lais',
        }
        return JsonResponse(prato)
