# RedcapCdmExport

PyCap is required to run this export.  To install PyCap, execute the following:

    pip install PyCap 

Local settings need to be specified in the `ExportSettings.py` file before running the program.

The code expects a REDCap CDM project (configured to extract DOB, and medications).  The script outputs a de-identified csv file containing REDCap record_id, the name of the medication ordered, the order status, and the age in days when the order was placed.

Once settings have been specified, one can execute the export by running the following:

    python NblChemotherapeutics.py
