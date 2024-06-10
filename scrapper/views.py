# from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .tasks import *
from .utils import get_allowed_coins
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Job
from .coinmarketcap import CoinMarketCap


def index(request):

    return JsonResponse({'status': 'OK', 'error_msg': 'Nothing to worry about', "data": "server started sccessfully"})

@csrf_exempt
def startScrapping(request):
    if request.method == 'POST':
        allowed_coins = get_allowed_coins()
        data = json.loads(request.body)
        coins = data['payload']
        job=dict()
        for coin in coins:
            if coin in allowed_coins:
                continue
            else:
                return JsonResponse({'status': 'ERROR', 'error_msg': 'scraping cannot be continued due to invalid input', "data": None})
        job_id = scrap.delay(coins)
        job['job_id'] = str(job_id)
        job["task_coins"] = coins

        new_job = Job(job_id = job_id, requested_for = coins)
        new_job.save()

        return JsonResponse({'status': 'OK', 'error_msg': None, 'data': job})
    return JsonResponse({'status': 'ERROR', 'error_msg': 'method not allowed !!!', 'data': None})

def scrappingStatus(request, job_id):
    job_obj = Job.objects.filter(job_id = job_id)
    if job_obj:
        task = CoinMarketCap.get_results(job_id)
        if task is not None:
            output_json = {"job_id": job_id, "task": task}
            return JsonResponse(output_json)
        return JsonResponse({'status': 'OK', 'error_msg': 'still pending...', 'data': None})
    
    return JsonResponse({'status': 'ERROR', 'error_msg': 'invalid job id !!!', 'data': None})
        