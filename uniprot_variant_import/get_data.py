import os
import glob
from uniprot_variant_import.constants import *

# TODO add docstrings
# TODO add comments

class GetData(object):

    def __init__(self, url, path_to_data):
        self.url = url
        self.path_to_data = path_to_data
        self.mapping_file_name = MAPPING_FILE_NAME

    def make_folder(self):
        if not(glob.glob(self.path_to_data)):
            os.system('mkdir %s' % self.path_to_data)
            return 1

    def get_file(self):
        print('Removing old SIFTS mapping file...')
        os.system('rm %s' % self.mapping_file_name)
        print('Getting latest SIFTS mapping file...')
        os.system('curl -s %s > %s.gz' % (self.url, self.mapping_file_name))

    def extract(self):
        print('Extracting mapping file...')
        os.system('gunzip %s.gz' % self.mapping_file_name)

    def get_jsons(self, clean):
        if clean:
            # Remove all the previous JSON files if clean is set to True
            os.system('rm %s/*.json' % self.path_to_data)
        with open(self.mapping_file_name) as mapping_file:
            file_count = 0
            for line in mapping_file:
                if not line.startswith('#') and not line.startswith('SP_PRIMARY'):
                    accession = line.split()[0]
                    if not (glob.glob('%s/%s.json' % (self.path_to_data, accession.strip()))):
                        file_count += 1
                        os.system('curl -s %s/%s > %s/%s.json' % (
                            UNIPROT_API_URL,
                            accession.strip(),
                            self.path_to_data,
                            accession.strip()))
            print("Retrieved %i new JSONs" % file_count)