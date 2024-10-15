import os
import uuid
from redcap import Project
import pandas as pd
import ExportSettings as es


def main():
    try:
        ### list of fields to export from REDCap CDM
        fields_to_export = [es.rc_cog_id_field, es.rc_anonymized_id_field]

        ### set up REDCap connection and export data to a Pandas dataframe
        project = Project(es.api_url, es.api_key)
        data = project.export_records(format_type="df", fields=fields_to_export)
        df = pd.DataFrame(data=data)

        ### create separate data frames for empty and non-empty anonymous id records
        ### records where anonmized id field is empty
        df_null_anonymized_id = df[df[es.rc_anonymized_id_field].isnull()]
        ### records where anonmized id field is not empty
        df_notnull_anonymized_id = df[df[es.rc_anonymized_id_field].notnull()]

        if (len(df_null_anonymized_id.index) > 0):
            ### create anonymized ids
            df_null_anonymized_id[es.rc_anonymized_id_field] = [uuid.uuid4() for _ in range(len(df_null_anonymized_id.index))]
            
            ### import anonymized ids to REDCap
            import_count = project.import_records(import_format="df", to_import=df)
            print(str(import_count) + " records with previously unassigned anonymous ids found.")
        else:
            print("No records with previously unassigned anonymous ids (i.e. " + es.rc_anonymized_id_field + ") found.")

        ### combine separate data frames into a single data frame for all records
        df_out = pd.concat([df_null_anonymized_id, df_notnull_anonymized_id])

        ### create identity mapping output file format
        df_out = df_out.drop(columns=['redcap_repeat_instrument','redcap_repeat_instance'])

        ### output identity map to csv
        df_out.to_csv(es.cog_id_mapping_file_out, index=False)
        print(str(len(df_out.index)) + " records written to file " + es.cog_id_mapping_file_out)

    except Exception as e:
        print("Uncaught error: " + str(e))

if __name__ == '__main__':
    main()
