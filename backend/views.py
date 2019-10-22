from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseNotAllowed
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from json import loads, dumps
from PIL import Image, ImageDraw, ImageFont
import io

EMPTY_RESPONSE = open('backend/mocks/empty.json', mode='r').read()


@method_decorator(csrf_exempt, name='dispatch')
class MockView(View):

    def post(self, request):
        unitId = request.POST.get('auid')
        # openRtbRaw = request.POST['openrtb']
        # openRtb = loads(openRtbRaw)
        response = EMPTY_RESPONSE
        if unitId is not None:
            logFile = open('backend/log.txt', 'w')
            logFile.close()
            try:
                jsonFile = open('backend/mocks/' + unitId + '.json', mode='r')
                response = jsonFile.read()
            except FileNotFoundError:
                response = EMPTY_RESPONSE

        return HttpResponse(response, content_type="application/json")


@method_decorator(csrf_exempt, name='dispatch')
class ApiView(View):

    def post(self, request):
        result = {'result': True}
        unitId = request.POST.get('auid')
        response = request.POST.get('mock')

        if unitId is None:
            result['message'] = 'auid is missing'
            result['result'] = False

        if response is None:
            result['message'] = 'mock is missing'
            result['result'] = False

        if unitId and response:
            try:
                jsonFile = open('backend/mocks/' + unitId + '.json', mode='w')
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
        unitId = request.GET.get('unitId')
        img = Image.new('RGB', (width, height), color=(73, 109, 137))
        bytes = io.BytesIO()
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('font.ttf', 24)
        textW, textH = draw.textsize("OpenX Mock Server. Unit id:" + unitId, font)
        draw.text(((width - textW) / 2, (height - textH) / 2), "OpenX Mock Server. Unit id:" + unitId,
                  fill=(255, 255, 0), font=font)
        img.save(bytes, 'png')
        return HttpResponse(bytes.getvalue(), content_type="image/png")


@method_decorator(csrf_exempt, name='dispatch')
class EventsView(View):

    def get(self, request):
        logFile = open('backend/log.txt', 'a')
        logFile.write(request.build_absolute_uri() + '\r\n')
        logFile.close()
        return HttpResponse(request)


@method_decorator(csrf_exempt, name='dispatch')
class EventsLogView(View):

    def get(self, request):
        logFile = open('backend/log.txt', 'r')
        logs = [log.rstrip() for log in logFile.readlines()]
        logFile.close()
        return HttpResponse(dumps(logs), content_type="application/json")
