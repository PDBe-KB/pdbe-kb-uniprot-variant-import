import glob
import os
from unittest import TestCase
from uniprot_variant_import.constants import *
from uniprot_variant_import import variation_import

# TODO add tests

mock_data_no_data = {"requestedURL": "https://www.ebi.ac.uk/proteins/api/variation/A0A678Z1Y6",
                     "errorMessage": ["Resources not found"]}

mock_data_no_features = {"accession": "P19851", "entryName": "TKNB_CHICK", "proteinName": "Neurokinin-A",
                         "organismName": "Gallus gallus", "proteinExistence": "Evidence at protein level",
                         "sequence": "HKTDSFVGLM",
                         "sequenceChecksum": "9974136592779295409", "sequenceVersion": 1, "taxid": 9031, "features": []}

mock_data = {"accession": "P39938", "entryName": "RS26A_YEAST", "proteinName": "40S ribosomal protein S26-A",
             "geneName": "RPS26A", "organismName": "Saccharomyces cerevisiae (strain ATCC 204508 / S288c)",
             "proteinExistence": "Evidence at protein level",
             "sequence": "MPKKRASNGRNKKGRGHVKPVRCVNCSKSIPKDKAIKRMAIRNIVEAAAVRDLSEASVYPEYALPKTYNKLHYCVSCAIHARIVRVRSREDRKNRAPPQRPRFNRENKVSPADAAKKAL",
             "sequenceChecksum": "3149736848154420222", "sequenceVersion": 1, "taxid": 559292, "features": [
        {"type": "VARIANT", "alternativeSequence": "T", "begin": "63", "end": "63",
         "xrefs": [{"name": "SGRP", "id": "s07-148408"}], "genomicLocation": "VII:g.148402C>T",
         "locations": [{"loc": "p.Ala63Thr", "seqId": "YGL189C_mRNA", "source": "Ensembl"},
                       {"loc": "c.187G>A", "seqId": "YGL189C_mRNA", "source": "Ensembl"}], "codon": "GCT/ACT",
         "consequenceType": "missense", "wildType": "A", "mutatedType": "T", "predictions": [
            {"predictionValType": "tolerated", "predictorType": "multi coding", "score": 0.4,
             "predAlgorithmNameType": "SIFT", "sources": ["Ensembl"]}], "somaticStatus": 0,
         "sourceType": "large_scale_study"}]}


class TestVariationImport(TestCase):

    def setUp(self):
        self.vi = variation_import.VariationImport(None)

    def test_encoded_value_or_null(self):
        # Check if the correct values are returned
        self.assertEqual(self.vi.encoded_value_or_null({'foo': 'bar'}, 'foo'), 'bar')
        self.assertEqual(self.vi.encoded_value_or_null({'foo': 'bar'}, 'asd'), '')
        self.assertEqual(self.vi.encoded_value_or_null(None, 'foo'), '')
        mock = u'text'
        # Check if it gets rid of unicode
        self.assertEqual(self.vi.encoded_value_or_null({'foo': mock}, 'foo'), 'text')

    def test_run(self):
        self.vi.save_to_file = lambda a, b, c, d: None
        self.vi.save_to_rels_file = lambda a, b, c: None
        self.vi.read_xrefs = lambda a, b, c: 1
        self.vi.read_evidences = lambda a, b, c: 2
        self.vi.read_associations = lambda a, b, c, d, e: (1, 2)
        self.vi.data = {'accession': 'asd', 'features': ['foo', 'bar']}
        # Check if correctly counts features
        self.assertEqual(self.vi.run(), 2)
        self.vi.data = {'features': ['foo', 'bar']}
        # Check if correctly handles missing accession
        self.assertIsNone(self.vi.run())

    def test_read_associations(self):
        self.vi.save_to_file = lambda a, b, c, d: None
        self.vi.save_to_rels_file = lambda a, b, c: None
        self.vi.read_xrefs = lambda a, b, c: 1
        self.vi.read_evidences = lambda a, b, c: 2
        # Check if it returns the output of read_xrefs and read_evidences
        self.assertEqual(self.vi.read_associations(0, 0, {'association': ['foo', 'bar']}, 0, 0), (2, 1))
        # Check if it handles missing data
        self.assertEqual(self.vi.read_associations(0, 0, {'foo': 'bar'}, 0, 0), (0, 0))

    def test_read_xrefs(self):
        self.vi.save_to_file = lambda a, b, c, d: None
        self.vi.save_to_rels_file = lambda a, b, c: None
        # Check if correctly counts xrefs
        self.assertEqual(self.vi.read_xrefs({'xrefs': ['foo', 'bar']}, 'asd', 0), 2)
        # Check if correctly handles missing xrefs
        self.assertEqual(self.vi.read_xrefs({'asd': ['foo', 'bar']}, 'asd', 0), 0)

    def test_read_evidences(self):
        self.vi.save_to_file = lambda a, b, c, d: None
        self.vi.save_to_rels_file = lambda a, b, c: None
        # Check is correctly counts evidences
        self.assertEqual(self.vi.read_evidences(0, {'evidences': [{'code': 'foo'}, {'code': 'bar'}]}, 'id'), 2)
        # Check if correctly handles missing evidences
        self.assertEqual(self.vi.read_evidences(0, {'foo': [{'code': 'foo'}, {'code': 'bar'}]}, 'id'), 0)
        self.assertEqual(
            self.vi.read_evidences(0, {'evidences': [{'code': 'foo'}, {'code': 'bar'}, {'source': {}}]}, 'id'), 3)

    def test_save_to_file(self):
        self.vi.encoded_value_or_null = lambda a, b: a[b]
        # Check if correctly writes out all the required key values
        self.vi.save_to_file({'foo': 'bar', 'asd': 'sad'}, 'id', ['foo'], 'mock.save')
        with open('mock.save') as mock_file:
            for line in mock_file:
                self.assertEqual('id,bar', line.strip())
        os.system('rm mock.save')

    def test_save_to_rels_file(self):
        # Check if correctly writes out the values
        self.vi.save_to_rels_file('foo', 'bar', 'mock.save')
        with open('mock.save') as mock_file:
            for line in mock_file:
                self.assertEqual('foo,bar', line.strip())
        os.system('rm mock.save')
