import glob
import os
from unittest import TestCase
from uniprot_variant_import.constants import *
from uniprot_variant_import import get_data


class TestGetData(TestCase):

    def setUp(self):
        self.gd = get_data.GetData(SIFTS_URL_TO_MAPPING,'tmp')
        self.gd.mapping_file_name = 'tmp.mapping'

    def test_make_folder(self):
        # Check if new folder is created
        self.assertIsNotNone(self.gd.make_folder())
        # Check if no new folder is made if there is already one
        self.assertIsNone(self.gd.make_folder())
        os.system('rm -fr tmp')

    def test_get_file(self):
        self.gd.get_file()
        # Check if the file can be retrieved
        self.assertNotEqual(glob.glob('%s.gz' % self.gd.mapping_file_name), [])
        os.system('rm %s.gz' % self.gd.mapping_file_name)

    def test_extract(self):
        os.system('cp tests/mock.gz mock.gz')
        self.gd.mapping_file_name = 'mock'
        self.gd.extract()
        # Check if the file can be extracted
        self.assertNotEqual(glob.glob(self.gd.mapping_file_name), [])
        os.system('rm %s' % self.gd.mapping_file_name)

    def test_jsons(self):
        self.gd.path_to_data = 'tmp'
        self.gd.mapping_file_name = 'tmp.mock'
        # Create a mock json file and a mock file list
        os.system('mkdir tmp')
        os.system('touch tmp/tmp.json')
        os.system('echo "Q9Z0S5 foo" > tmp.mock')
        # Check if the clean option removes the old json file
        self.gd.get_jsons(clean=True)
        self.assertEqual(glob.glob('tmp/tmp.json'), [])
        self.assertIsNotNone(glob.glob('tmp/Q9Z0S5.json'))
        os.system('touch tmp/tmp.json')
        os.system('echo "Q9Z0S5 foo" > tmp.mock')
        # Check if without the clean option the old json file remains
        self.gd.get_jsons(clean=False)
        self.assertIsNotNone(glob.glob('tmp/tmp.json'))
        os.system('rm tmp.mock')
        os.system('rm -fr tmp')




