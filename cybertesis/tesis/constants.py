# Códigos de respuesta HTTP
HTTP_RESPONSE_CODES = {
    'NO_CONTENT': 204,
    'OK': 200,
    'BAD_REQUEST': 400,
    'NOT_FOUND': 404,
    'FORBIDDEN': 403,
    'PRECONDITION_FAILED': 412
}

ORDER_BY_MOST_RECENT = 1
ORDER_BY_MOST_VALUED = 2

TYPE_CHOICES = (
    ('T', 'Tesis'),
    ('TD', 'Tesis Doctoral'),
    ('MS', 'Maestría'),
    ('TM', 'Tesis Maestría')
)
