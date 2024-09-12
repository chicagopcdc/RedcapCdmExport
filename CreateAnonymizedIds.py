import uuid
from redcap import Project
import pandas as pd
import ExportSettings as es


### list of fields to export from REDCap CDM
fields_to_export = [es.rc_cog_id_field, es.rc_anonymized_id_field]

### set up REDCap connection and export data to a Pandas dataframe
project = Project(es.api_url, es.api_key)
data = project.export_records(format_type="df", fields=fields_to_export)
df = pd.DataFrame(data=data)

### create anonymized ids
df[es.rc_anonymized_id_field] = [uuid.uuid4() for _ in range(len(df.index))]

### import anonymized ids to REDCap
import_count = project.import_records(import_format="df", to_import=df)
print(import_count)

### create identity mapping output file format
df_out = df.drop(columns=['redcap_repeat_instrument','redcap_repeat_instance'])

### output to csv
df_out.to_csv(es.mapping_file_out, index=False)

