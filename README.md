# RedcapCdmExport

PyCap is required to run this export.  To install PyCap, execute the following:

    pip install PyCap 

Local settings need to be specified in the `ExportSettings.py` file before running the program.

The code expects a REDCap CDM project (configured to extract DOB, and medications) with an additional `identity_mapping` instrument containing a single `text` field named `cog_id` that holds the COG Identifier of the participant.  This field will be used when creating the CSV export rather than the medical record number.

Once settings have been specified, one can execute the export by running the following:

    python NblChemotherapeutics.py
