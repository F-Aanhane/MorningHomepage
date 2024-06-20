import unittest
from ns_importer import data2prepared_html, open_example_json, extract_warning
import os


class Ns_importer_test(unittest.TestCase):
    def test_data2prepared_html(self):
        os.chdir('..')
        test_payload = open_example_json()
        prepared_html = data2prepared_html(test_payload)
        self.assertMultiLineEqual(prepared_html, expected_html)

    def test_extract_warning(self):
        messages = [{
                "message": "WARNING_TEST_MESSAGE",
                "style": "WARNING"
            }, {
                "message": "INFO_TEST_MESSAGE",
                "style": "INFO"
            }]
        warnings = extract_warning(messages)
        self.assertMultiLineEqual(warnings, 'WARNING_TEST_MESSAGE')


expected_html = """<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>planned</th>
      <th>delay</th>
      <th>cat</th>
      <th>direction</th>
      <th>platform</th>
      <th>warnings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>12:04</td>
      <td></td>
      <td>SPR</td>
      <td>Den Haag Centraal</td>
      <td>3</td>
      <td></td>
    </tr>
    <tr>
      <td>12:06</td>
      <td>+1</td>
      <td>IC</td>
      <td>Amsterdam Centraal</td>
      <td>6</td>
      <td></td>
    </tr>
    <tr>
      <td>12:12</td>
      <td></td>
      <td>SPR</td>
      <td>Hoorn Kersenboogerd</td>
      <td>4</td>
      <td>Rijdt niet verder dan Hoofddorp door een defecte bovenleiding</td>
    </tr>
    <tr>
      <td>12:14</td>
      <td></td>
      <td>IC</td>
      <td>Dordrecht</td>
      <td>5</td>
      <td></td>
    </tr>
    <tr>
      <td>12:16</td>
      <td></td>
      <td>IC</td>
      <td>Venlo</td>
      <td>6</td>
      <td></td>
    </tr>
    <tr>
      <td>12:20</td>
      <td></td>
      <td>SPR</td>
      <td>Den Haag Centraal</td>
      <td>3</td>
      <td></td>
    </tr>
    <tr>
      <td>12:24</td>
      <td></td>
      <td>IC</td>
      <td>Vlissingen</td>
      <td>5</td>
      <td></td>
    </tr>
    <tr>
      <td>12:25</td>
      <td></td>
      <td>SPR</td>
      <td>Haarlem</td>
      <td>4</td>
      <td></td>
    </tr>
    <tr>
      <td>12:34</td>
      <td></td>
      <td>SPR</td>
      <td>Den Haag Centraal</td>
      <td>3</td>
      <td></td>
    </tr>
    <tr>
      <td>12:36</td>
      <td></td>
      <td>IC</td>
      <td>Amsterdam Centraal</td>
      <td>6</td>
      <td></td>
    </tr>
  </tbody>
</table>"""


if __name__ == '__main__':
    unittest.main()


