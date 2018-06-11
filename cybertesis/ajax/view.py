import json

from django.http import HttpResponse
import django
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# TODO: controlar csrf
from cybertesis.settings import HTTP_RESPONSE_CODES
from tesis.models import TesisRanking, Tesis
from services.tesis import TesisServices

# TODO: considerar CSRF
@csrf_exempt
@require_http_methods(['POST'])
def add_rating(request):
    data = request.POST
    tesis_id = data.get('tesis_id', None)
    user_name = data.get('user_name', '')
    user_email = data.get('user_email', '')
    value = data.get('rate', '')

    # TODO: almacenar los datos de nombre y correo
    if not user_name or len(user_name) < 3:
        respond = {
            'error_message': 'EL nombre ingresado de tener 3 o más caracteres.',
        }
        return HttpResponse(json.dumps(respond), content_type='application/json')
    if not user_email or len(user_email) < 3 or '@' not in user_email:
        respond = {
            'error_message': 'La dirección de correo ingresada no es válidad.',
        }
        return HttpResponse(json.dumps(respond), content_type='application/json')

    try:
        tesis_by_id = Tesis.objects.get(id=tesis_id)
        tesis_rating = TesisRanking(tesis_id=tesis_by_id, value=int(value), date_vote=django.utils.timezone.now)
        tesis_rating.save()
        new_tesis_rating = TesisServices.get_tesis_rating(tesis_id=tesis_id)
        return HttpResponse(json.dumps(new_tesis_rating), content_type='application/json')
    except Exception as e:
        respond = {
            'error_message': e,
        }
        return HttpResponse(status=HTTP_RESPONSE_CODES['PRECONDITION_FAILED'],
                        content_type='application/json',
                        content=json.dumps(respond))


