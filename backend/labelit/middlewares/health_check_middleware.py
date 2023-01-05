import logging
from django.utils.deprecation import MiddlewareMixin

from django.http import HttpResponse, HttpResponseServerError

logger = logging.getLogger(__name__)


class HealthCheckMiddleware(MiddlewareMixin):
    # def __init__(self, get_response):
    #     self.get_response = get_response
    #     # One-time configuration and initialization.

    def process_request(self, request):
        if request.method == "GET":
            if request.path == "/probes/startup":
                return self.startupProbe(request)
            elif request.path == "/probes/readiness":
                return self.readinessProbe(request)
            elif request.path == "/probes/liveness":
                return self.livenessProbe(request)
        return None

    def startupProbe(self, request):
        return HttpResponse("OK")

    def readinessProbe(self, request):
        if self._dbIsAlive() == False:
            logger.error("DB is not reachable")
            return HttpResponseServerError("Cannot connect to database.")
        return HttpResponse("OK")

    def livenessProbe(self, request):
        if self._dbIsAlive() == False:
            logger.error("DB is not reachable")
            return HttpResponseServerError("Cannot connect to database.")
        return HttpResponse("OK")

    def _dbIsAlive(self):
        # Connect to each database and do a generic standard SQL query
        # that doesn't write any data and doesn't depend on any tables
        # being present.
        try:
            from django.db import connections
            for name in connections:
                cursor = connections[name].cursor()
                cursor.execute("SELECT 1;")
                row = cursor.fetchone()
                if row is None:
                    return False
        except Exception as e:
            logger.exception(e)
            return False
        return True
