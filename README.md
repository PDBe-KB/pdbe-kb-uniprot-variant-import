# PDBe-KB Variant Importer

[![Build Status](https://travis-ci.com/PDBe-KB/pdbe-kb-uniprot-variant-import.svg?branch=master)](https://travis-ci.com/PDBe-KB/pdbe-kb-uniprot-variant-import)
[![codecov](https://codecov.io/gh/PDBe-KB/pdbe-kb-uniprot-variant-import/branch/master/graph/badge.svg?token=y3ECW921dY)](https://codecov.io/gh/PDBe-KB/pdbe-kb-uniprot-variant-import)
[![Maintainability](https://api.codeclimate.com/v1/badges/0d310eccab1721310e31/maintainability)](https://codeclimate.com/github/PDBe-KB/pdbe-kb-uniprot-variant-import/maintainability)

## Basic information

This repository contains code for a process that is used by [PDBe-KB](https://pdbe-kb.org) to retrieve, parse, process and convert variant data from UniProt so that it can be integrated with the core PDB data in the [PDBe graph database](https://pdbe.org/graph-schema).

In particular, the process will:
 
* Retrieve the latest mapping between PDB and UniProt, using SIFTS; 
* Query the UniProt API for retrieving all the variant-related data for UniProt accessions that have PDB entries mapped to them; 
* Extract and convert the data to CSV format that can be used by Neo4j to import the data into a graph database.

## Usage

Clone this repository
```
git clone https://github.com/PDBe-KB/pdbe-kb-uniprot-variant-import.git
```
Run the process
```
python3 run.py
```
1.) This will first download and unzip the latest SIFTS mapping via the URL defined in "SIFTS_URL_TO_MAPPING".

2.) Next, it will extract all the UniProt accessions from the mapping file

3.) Then it pulls all the data from UniProt API via the URL defined in "UNIPROT_API_URL", using curl to save the JSON files. The files are saved in the "data" folder

4.) Finally, it parses all the JSON files, extracts the relevant data and exports them to CSV in a format that is expected by Neo4j for encoding nodes and edges. The files are saved in the top folder
## Dependencies

None for running it. 

For development: codecov, pytest-cov

## Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/PDBe-KB/pdbe-kb-uniprot-variant-import/tags).

## Authors
* **Mihaly Varadi** - *Initial work* - [mvaradi](https://github.com/mvaradi)

See also the list of [contributors](https://github.com/PDBe-KB/pdbe-kb-uniprot-variant-import/contributors) who participated in this project.

## License
This project is licensed under the Apache License (version 2.) - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
We would like to acknowledge the PDBe and UniProt teams for their help both via coding and consultation.