from celery import shared_task
from .coinmarketcap import CoinMarketCap
from .models import Job
import json

@shared_task(bind=True)
def scrap(self, coins, *args):
    C = CoinMarketCap()
    C.make_request(coins)
    C.scrap_and_process_data()
    json_data = C.final_output()
    json_data = json.loads(json_data)

    for coin in json_data:
        job_id = self.request.id
        coin_symbol = coin['coin']
        coin_slug = coin['slug']
        coin_data = coin['output']
        new_job = Job.objects.get(job_id = job_id)
        new_job.task_set.create(coin = coin_symbol, slug = coin_slug, data = coin_data)
    del C
    return None
