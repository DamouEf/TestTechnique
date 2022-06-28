import json
from unittest import result
from django.http import HttpResponse
from api.connectors.pagespeed_connector import PageSpeed
# Create your views here.


def RunpagespeedViews(request):

    pagespeed_connector: PageSpeed = PageSpeed()
    result: dict = pagespeed_connector.runpagespeed(url_to_analyse="https://www.voici.fr/")

    return HttpResponse(json.dumps(result))