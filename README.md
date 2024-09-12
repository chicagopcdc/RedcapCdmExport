# RedcapCdmExport

PyCap and Pandas are required to run this export.
  
To install PyCap, execute the following:

    pip install PyCap 

To install Pandas, execute the following:

    pip install Pandas 

Local settings need to be specified in an `ExportSettings.py` file before running the program.  An example file is provided (`ExportSettings.py.default`) that can be used as a template.

The code expects a REDCap CDM project (configured to extract DOB, and medications).  The script outputs a de-identified csv file containing REDCap record_id, the name of the medication ordered, the order status, and the age in days when the order was placed.

Once settings have been specified, one can execute the export by running the following:

    python NblChemotherapeutics.py
