from unittest.case import TestCase
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from app import application


class AppTest(TestCase):
    def setUp(self):
        self.client = Client(application, BaseResponse)

    def test_post_html_file_should_produce_pdf_response(self):
        response = self.client.post('/', data={'file': open('sample.html')})
        self.assertEquals(200, response.status_code)
        self.assertEquals('application/pdf', response.headers['Content-Type'])
