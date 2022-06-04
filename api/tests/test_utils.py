import os
from unittest import TestCase
from unittest.mock import Mock
import settings

from werkzeug.datastructures import FileStorage

import utils


class TestUtils(TestCase):

    def test_allowed_file(self):
        self.assertTrue(utils.allowed_file('cat.JPG'))
        self.assertTrue(utils.allowed_file('cat.jpeg'))
        self.assertTrue(utils.allowed_file('cat.JPEG'))
        self.assertTrue(utils.allowed_file('../../car.PNG'))
        self.assertTrue(utils.allowed_file('/usr/var/src/car.gif'))

        self.assertFalse(utils.allowed_file('cat.JPGG'))
        self.assertFalse(utils.allowed_file('invoice.pdf'))
        self.assertFalse(utils.allowed_file('/usr/src/slides.odt'))
        self.assertFalse(utils.allowed_file('/usr/src/api'))
        self.assertFalse(utils.allowed_file('/usr/src/api/'))
        self.assertFalse(utils.allowed_file('/usr/src/dog.'))
        self.assertFalse(utils.allowed_file('/usr/src/dog./'))

    def test_get_file_hash(self):
        filename = 'tests/dog.jpeg'
        md5_filename = '0a7c757a80f2c5b13fa7a2a47a683593.jpeg'
        with open(filename, 'rb') as fp:
            file = FileStorage(fp)

            # Check the new filename is correct
            new_filename = utils.get_file_hash(file)
            self.assertEqual(md5_filename, new_filename, new_filename)

            # Check the file content is still readable!
            self.assertTrue(file.read() != b"")
    
    def test_read_and_save_prediction(self):
        file_name = '0a7c757a80f2c5b13fa7a2a47a683593.jpeg'
        file_name_txt = '0a7c757a80f2c5b13fa7a2a47a683593.txt'

        pred_class = "Eskimo_dog"
        pred_score = 0.9346

        # first delete txt file if exist
        if (os.path.exists(os.path.join(settings.UPLOAD_FOLDER, file_name_txt))):
            os.remove(os.path.join(settings.UPLOAD_FOLDER, file_name_txt))

        # save prediction
        utils.save_predictions(file_name,pred_score,pred_class)

        # Check if file exist
        self.assertTrue(os.path.exists(os.path.join(settings.UPLOAD_FOLDER, file_name_txt)) == True)
        
        # check if it has the correct predictions
        class_name, score = utils.read_prediction_file(file_name)
        self.assertEqual(pred_class, class_name, class_name)
        self.assertEqual(pred_score, score, score)

        # remove the file
        os.remove(os.path.join(settings.UPLOAD_FOLDER, file_name_txt))

    def test_get_prediction(self):
        file_name = '0a7c757a80f2c5b13fa7a2a47a683593.jpeg'
        file_name_txt = '0a7c757a80f2c5b13fa7a2a47a683593.txt'
        pred_class = "Eskimo_dog"
        pred_score = 0.9346
        model_predict = Mock()
        model_predict.return_value = (pred_class, pred_score)

        # first delete txt file if exist
        if (os.path.exists(os.path.join(settings.UPLOAD_FOLDER, file_name_txt))):
            os.remove(os.path.join(settings.UPLOAD_FOLDER, file_name_txt))

        class_name, score = utils.get_prediction(model_predict, file_name)

        # check if it has the correct predictions
        class_name, score = utils.read_prediction_file(file_name)
        self.assertEqual(pred_class, class_name, class_name)
        self.assertEqual(pred_score, score, score)

        # check if the correct predictions were saved
        class_name, score = utils.read_prediction_file(file_name)
        self.assertEqual(pred_class, class_name, class_name)
        self.assertEqual(pred_score, score, score)

        # remove the file
        os.remove(os.path.join(settings.UPLOAD_FOLDER, file_name_txt))
    
    def test_process_file(self):
        request_mock = Mock()
        filename = 'tests/dog.jpeg'
        md5_filename = '0a7c757a80f2c5b13fa7a2a47a683593.jpeg'

        request_mock.files = {}
        result = utils.process_file(request_mock, 'file')
        self.assertEqual(result["error"], 'No file part')
        self.assertEqual(result["redirect_home"], True)
        self.assertEqual(result["valid"], False)
        self.assertEqual(result["file_name"], False)
        
        with open(filename, 'rb') as fp:
            file = FileStorage(fp)

            request_mock.files = {'file': file}

            result = utils.process_file(request_mock, 'file')
            
            self.assertEqual(result["error"], None)
            self.assertEqual(result["redirect_home"], False)
            self.assertEqual(result["valid"], True)
            self.assertEqual(result["file_name"], md5_filename)

            file.filename = ""
            request_mock.files = {'file': file}

            result = utils.process_file(request_mock, 'file')

            self.assertEqual(result["error"], 'No image selected for uploading')
            self.assertEqual(result["redirect_home"], True)
            self.assertEqual(result["valid"], False)
            self.assertEqual(result["file_name"], False)


