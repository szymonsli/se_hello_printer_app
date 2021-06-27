import unittest
import json
import xml.etree.cElementTree as ET
from hello_world import app
from hello_world.formater import SUPPORTED


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_outputs(self):
        rv = self.app.get('/outputs')
        s = str(rv.data)
        ','.join(SUPPORTED) in s

    def test_msg_with_output(self):
        test_data = {"imie": "Simon", "msg": "Hello World!"}
        rv = self.app.get('/?output=json')
        js = json.loads(rv.data)
        self.assertEqual(test_data['msg'], js['msg'])
        self.assertEqual(test_data['imie'], js['imie'])

    def test_msg_with_xml_output(self):
        # Tworzenie XML
        greetings = ET.Element("greeetings")
        name = ET.SubElement(greetings, "imie")
        name.text = "Simon"
        message = ET.SubElement(greetings, "msg")
        message.text = "Hello World!"

        test_xml = ET.tostring(greetings)

        # Wczytanie XMLa z aplikacji
        rv = self.app.get('/?output=xml')

        # Test
        self.assertEqual(test_xml, rv.data)
