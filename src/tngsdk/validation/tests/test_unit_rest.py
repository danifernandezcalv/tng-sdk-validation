#  Copyright (c) 2015 SONATA-NFV, 5GTANGO, UBIWHERE, Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, 5GTANGO, UBIWHERE, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).


import unittest
import json
import time
import ast
from unittest.mock import patch
from requests.exceptions import RequestException
# Do unit test of specific functions
# from tngsdk.validation.rest import app, on_unpackaging_done,
#                                    on_packaging_done
from tngsdk.validation.rest import app

SAMPLES_DIR = 'src/tngsdk/validation/tests/'


# class MockResponse(object):
#         pass

#
# def mock_requests_post(url, json):
#     if url != "https://test.local:8000/cb":
#         raise RequestException("bad url")
#     if "event_name" not in json:
#         raise RequestException("bad request")
#     if "package_id" not in json:
#         raise RequestException("bad request")
#     if "package_location" not in json:
#         raise RequestException("bad request")
#     if "package_metadata" not in json:
#         raise RequestException("bad request")
#     if "package_process_uuid" not in json:
#         raise RequestException("bad request")
#     mr = MockResponse()
#     mr.status_code = 200
#     return mr


class TngSdkValidationRestTest(unittest.TestCase):

    def setUp(self):
        # configure mocks
        # self.patcher = patch("requests.post", mock_requests_post)
        # self.patcher.start()
        # configure flask
        app.config['TESTING'] = True
        app.cliargs = None
        self.app = app.test_client()

    # def tearDown(self):
    #     self.patcher.stop()

    # def test_validations_v1_endpoint(self):
    #     # do a malformed post
    #     r = self.app.post("/api/v1/validations")
    #     self.assertEqual(r.status_code, 400)
    #     # do a post with a real validation for function
    #     # w/o errors
    #     r = self.app.post("/api/v1/packages",
    #                       content_type="multipart/form-data",
    #                       data={"package": (
    #                           open("misc/5gtango-ns-package-example.tgo",
    #                                "rb"), "5gtango-ns-package-example.tgo"),
    #                             "skip_store": True})
    #     self.assertEqual(r.status_code, 200)
    #     rd = json.loads(r.get_data(as_text=True))
    #     self.assertIn("package_process_uuid", rd)
        # do a post with a real validation for service
        # w/o errors

        # do a post with a real validation for fucntion
        # w/o errors

        # do a post with a real validation for service
        # with errors

    def test_rest_validation_function_syntax_ok_file(self):
        with open(SAMPLES_DIR + 'samples/functions/valid-son/' +
                  'firewall-vnfd.yml', 'rb') as f:
            r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                              'function=embedded',
                              files={'firewall-vnfd.yml': f})
            data = r.data.decode('utf-8')
            d = ast.literal_eval(data)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(d['error_count'], 0)

    def test_rest_validation_function_syntax_ok(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'function=' + SAMPLES_DIR + 'samples/functions/' +
                          'valid-syntax-tng/default-vnfd-tng.yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 0)

    def test_rest_validation_function_syntax_ok_dext(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'function=' + SAMPLES_DIR + 'samples/functions/' +
                          'valid-syntax-tng/&dext=yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 0)

    def test_rest_validation_function_syntax_ko(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'function=' + SAMPLES_DIR + 'samples/functions/' +
                          'invalid-syntax-tng/default-vnfd-tng.yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 1)

    def test_rest_validation_service_syntax_ok(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'service=' + SAMPLES_DIR + 'samples/services/' +
                          'valid-son/valid.yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 0)

    def test_rest_validation_service_syntax_ko(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'service=' + SAMPLES_DIR + 'samples/services/' +
                          'invalid-syntax-tng/unexpected_field.yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 1)

    def test_rest_validation_function_integrity_ok(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&function=' + SAMPLES_DIR +
                          'samples/' +
                          'functions/valid-son/firewall-vnfd.yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 0)

    def test_rest_validation_function_integrity_ok_dext(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&function=' + SAMPLES_DIR +
                          'samples/functions/valid-son/&&dext=yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 0)

    def test_rest_validation_function_integrity_ko(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&function=' + SAMPLES_DIR +
                          'samplesfunctions/invalid_integrity-son/' +
                          'firewall-vnfd.yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 1)

    def test_rest_validation_function_integrity_ko_dext(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&function=' + SAMPLES_DIR +
                          'samples/functions/invalid_integrity-son/&dext=yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 3)

    def test_rest_validation_service_integrity_ok(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&service=' + SAMPLES_DIR +
                          'samples/' +
                          'services/valid-son/valid.yml&dpath=' +
                          SAMPLES_DIR +
                          'samples/functions/valid-son/&dext=yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 0)

    def test_rest_validation_service_integrity_ko(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&service=' + SAMPLES_DIR +
                          'samples/' +
                          'services/valid-son/valid.yml&dpath=' +
                          SAMPLES_DIR +
                          'samples/functions/invalid_integrity-son/&dext=yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 3)

    def test_rest_validation_function_topology_ok(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&topology=true&function=' +
                          SAMPLES_DIR +
                          'samples/functions/valid-son/firewall-vnfd.yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 0)

    def test_rest_validation_function_topology_ok_dext(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&topology=true&function=' +
                          SAMPLES_DIR +
                          'samples/functions/valid-son/&dext=yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 0)

    def test_rest_validation_function_topology_ko(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&topology=true&function=' +
                          SAMPLES_DIR +
                          'samples/functions/invalid_topology-son/' +
                          'firewall-vnfd.yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 1)

    def test_rest_validation_function_topology_ko_dext(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&topology=true&function=' +
                          SAMPLES_DIR +
                          'samples/functions/invalid_topology-son/&dext=yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 1)

    def test_rest_validation_service_topology_ok(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&topology=true&service=' +
                          SAMPLES_DIR +
                          'samples/services/valid-son/valid.yml&dpath=' +
                          SAMPLES_DIR +
                          'samples/functions/valid-son/&dext=yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 0)

    def test_rest_validation_service_topology_ko(self):
        r = self.app.post('/api/v1/validations?sync=true&syntax=true&' +
                          'integrity=true&topology=true&service=' +
                          SAMPLES_DIR +
                          'samples/services/valid-son/valid.yml&dpath=' +
                          SAMPLES_DIR +
                          'samples/functions/invalid_topology-son/&dext=yml')
        data = r.data.decode('utf-8')
        d = ast.literal_eval(data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(d['error_count'], 1)


if __name__ == "__main__":
    unittest.main()
