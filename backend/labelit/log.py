import sys
import logging
import traceback
import json_log_formatter

# Configure logger to capture exceptions
def uncaught_exception_handler(type, value, tb):
    extra_info = {
        'uncaught_exception_exc_info': traceback.format_exc(),
    }
    logger.critical("Uncaught exception: {0}".format(str(value)), extra=extra_info)

# Install exception handler
logger = logging.getLogger(__name__)
sys.excepthook = uncaught_exception_handler

class JSONFormatter(json_log_formatter.JSONFormatter):
    """ Formats logs in JSON """

    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        log = {}
        log['message'] = message

        log['level'] = record.levelname
        log['module_name'] = record.name

        if record.exc_info:
            log['exc_info'] = self.formatException(record.exc_info)

        if 'uncaught_exception_exc_info' in extra.keys():
            log['exc_info'] = extra['uncaught_exception_exc_info']

        return log
