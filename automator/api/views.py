import json
import time
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from api.models import DriverSessions

Sessions = DriverSessions()

class Index(TemplateView):
    template_name = "index.html"


class BaseView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class API(BaseView):

    def post(self, request: HttpRequest) -> HttpResponse:
        body = json.loads(request.body.decode('utf-8'))
        sessionID = Sessions.addSession(
            body["meetingURL"],
            body["attendanceName"],
            body["chatMessage"])
        return JsonResponse({"sessionID": sessionID})


class Updates(BaseView):

    def get(self, request: HttpRequest, sessionID:str = None) -> StreamingHttpResponse:
        print(sessionID)
        session = Sessions.getSession(sessionID)
        session.start()
        session.run()
        return StreamingHttpResponse(self.report(session), content_type='text/event-stream')

    def report(self, session):
        for i in range(100):
            time.sleep(1)
            print(session.update)
            yield 'data: %s\n\n' %session.update
