import json
import os

#  TODO change later
with open('./sample.json') as sampleJson:
    sampleData = json.load(sampleJson)

# print(sampleData)


class VariationImport(object):
    # TODO add path to UniProt mapping file or make query to DB
    # TODO change later the data input

    def __init__(self, data):
        self.data = data
        self.unp_variant_csv_path = './UNP_Variant.csv'
        self.xref_csv_path = './UNP_Variant_Xref.csv'
        self.xref_keys = ['name', 'id', 'url', 'alternativeUrl']
        self.unp_variant_keys = ['type', 'description', 'alternativeSequence',
                                 'begin', 'end', 'wildType', 'polyphenPrediction',
                                 'polyphenScore', 'siftPrediction', 'siftScore',
                                 'somaticStatus', 'cytogeneticBand', 'consequenceType',
                                 'genomicLocation', 'clinicalSignificances', 'sourceType']

    def clean_up(self):
        os.system('rm %s' % self.unp_variant_csv_path)

    def run(self):
        accession = self.data['accession']
        feature_count = 0
        for feature in self.data['features']:
            feature_count += 1
            variant_id = '%s_%s' % (accession, feature_count)
            self.save_to_file(feature, variant_id, self.unp_variant_keys, self.unp_variant_csv_path)
            if 'xrefs' in feature.keys():
                xref_count = 0
                for xref in feature['xrefs']:
                    xref_count += 1
                    xref_id = '%s_%s' % (variant_id, xref_count)
                    self.save_to_file(xref, xref_id, self.xref_keys, self.xref_csv_path)

    def save_to_file(self, data, identifier, keyList, csvPath):
        csvFile = open(csvPath, 'a')
        csvFile.write(identifier)
        for key in keyList:
            csvFile.write(';%s' % self.value_or_null(data, key))
        csvFile.write('\n')
        csvFile.close()

    def value_or_null(self, data, key):
        if data and key in data.keys():
            return data[key]
        return ''

vi = VariationImport(sampleData)
vi.clean_up()
vi.run()

# "evidences": [
#     {
#         "code": "ECO:0000313",
#         "source": {
#             "name": "cosmic_study",
#             "id": "418",
#             "url": "https://cancer.sanger.ac.uk/cosmic/study/overview?study_id=418"
#         }
#     }
# ],

# "association": [
#         {
#           "name": "Rubinstein-Taybi syndrome 1 (RSTS1)",
#           "description": "Rubinstein-Taybi syndrome (RSTS) is characterized by distinctive facial features, broad and often angulated thumbs and great toes, short stature, and moderate to severe intellectual disability.",
#           "xrefs": [
#             {
#               "name": "MIM",
#               "id": "180849",
#               "url": "https://www.omim.org/entry/180849"
#             }
#           ],
#           "evidences": [
#             {
#               "code": "ECO:0000313",
#               "source": {
#                 "name": "pubmed",
#                 "id": "20301699",
#                 "url": "https://www.ncbi.nlm.nih.gov/pubmed/20301699",
#                 "alternativeUrl": "https://europepmc.org/abstract/MED/20301699"
#               }
#             },
#             {
#               "code": "ECO:0000313",
#               "source": {
#                 "name": "ClinVar",
#                 "id": "RCV000145718"
#               }
#             }
#           ],
#           "disease": true
#         }
#       ],