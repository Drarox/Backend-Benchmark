import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def process_numbers(request):
    try:
        data = json.loads(request.body)
        numbers = data.get('numbers')
        if not isinstance(numbers, list) or not all(isinstance(n, (int, float)) for n in numbers):
            return HttpResponseBadRequest('Invalid input: "numbers" must be a list of numbers.')
        
        result = sum(x*x for x in numbers)
        return JsonResponse({'result': result})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON.')
