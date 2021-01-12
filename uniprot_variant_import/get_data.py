import os
import glob

# TODO add docstrings
# TODO add comments

class GetData(object):

    def __init__(self, url):
        self.url = url
        self.mapping_file_name = 'uniprot.tsv'

    def make_folder(self):
        if not(glob.glob('data')):
            os.system('mkdir data')

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
            os.system('rm data/*.json')
        with open(self.mapping_file_name) as mapping_file:
            file_count = 0
            for line in mapping_file:
                if not line.startswith('#') and not line.startswith('SP_PRIMARY'):
                    accession = line.split()[0]
                    if not (glob.glob('data/%s.json' % accession.strip())):
                        file_count += 1
                        os.system('curl -s https://www.ebi.ac.uk/proteins/api/variation/%s > data/%s.json' % (
                            accession.strip(),
                            accession.strip()))
            print("Retrieved %i new JSONs" % file_count)