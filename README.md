# RedcapCdmExport

PyCap and Pandas are required to run this export.

To install all requirements using pip run the following command:

    pip install -r requirements.txt

Local settings need to be specified in an `ExportSettings.py` file before running the program.  An example file is provided (`ExportSettings.py.default`) that can be used as a template.

The code expects a REDCap CDM project (configured to extract DOB, and medications) with an additional data collection instrument for handling identity mapping (with two identity fields: `cog_id` and `anonymized_id`). There are two scripts that must be run in sequential order:

1. `CreateAnonymizedIds.py`
2. `NblChemotherapeutics.py`

The first script performs two tasks.  First, it generates UUIDs and imports these into REDCap in the `anonymized_id` field.  Each time the script is run, `anonymized_id` values will be created and written to REDCap for any records where `anonymized_id` has a null value.  Second, the script outputs an identity mapping file containing two fields: `anonymized_id` and `cog_id`.  This mapping file may then be used to support honest brokering through the COG who can lookup USI values from the `cog_id` values and produce a separate mapping file with `anonymized_id` and USI values that are suitable for linking data sets.

The second script outputs a de-identified csv treatment file containing anonymized_id, the name of the medication ordered, the order status, and the age in days when the order was placed.

Once settings have been specified, one can execute the export by running the following in sequence

    python CreateAnonymizedIds.py

    python NblChemotherapeutics.py

In order to combine the de-identified csv treatment file with USI values, one can run the following

    python CollateDeidTreatmentData.py
