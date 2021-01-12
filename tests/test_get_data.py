# TODO add tests

import glob
import os
from unittest import TestCase
from uniprot_variant_import.constants import *
from uniprot_variant_import import get_data


class TestGetData(TestCase):

    def setUp(self):
        self.gd = get_data.GetData(SIFTS_URL_TO_MAPPING,'DATA')

    def tearDown(self):
        if glob.glob(self.gd.path_to_data):
            os.system('rm -f %s' % self.gd.path_to_data)
        if glob.glob(MAPPING_FILE_NAME):
            os.system('rm %s' % MAPPING_FILE_NAME)
            os.system('rm %s.gz' % MAPPING_FILE_NAME)

    def test_make_folder(self):
        # Check if new folder is created
        self.assertIsNotNone(self.gd.make_folder())
        # Check if no new folder is made if there is already one
        self.assertIsNone(self.gd.make_folder())

    def test_get_file(self):
        self.gd.get_file()
        # Check if the file can be retrieved
        self.assertIsNotNone(glob.glob('%s.gz' % MAPPING_FILE_NAME))

    def test_extract(self):
        self.gd.extract()
        # Check if the file can be extracted
        self.assertIsNotNone(glob.glob(MAPPING_FILE_NAME))

    # def test_jsons(self):
    #     self.gd.path_to_data = 'TMP'
    #     os.system('touch TMP/tmp.json')
    #     self.gd.get_jsons(clean=True)




