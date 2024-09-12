from redcap import Project
import pandas as pd
import ExportSettings as es


### list of fields to export from REDCap CDM
fields_to_export = es.rc_fields_to_export
### list of medication names to export from REDCap CDM and convert to all uppercase for eventual string comparison
meds_list = list(map(lambda x: x.upper(), es.rc_meds_to_export))
### list of medication statuses to export from REDCap CDM and convert to all uppercase for eventual string comparison
statuses_to_export = list(map(lambda x: x.upper(), es.rc_statuses_to_export))

### set up REDCap connection and export data to a Pandas dataframe
project = Project(es.api_url, es.api_key)
data = project.export_records(format_type="df", fields=fields_to_export)
df = pd.DataFrame(data=data)

### convert medication labels and statuses to all uppercase for eventual string comparison
df['medication_label'] = df['medication_label'].apply(lambda x: str(x).upper())
df['medication_status'] = df['medication_status'].apply(lambda x: str(x).upper())

### create dataframe with only the records that have date of birth (required to calculate age in days)
df_dob=df[~df['dob'].isnull()]['dob']

### create dataframe with only the records that have anonymized_ids (required to create lookup)
df_identity=df[~df[es.rc_anonymized_id_field].isnull()][es.rc_anonymized_id_field]

### populate an output dataframe with the records that have the medication name and statuses of interest
df_out = pd.DataFrame()
for med in meds_list:
    df_out=pd.concat([df_out,df[(df["medication_label"].str.contains(med)==True) & (df["medication_status"].isin(statuses_to_export))]])

### join date of birth and identity_mapping data frames
df_out = df_out.drop(columns=['dob'])
df_out = df_out.join(df_dob)
df_out = df_out.join(df_identity, lsuffix='_l')

### calculate age in days at time of medication
df_out['age_at_medication'] = pd.to_datetime(df_out['medication_date'])-pd.to_datetime(df_out['dob'])
### drop columns that are not needed and reorder columns
df_out = df_out.drop(columns=['dob','medication_date','medication_dosage','redcap_repeat_instance','redcap_repeat_instrument']).sort_values(['record_id','age_at_medication'])
cols = [es.rc_anonymized_id_field, 'medication_label','medication_status','age_at_medication']
df_out = df_out[cols]
### output to csv
df_out.to_csv(es.csv_out, index=False)

