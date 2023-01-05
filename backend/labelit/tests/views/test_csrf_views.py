from django.test import TestCase
from labelit.views import csrf
from django.test.client import RequestFactory
import json

###
# csrf views no longer needed, TODO: remove
###
class CsrfViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_csrf_token(self):
        response = csrf(self.factory.get("/csrf/"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("csrfToken" in json.loads(response.content).keys())
