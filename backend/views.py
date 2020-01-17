import io
import time
import urllib.parse
from json import dumps

from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from backend.models import LogModel
from mock.settings import BASE_DIR

EMPTY_RESPONSE = open(BASE_DIR + '/backend/mocks/empty.json', mode='r').read()
EMPTY_VIDEO_RESPONSE = open(BASE_DIR + '/backend/mocks/empty.xml', mode='r').read()


class Configs:
    enableErrorResponse = False
    responseLatency = .0


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
                try:
                    jsonFile = open(BASE_DIR + '/backend/mocks/' + unitId + '.json', mode='r')
                    response = jsonFile.read()
                except FileNotFoundError:
                    response = EMPTY_RESPONSE

        if Configs.responseLatency > 0:
            time.sleep(Configs.responseLatency)

        return HttpResponse(response, content_type="application/json")


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
                try:
                    xmlFile = open(BASE_DIR + '/backend/mocks/' + unitId + '.xml', mode='r')
                    response = xmlFile.read()
                except FileNotFoundError:
                    response = EMPTY_VIDEO_RESPONSE
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
                jsonFile = open(BASE_DIR + '/backend/mocks/' + unitId + '.' + allowed_types[type], mode='w')
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


def write_log(request):
    LogModel(path=request.get_full_path(),
             host=request.get_host(),
             method=request.method,
             body=request.body.decode('utf-8'),
             query_string=urllib.parse.urlencode(request.GET)).save()
