import csv

# TODO add progress % output
# TODO move the file name strings into constants.py
# TODO add docstrings
# TODO add comments

class VariationImport(object):

    def __init__(self, data):
        self.data = data
        self.unp_variant_csv_path = './UNP_Variant.csv'
        self.xref_csv_path = './UNP_Variant_Xref.csv'
        self.evidence_csv_path = './UNP_Variant_Evidence.csv'
        self.association_csv_path = './UNP_Association.csv'
        self.unp_unp_variant_csv_path = './UNP_UNP_Variant_Rels.csv'
        self.unp_variant_xref_csv_path = './UNP_Variant_Xref_Rels.csv'
        self.unp_variant_association_csv_path = './UNP_Variant_Association_Rels.csv'
        self.unp_variant_evidence_csv_path = './UNP_Variant_Evidence_Rels.csv'
        self.unp_assoc_xref_csv_path = './UNP_Association_Xref_Rels.csv'
        self.unp_assoc_evidence_csv_path = './UNP_Association_Evidence_Rels.csv'
        self.xref_keys = ['name', 'id', 'url', 'alternativeUrl']
        self.unp_variant_keys = ['type', 'description', 'alternativeSequence',
                                 'begin', 'end', 'wildType', 'polyphenPrediction',
                                 'polyphenScore', 'siftPrediction', 'siftScore',
                                 'somaticStatus', 'cytogeneticBand', 'consequenceType',
                                 'genomicLocation', 'clinicalSignificances', 'sourceType']
        self.evidence_keys = ['code', 'name', 'id', 'url', 'alternativeUrl']
        self.association_keys = ['name', 'description', 'disease']

    def run(self):
        if 'accession' not in self.data.keys():
            return None
        accession = self.data['accession']
        feature_count = 0
        xref_count = 0
        evidences_count = 0
        association_count = 0
        for feature in self.data['features']:
            feature_count += 1
            variant_id = 'var_%s_%s' % (accession, feature_count)
            self.save_to_rels_file(accession, variant_id, self.unp_unp_variant_csv_path)
            self.save_to_file(feature, variant_id, self.unp_variant_keys, self.unp_variant_csv_path)
            xref_count = self.read_xrefs(feature, variant_id, xref_count, self.unp_variant_xref_csv_path)
            evidences_count = self.read_evidences(evidences_count, feature, variant_id, self.unp_variant_evidence_csv_path)
            evidences_count, xref_count = self.read_associations(association_count, evidences_count, feature,
                                                                 variant_id, xref_count)

    def read_associations(self, association_count, evidences_count, feature, variant_id, xref_count):
        if 'association' in feature.keys():
            for association in feature['association']:
                association_count += 1
                association_id = 'assoc_%s_%s' % (variant_id, association_count)
                self.save_to_rels_file(variant_id, association_id, self.unp_variant_association_csv_path)
                self.save_to_file(association, association_id, self.association_keys, self.association_csv_path)
                xref_count = self.read_xrefs(association, association_id, xref_count, self.unp_assoc_xref_csv_path)
                evidences_count = self.read_evidences(evidences_count, association, association_id,
                                                      self.unp_assoc_evidence_csv_path)
        return evidences_count, xref_count

    def read_xrefs(self, data, variant_id, xref_count, rels_csv_path):
        if 'xrefs' in data.keys():
            for xref in data['xrefs']:
                xref_count += 1
                xref_id = 'xref_%s_%s' % (variant_id, xref_count)
                self.save_to_file(xref, xref_id, self.xref_keys, self.xref_csv_path)
                self.save_to_rels_file(variant_id, xref_id, rels_csv_path)
        return xref_count

    def read_evidences(self, evidences_count, data, variant_id, rels_csv_path):
        if 'evidences' in data.keys():
            for evidence in data['evidences']:
                evidences_count += 1
                evidence_id = 'evid_%s_%s' % (variant_id, evidences_count)
                flat_evidence = {}
                if 'source' in evidence.keys():
                    flat_evidence = evidence['source']
                flat_evidence['code'] = self.value_or_null(evidence, 'code')
                self.save_to_file(flat_evidence, evidence_id, self.evidence_keys, self.evidence_csv_path)
                self.save_to_rels_file(variant_id, evidence_id, rels_csv_path)
        return evidences_count

    def save_to_file(self, data, identifier, key_list, csv_path):
        csv_file = open(csv_path, 'a')
        csv_writer = csv.writer(csv_file, dialect='excel')
        row = [identifier]
        for key in key_list:
            row.append(self.value_or_null(data, key))
        csv_writer.writerow(row)
        csv_file.close()

    def save_to_rels_file(self, x, y, csv_path):
        csv_file = open(csv_path, 'a')
        csv_writer = csv.writer(csv_file, dialect='excel')
        csv_writer.writerow((x, y))
        csv_file.close()

    def value_or_null(self, data, key):
        if data and key in data.keys():
            if type(data[key]) is 'unicode':
                data[key] = data[key].encode('utf-8')
            return data[key]
        return ''