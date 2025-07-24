import unittest
from unittest.mock import patch, MagicMock
from GreenIsland.plantid.plant_utils import parse_plant_info, scrap_plant, insert_plant_in_firestore

class ParsePlantInfoTestCase(unittest.TestCase):
    def test_parse_valid_text(self):
        text = "• Type : vivace\n• Hauteur : 50 cm\n• Floraison : été"
        expected = {
            "Type": "vivace",
            "Hauteur": "50 cm",
            "Floraison": "été"
        }
        self.assertEqual(parse_plant_info(text), expected)

    def test_parse_empty_text(self):
        self.assertEqual(parse_plant_info(""), {})

    def test_parse_text_without_colon(self):
        text = "• Juste un texte sans valeur claire"
        self.assertEqual(parse_plant_info(text), {})


class ScrapPlantTestCase(unittest.TestCase):
    @patch('GreenIsland.plantid.plant_utils.webdriver.Chrome')
    def test_scrap_plant_returns_parsed_text(self, mock_chrome):
        mock_driver = MagicMock()
        element_mock = MagicMock()
        element_mock.text = "• Type : vivace\n• Floraison : printemps"

        mock_driver.find_element.return_value = element_mock
        mock_chrome.return_value = mock_driver

        result = scrap_plant("plante-test")
        expected = {
            "Type": "vivace",
            "Floraison": "printemps"
        }
        self.assertEqual(result, expected)

        mock_driver.quit.assert_called()  # Vérifie que quit a été appelé

    @patch('GreenIsland.plantid.plant_utils.webdriver.Chrome')
    def test_scrap_plant_not_found_return_none(self, mock_chrome):
        mock_driver = MagicMock()
        mock_driver.find_element.side_effect = Exception("Not Found")
        mock_chrome.return_value = mock_driver

        result = scrap_plant("plante-inconnue")
        self.assertIsNone(result)


class FirebaseInsertTestCase(unittest.TestCase):
    @patch('GreenIsland.plantid.plant_utils.db')
    def test_insert_valid_data(self, mock_db):
        mock_doc_ref = MagicMock()
        mock_doc_ref.get.return_value.exists = False
        mock_db.collection.return_value.document.return_value = mock_doc_ref

        data = {
            "plant": "Menthe",
            "texte": {
                "Type": "Aromatique",
                "Soleil": "Ombre partielle"
            }
        }

        success = insert_plant_in_firestore(data)
        self.assertTrue(success)

    @patch('GreenIsland.plantid.plant_utils.db')
    def test_insert_invalid_data(self, mock_db):
        data = {
            "plant": "",
            "texte": None
        }
        success = insert_plant_in_firestore(data)
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()
