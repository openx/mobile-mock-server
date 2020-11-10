import io
import time
import urllib.parse
import random
from json import dumps, loads

from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from backend.models import LogModel
from mock.settings import BASE_DIR

EMPTY_RESPONSE = open(BASE_DIR + '/backend/mocks/empty.json', mode='r').read()
EMPTY_VIDEO_RESPONSE = open(BASE_DIR + '/backend/mocks/empty.xml', mode='r').read()
NO_BIDS_RESPONSE = open(BASE_DIR + '/backend/mocks/no_bids.json', mode='r').read()

MAX_FAILED_REQUESTS = 3


class Configs:
    enableErrorResponse = False
    responseLatency = .0
    enableRandomNoBids = False
    failedBidRequestCount = 0


@method_decorator(csrf_exempt, name='dispatch')
class MockView(View):

    def post(self, request):
        unitId = request.POST.get('auid')
        # openRtbRaw = request.POST['openrtb']
        # openRtb = loads(openRtbRaw)
        response = EMPTY_RESPONSE
        if unitId is not None:
            write_log(request)
            if Configs.enableErrorResponse is False:
                response = findMock(unitId + ".json", ["acj"], EMPTY_RESPONSE)

        if Configs.responseLatency > 0:
            time.sleep(Configs.responseLatency)

        return HttpResponse(response, content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class CacheMockView(View):

    def get(self, request):
        unitId = request.GET.get('uuid')
        # openRtbRaw = request.POST['openrtb']
        # openRtb = loads(openRtbRaw)
        response = EMPTY_RESPONSE
        if unitId is not None:
            write_log(request)
            if Configs.enableErrorResponse is False:
                response = findMock(unitId + ".json", ["prebid", "cache"], None)

        if Configs.responseLatency > 0:
            time.sleep(Configs.responseLatency)

        if response is None:
            return HttpResponseNotFound("No content stored for uuid=" + unitId)

        result = HttpResponse(response, content_type="application/json")
        originHeader = request.headers.get('origin')
        if originHeader is not None:
            result['access-control-allow-credentials'] = 'true'
            result['access-control-allow-origin'] = originHeader
            result['vary'] = 'Origin'
        return result


@method_decorator(csrf_exempt, name='dispatch')
class PrebidMockView(View):

    def post(self, request):
        unitId = loads(request.body)['imp'][0]['ext']['prebid']['storedrequest']['id']
        response = NO_BIDS_RESPONSE

        # openRtbRaw = request.POST['openrtb']
        # openRtb = loads(openRtbRaw)

        if self.shouldFailBidRequest():
            Configs.failedBidRequestCount += 1
            print("Failing the bid request due to shouldFailBidRequest().")
            return HttpResponse(response, content_type="application/json")

        Configs.failedBidRequestCount = 0

        if unitId is not None:
            write_log(request)
            if Configs.enableErrorResponse is False:
                response = findMock(unitId + ".json", ["prebid"], NO_BIDS_RESPONSE)

        if Configs.responseLatency > 0:
            time.sleep(Configs.responseLatency)

        return HttpResponse(response, content_type="application/json")

    def shouldFailBidRequest(self):
        return Configs.enableRandomNoBids and Configs.failedBidRequestCount < MAX_FAILED_REQUESTS and random.random() < 0.5


@method_decorator(csrf_exempt, name='dispatch')
class VideoMockView(View):

    def post(self, request):
        unitId = request.POST.get('auid') if request.POST.get('auid') else request.POST.get('pgid')
        # openRtbRaw = request.POST['openrtb']
        # openRtb = loads(openRtbRaw)
        response = EMPTY_VIDEO_RESPONSE
        if unitId is not None:
            write_log(request)
            if Configs.enableErrorResponse is False:
                response = findMock(unitId + ".xml", ["video"], EMPTY_VIDEO_RESPONSE)
        if Configs.responseLatency > 0:
            time.sleep(Configs.responseLatency)

        return HttpResponse(response, content_type="text/xml")


@method_decorator(csrf_exempt, name='dispatch')
class AddMockView(View):

    def post(self, request):
        allowed_types = {'regular': 'json', 'video': 'xml'}

        result = {'result': True}
        unitId = request.POST.get('auid')
        response = request.POST.get('mock')
        type = request.POST.get('type') if request.POST.get('type') else 'regular'

        if not type in allowed_types.keys():
            result['message'] = 'Supported types: {0}'.format(', '.join(allowed_types.keys()))
            result['result'] = False

        if unitId is None:
            result['message'] = 'auid is missing'
            result['result'] = False

        if response is None:
            result['message'] = 'mock is missing'
            result['result'] = False

        if unitId and response:
            try:
                jsonFile = open(BASE_DIR + '/backend/mocks/_dynamic/' + unitId + '.' + allowed_types[type], mode='w')
                jsonFile.write(response)
                jsonFile.close()
            except RuntimeError:
                result['result'] = False

        return HttpResponse(dumps(result), content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class ImageGeneratorView(View):

    def get(self, request):
        width = int(request.GET.get('width')) if request.GET.get('width') else 640
        height = int(request.GET.get('height')) if request.GET.get('height') else 100
        unitId = request.GET.get('auid')
        img = Image.new('RGB', (width, height), color=(73, 109, 137))
        bytes = io.BytesIO()
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(BASE_DIR + '/font.ttf', 24)
        textW, textH = draw.textsize("OpenX Mock Server. Unit id:" + unitId, font)
        draw.text(((width - textW) / 2, (height - textH) / 2), "OpenX Mock Server. Unit id:" + unitId,
                  fill=(255, 255, 0), font=font)
        img.save(bytes, 'png')
        return HttpResponse(bytes.getvalue(), content_type="image/png")


@method_decorator(csrf_exempt, name='dispatch')
class EventsView(View):

    def get(self, request):
        write_log(request)
        return HttpResponse(request)


@method_decorator(csrf_exempt, name='dispatch')
class ClearLogView(View):

    def get(self, request):
        LogModel.objects.all().delete()
        return HttpResponse(request)


@method_decorator(csrf_exempt, name='dispatch')
class EventsLogView(View):

    def get(self, request):
        json = {'requests': []}

        for log in LogModel.objects.all():
            json['requests'].append({'path' : log.path,
                                     'host' : log.host,
                                     'method' : log.method,
                                     'body' : log.body,
                                     'queryString': dict(urllib.parse.parse_qsl(log.query_string))})

        return HttpResponse(dumps(json), content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class SetLatencyView(View):

    def post(self, request):
        Configs.responseLatency = float(request.POST.get("latency"))/1000

        return HttpResponse("{}", content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class CancelLatencyView(View):

    def get(self, request):
        Configs.responseLatency = 0

        return HttpResponse(request)


@method_decorator(csrf_exempt, name='dispatch')
class SetErrorView(View):

    def get(self, request):
        Configs.enableErrorResponse = True

        return HttpResponse(request)


@method_decorator(csrf_exempt, name='dispatch')
class CancelErrorView(View):

    def get(self, request):
        Configs.enableErrorResponse = False

        return HttpResponse(request)

@method_decorator(csrf_exempt, name='dispatch')
class SetRandomNoBidsView(View):

    def post(self, request):
        Configs.enableRandomNoBids = True

        return HttpResponse("{}", content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class CancelRandomNoBidsView(View):

    def get(self, request):
        Configs.enableRandomNoBids = False
        Configs.failedBidRequestCount = 0

        return HttpResponse(request)

def write_log(request):
    LogModel(path=request.get_full_path(),
             host=request.get_host(),
             method=request.method,
             body=request.body.decode('utf-8'),
             query_string=urllib.parse.urlencode(request.GET)).save()

def findMock(name, paths, fallback):
    folders = ["_dynamic/"]
    for skipCount in range(len(paths)):
        s = ""
        for i in range(len(paths) - skipCount):
            s = s + paths[i] + "/"
        folders.append(s)
    for nextFolder in folders:
        mockFileName = BASE_DIR + '/backend/mocks/' + nextFolder + name
        try:
            jsonFile = open(mockFileName, mode='r')
            result = jsonFile.read()
            return result
        except FileNotFoundError:
            pass
    return fallback
