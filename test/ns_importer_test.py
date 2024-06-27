import unittest
from unittest.mock import patch
from ns_importer import data2prepared_html, open_example_json, extract_warning_message, get_response, refactor_dt_cols
import test_utils
import os
from pandas.testing import assert_frame_equal
from pandas import Series


class Ns_importer_test(unittest.TestCase):
    def test_data2prepared_html(self):
        self.maxDiff = None
        os.chdir('..')
        test_payload = open_example_json()
        prepared_html = data2prepared_html(test_payload)
        print(prepared_html)
        self.assertMultiLineEqual(prepared_html, test_utils.html_expected)

    def test_extracting_warning_message(self):
        messages = [{
            "message": "WARNING_TEST_MESSAGE",
            "style": "WARNING"
        }, {
            "message": "INFO_TEST_MESSAGE",
            "style": "INFO"
        }]
        warnings = extract_warning_message(messages)
        self.assertMultiLineEqual(warnings, 'WARNING_TEST_MESSAGE')

    @staticmethod
    def test_refactor_dt_cols():
        planned = Series(['2018-06-12 09:55', '2018-06-12 10:01'])
        actual = Series(['2018-06-12 09:55', '2018-06-12 10:03'])

        result = refactor_dt_cols(actual, planned)
        assert_frame_equal(result, test_utils.df_expected)

    @patch('ns_importer.requests.request')
    def test_getting_response(self, mock_request):
        mock_request.return_value.ok = True
        response = get_response()
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
