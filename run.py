import json
import glob
from uniprot_variant_import import get_data, variation_import
from uniprot_variant_import.constants import *

# TODO add argument support for clean run using getops or sys.argv

def main(clean=False):
    """
    This function:
    1.) Downloads the latest SIFTS mappings
    2.) Downloads all the new UniProt data files using the UniProt API
        Note: if clean=True, the process will remove all the old .json files first
    3.) Converts the variant data from the UniProt .json files into .csv format
    :return: None
    """

    print('\nSTARTING UNIPROT VARIANT RETRIEVAL AND CONVERSION')

    """
    Get the latest UniProt mapping from SIFTS and
    retrieve all the JSONs with the variation data
    """
    gd = get_data.GetData(SIFTS_URL_TO_MAPPING, 'data')
    gd.make_folder()
    gd.get_file()
    gd.extract()
    gd.get_jsons(clean)

    """
    Convert the variation data JSONs files to
    CSV files for loading into PDBe-KB graph
    database
    """

    print("Converting JSON files to CSV...")

    for json_path in glob.glob('data/*.json'):
        with open(json_path) as json_file:
            try:
                data = json.load(json_file)
                vi = variation_import.VariationImport(data)
                vi.run()
            except:
                continue

    print("DONE\n")


if __name__ == "__main__":
    main()