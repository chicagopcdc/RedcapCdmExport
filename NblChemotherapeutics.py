from redcap import Project
import pandas as pd
import ExportSettings as es

project = Project(es.api_url, es.api_key)

fields_to_export=['record_id','dob','medication_label','medication_date','medication_dosage','medication_status']

data = project.export_records(format_type="df", fields=fields_to_export)

df = pd.DataFrame(data=data)
df_dob=df[~df['dob'].isnull()]['dob']
df_out = pd.DataFrame()

meds_list = ['CYCLOPHOSPHAMIDE','TOPOTECAN','ETOPOSIDE','CISPLATIN','DOXORUBICIN','VINCRISTINE','MESNA','BUSULFAN','MELPHALAN','FILGRASTIM','CARBOPLATIN','ISOTRETINOIN']

for med in meds_list:
    df_out=df_out.append(df[df["medication_label"].str.contains(med)==True])
df_out = df_out.drop(columns=['dob'])
df_out = df_out.join(df_dob)
df_out['age_at_medication'] = pd.to_datetime(df_out['medication_date'])-pd.to_datetime(df_out['dob'])
df_out = df_out.drop(columns=['dob','medication_date','redcap_repeat_instance','redcap_repeat_instrument']).sort_values(['record_id','age_at_medication'])
df_out.to_csv(es.csv_out)

