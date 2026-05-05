from django.http import JsonResponse

def home(request):
    return JsonResponse({
        'message': 'Bienvenue sur OCALM API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'profile': '/api/auth/profile/'
            },
            'escrow': {
                'transactions': '/api/escrow/transactions/',
                'create': '/api/escrow/transactions/create_transaction/'
            }
        }
    })
