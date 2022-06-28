import imp
import json
import os
from django.test import TestCase
from api.connectors.pagespeed_connector import PageSpeed
from api.views import RunpagespeedViews
import responses
from django.conf import settings

# constantes
ENDPOINT_PAGESPEED_CORRECT: str = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=fake_correct_url&category=PERFORMANCE'
ENDPOINT_PAGESPEED_FAIL: str = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=fail_url&category=PERFORMANCE'
TEST_DATA_SET = os.path.join(os.path.dirname(
    __file__), 'data_set/response_example.json')

class PageSpeedTestCases(TestCase):

    def setUp(self):
        super().setUp()
        self.pagespeed_connector = PageSpeed() 

        # mock data
        responses.add(responses.GET,
                      ENDPOINT_PAGESPEED_CORRECT,
                      json={'result': 'fake correct url result'},
                      status=200)        

        responses.add(responses.GET,
                      ENDPOINT_PAGESPEED_FAIL,
                      json={'result': 'fake incorrect url result'},
                      status=400)        

    @responses.activate
    def test_success_response_from_runpagespeed_api(self):
        """
        In this test we will check that the function runpagespeed return a dictionary
        """
        result: dict = self.pagespeed_connector.runpagespeed(url_to_analyse="fake_correct_url")
        self.assertIsNotNone(result)
        self.assertEquals(type(result), dict)

    @responses.activate
    def test_failed_response_from_runpagespeed_api(self):
        """
        In this test we will check that the function runpagespeed return None
        """
        result: dict = self.pagespeed_connector.runpagespeed(url_to_analyse="fail_url")
        self.assertIsNone(result)

    def test_parse_data_function(self):
        """
        In this test we will test the function parse_data of PageSpeed class
        by passing an exemple of runpagespeed API response

        expected result : 
            * dict
            * dict contains keys (performance_score, interactive, speed_index, javascript_execution_time) 
        """
        
        # initial data 
        initial_data: dict = {}
        # raise ValueError(settings.BASE_DIR)
        with open(TEST_DATA_SET, "r") as data_file:
            initial_data: dict = json.loads(data_file.read())

        result: dict = self.pagespeed_connector.parse_data(initial_data)
        self.assertEquals(type(result), dict)
        self.assertIn("performance_score", result.keys())
        self.assertEqual(0.99, result.get('performance_score'))
        self.assertIn("interactive_score", result.keys())
        self.assertEqual(0.99, result.get('interactive_score'))
        self.assertIn("speed_index", result.keys())
        self.assertEqual(0.98, result.get('speed_index'))
        self.assertIn("javascript_execution_time", result.keys())
        self.assertEqual("0.4 s", result.get('javascript_execution_time'))
        
