import csv
from uniprot_variant_import.constants import *


class VariationImport(object):
    """
    This object is responsible for parsing the data from a JSON file that is in
    the UniProt variant API format, and for extracting relevant information, saving it
    in multiple CSV files.

    These CSV files are used for importing data into Neo4j, and have a defined format.
    """

    def __init__(self, data):
        """
        :param data: JSON data that complies with the UniProt variant API format, see UNIPROT_API_URL for examples
        """
        self.data = data
        self.unp_variant_csv_path = UNP_VARIANT_CSV_PATH
        self.xref_csv_path = UNP_XREF_CSV_PATH
        self.evidence_csv_path = UNP_EVIDENCE_CSV_PATH
        self.association_csv_path = UNP_ASSOCIATION_CSV_PATH
        self.unp_unp_variant_csv_path = UNP_UNP_VARIANT_CSV_PATH
        self.unp_variant_xref_csv_path = UNP_VARIANT_XREF_CSV_PATH
        self.unp_variant_association_csv_path = UNP_VARIANT_ASSOCIATION_CSV_PATH
        self.unp_variant_evidence_csv_path = UNP_VARIANT_EVIDENCE_CSV_PATH
        self.unp_assoc_xref_csv_path = UNP_ASSOCIATION_XREF_CSV_PATH
        self.unp_assoc_evidence_csv_path = UNP_ASSOCIATION_EVIDENCE_CSV_PATH
        self.xref_keys = ['name', 'id', 'url', 'alternativeUrl']
        self.unp_variant_keys = ['type', 'description', 'alternativeSequence',
                                 'begin', 'end', 'wildType', 'polyphenPrediction',
                                 'polyphenScore', 'siftPrediction', 'siftScore',
                                 'somaticStatus', 'cytogeneticBand', 'consequenceType',
                                 'genomicLocation', 'clinicalSignificances', 'sourceType']
        self.evidence_keys = ['code', 'name', 'id', 'url', 'alternativeUrl']
        self.association_keys = ['name', 'description', 'disease']

    def run(self):
        """
        Parses the JSON and writes out the relevant pieces of information. It first handles the actual variant data,
        and then calls a number of other methods to handle the various other parts like xrefs and associations.
        :return: Int or None; the number of variant features found
        """
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
        return feature_count

    def read_associations(self, association_count, evidences_count, feature, variant_id, xref_count):
        """
        Parses the associations sub-dictionary of the data and saves information to files
        :param association_count: Int; used for generating unique identifiers
        :param evidences_count: Int; used for generating unique identifiers
        :param feature: Dict; the data that has the required information
        :param variant_id: String; used for generating unique identifiers
        :param xref_count: Int; used for generating unique identifiers
        :return:
        """
        if 'association' in feature.keys():
            for association in feature['association']:
                association_count += 1
                # Generate an identifier
                association_id = 'assoc_%s_%s' % (variant_id, association_count)
                # Save the relation between the variant and the association using the variant id and association id
                self.save_to_rels_file(variant_id, association_id, self.unp_variant_association_csv_path)
                # Save all the data items from the association dictionary
                self.save_to_file(association, association_id, self.association_keys, self.association_csv_path)
                # Update the count of xrefs (used for generating identifiers)
                xref_count = self.read_xrefs(association, association_id, xref_count, self.unp_assoc_xref_csv_path)
                # Update the count of evidences (used for generating identifiers)
                evidences_count = self.read_evidences(evidences_count, association, association_id, self.unp_assoc_evidence_csv_path)
        return evidences_count, xref_count

    def read_xrefs(self, data, variant_id, xref_count, rels_path):
        """
        Parses the xref sub-dictionary of the data and saves the information to files
        :param data: Dict; sub-dictionary with the xref data
        :param variant_id: String; used for generating unique identifiers
        :param xref_count: Int; used for generating unique identifiers
        :param rels_path: String; used for getting the path to the relevant CSV - Note: there are 2 different CSVs
        :return: Int; the count of xrefs in the data
        """
        if 'xrefs' in data.keys():
            for xref in data['xrefs']:
                xref_count += 1
                xref_id = 'xref_%s_%s' % (variant_id, xref_count)
                self.save_to_file(xref, xref_id, self.xref_keys, self.xref_csv_path)
                self.save_to_rels_file(variant_id, xref_id, rels_path)
        return xref_count

    def read_evidences(self, evidences_count, data, variant_id, rels_path):
        """
        Parses the evidences sub-dictionary of the data and saves the information to files
        :param evidences_count: Int; used for generating unique identifiers
        :param data: Dict; sub-dictionary with the evidences data
        :param variant_id: String; used for generating unique identifiers
        :param rels_path: String; used for getting the path to the relevant CSV - Note: there are 2 different CSVs
        :return: Int; the count of evidences in the data
        """
        if 'evidences' in data.keys():
            for evidence in data['evidences']:
                evidences_count += 1
                evidence_id = 'evid_%s_%s' % (variant_id, evidences_count)
                flat_evidence = {}
                if 'source' in evidence.keys():
                    flat_evidence = evidence['source']
                flat_evidence['code'] = self.value_or_null(evidence, 'code')
                self.save_to_file(flat_evidence, evidence_id, self.evidence_keys, self.evidence_csv_path)
                self.save_to_rels_file(variant_id, evidence_id, rels_path)
        return evidences_count

    def save_to_file(self, data, identifier, key_list, csv_path):
        """
        Write out all the data from a dictionary to a CSV file
        :param data: Dict; data to be saved
        :param identifier: String; identifier of the data
        :param key_list: Array; a list of keys (Strings) to be used from the data dictionary
        :param csv_path: String; path to the CSV file
        :return: None
        """
        csv_file = open(csv_path, 'a')
        csv_writer = csv.writer(csv_file, dialect='excel')
        row = [identifier]
        for key in key_list:
            row.append(self.value_or_null(data, key))
        csv_writer.writerow(row)
        csv_file.close()

    def save_to_rels_file(self, x, y, csv_path):
        """
        Write out data to a CSV file
        :param x: String; data to write out
        :param y: String; data to write out
        :param csv_path: String; path to the CSV file
        :return: None
        """
        csv_file = open(csv_path, 'a')
        csv_writer = csv.writer(csv_file, dialect='excel')
        csv_writer.writerow((x, y))
        csv_file.close()

    def value_or_null(self, data, key):
        """
        Checks if there is data for a given key
        :param data: Dict; a sub-dictionary of the UniProt data
        :param key: String; a key
        :return: String; the value or ''
        """
        if data and key in data.keys():
            return str(data[key])
        return ''
