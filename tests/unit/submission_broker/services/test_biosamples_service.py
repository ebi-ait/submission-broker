import unittest
from unittest.mock import MagicMock, Mock

from biosamples_v4.models import Sample
from biosamples_v4.aap import Client as AapClient

from submission_broker.services.biosamples import BioSamples


class MyTestCase(unittest.TestCase):
    def test_valid_submission_request_response_with_success(self):
        aap_client = AapClient("username", "password", "url")
        aap_client.get_token = Mock()
        sample = Sample(name="FakeSample")
        expected_response = {
            "name": "FakeSample",
            "accession": "SAMFAKE123456",
            "domain": "self.ExampleDomain",
            "characteristics": {}
        }

        biosamples = BioSamples(aap_client, "url")
        biosamples.biosamples.persist_sample = MagicMock(return_value=expected_response)

        actual_response = biosamples.send_sample(sample)

        self.assertEqual(expected_response, actual_response)


if __name__ == '__main__':
    unittest.main()
