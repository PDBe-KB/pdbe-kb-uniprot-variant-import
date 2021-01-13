import os
import glob
from datetime import datetime as dt
from uniprot_variant_import.constants import *


class GetData(object):
    """
    These methods can be used to get the latest UniProt mappings from SIFTS, and to use the mappings
    for getting variants data for all the listed UniProt accessions. The variant data is retrieved using
    the UniProt API

    There are 2 main modes:
    1.) "clean", i.e. all the previously downloaded json files get removed and downloaded again
    2.) incremental, i.e. all the old files are kept, and only new json files are downloaded
    """

    def __init__(self, url, path_to_data):
        """
        :param url: String; the URL of the SIFTS mapping file
        :param path_to_data: String; the path to where the UniProt json files will be saved
        """
        self.url = url
        self.path_to_data = path_to_data
        self.mapping_file_name = MAPPING_FILE_NAME

    def make_folder(self):
        """
        Make a folder to save the json files
        :return: 1 or None
        """
        if not(glob.glob(self.path_to_data)):
            os.system('mkdir %s' % self.path_to_data)
            return 1

    def get_file(self):
        """
        Get the latest SIFTS mapping file
        :return: None
        """
        print(dt.now(), 'Removing old SIFTS mapping file...')
        os.system('rm %s' % self.mapping_file_name)
        print(dt.now(), 'Getting latest SIFTS mapping file...')
        os.system('curl -s %s > %s.gz' % (self.url, self.mapping_file_name))

    def extract(self):
        """
        Extract the SIFTS mapping file
        :return: None
        """
        print(dt.now(), 'Extracting mapping file...')
        os.system('gunzip %s.gz' % self.mapping_file_name)

    def get_jsons(self, clean):
        """
        Get all the json files from UniProt
        :param clean: Boolean; if set to True, remove all the previous json files from self.path_to_data
        :return: None
        """
        accessions = []
        if clean:
            # Remove all the previous JSON files if clean is set to True
            os.system('rm %s/*.json' % self.path_to_data)
        with open(self.mapping_file_name) as mapping_file:
            file_count = 0
            for line in mapping_file:
                if not line.startswith('#') and not line.startswith('SP_PRIMARY'):
                    accession = line.split()[0]
                    accessions.append(accession.strip())
        print(dt.now(), "Extracted %i UniProt accessions" % len(accessions))
        for i in range(len(accessions)):
            if not (glob.glob('%s/%s.json' % (self.path_to_data, accessions[i]))):
                file_count += 1
                os.system('curl -s %s/%s > %s/%s.json' % (
                    UNIPROT_API_URL,
                    accessions[i],
                    self.path_to_data,
                    accessions[i]))
        print(dt.now(), "Downloaded %i new JSONs" % file_count)