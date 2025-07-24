import unittest
from unittest.mock import patch, MagicMock
from GreenIsland.plantid.arduino_service import *

class TestGetWateringInfo(unittest.TestCase):
    @patch('plant_service.db')
    def test_get_watering_info_success(self, mock_db):
        # Mock des documents Firestore
        plant_doc_mock = MagicMock()
        plant_doc_mock.exists = True
        plant_doc_mock.to_dict.return_value = {'name': 'Hisbicus'}

        plant_data_doc_mock = MagicMock()
        plant_data_doc_mock.exists = True
        plant_data_doc_mock.to_dict.return_value = {
            'data': {
                'zone culture': 'Zone 9b ensoleillée'
            }
        }

        zone_doc_mock = MagicMock()
        zone_doc_mock.exists = True
        zone_doc_mock.to_dict.return_value = {
            'watering': 'Arroser 2 fois par semaine'
        }

        # Configuration de la séquence des appels
        mock_db.collection.return_value.document.return_value.get.side_effect = [
            plant_doc_mock,       # plants
            plant_data_doc_mock,  # plants_data
            zone_doc_mock         # zones
        ]

        result = get_watering_info_from_plant_doc("plant123")
        self.assertEqual(result, 'Arroser 2 fois par semaine')

    @patch('plant_service.db')
    def test_plant_doc_not_exist(self, mock_db):
        mock_doc = MagicMock()
        mock_doc.exists = False

        mock_db.collection.return_value.document.return_value.get.return_value = mock_doc

        result = get_watering_info_from_plant_doc("plant123")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()