import json

from django.db import IntegrityError
from django.http import HttpResponse
import django
from django.views.decorators.http import require_http_methods

from tesis.models import TesisRanking, Tesis
from services.tesis import TesisServices

from tesis.constants import HTTP_RESPONSE_CODES


@require_http_methods(['POST'])
def add_rating(request):
    data = request.POST
    tesis_id = data.get('tesis_id', None)
    user_name = data.get('user_name', '').lower()
    user_email = data.get('user_email', '').lower()
    value = data.get('rate', '')

    if not user_name or len(user_name) < 3:
        respond = {
            'error_message': 'EL nombre ingresado de tener 3 o más caracteres.',
        }
        return HttpResponse(json.dumps(respond), content_type='application/json')
    if not user_email or len(user_email) < 3 or '@' not in user_email:
        respond = {
            'error_message': 'La dirección de correo ingresada no es válida.',
        }
        return HttpResponse(json.dumps(respond), content_type='application/json')

    try:
        tesis_by_id = Tesis.objects.get(id=tesis_id)
        tesis_rating = TesisRanking(tesis_id=tesis_by_id, value=int(value), date_vote=django.utils.timezone.now,
                                    user_name=user_name, user_email=user_email)
        tesis_rating.save()
        new_tesis_rating = TesisServices.get_tesis_rating(tesis_id=tesis_id)
        return HttpResponse(json.dumps(new_tesis_rating), content_type='application/json')
    except Exception as e:
        print(e)
        if isinstance(e, IntegrityError):
            code = 200
            respond = {
                'error_message': 'El correo ingresado ya envió una valoración.',
            }
        else:
            print(e)
            code = HTTP_RESPONSE_CODES['PRECONDITION_FAILED']
            respond = {
                'error_message': 'Error desconocido al guardar la valoración.',
            }
        return HttpResponse(status=code, content_type='application/json',
                            content=json.dumps(respond))
