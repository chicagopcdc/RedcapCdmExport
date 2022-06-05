from redcap import Project
import pandas as pd
import ExportSettings as es


### list of fields to export from REDCap CDM
fields_to_export=['record_id','dob','medication_label','medication_date','medication_dosage','medication_status']
### list of medication names to export from REDCap CDM
meds_list = ['CYCLOPHOSPHAMIDE','TOPOTECAN','ETOPOSIDE','CISPLATIN','DOXORUBICIN','VINCRISTINE','MESNA','BUSULFAN','MELPHALAN','FILGRASTIM','CARBOPLATIN','ISOTRETINOIN','DINUTUXIMAB','SARGRAMOSTIM','ALDESLEUKIN','ISOTRETINOIN']
### list of medication statuses to export from REDCap CDM
statuses_to_export=['completed']

### set up REDCap connection and export data to a Pandas dataframe
project = Project(es.api_url, es.api_key)
data = project.export_records(format_type="df", fields=fields_to_export)
df = pd.DataFrame(data=data)

### create dataframe with only the records that have date of birth
df_dob=df[~df['dob'].isnull()]['dob']
### populate an output dataframe with the records that have the medication name and statuses of interest
df_out = pd.DataFrame()
for med in meds_list:
    df_out=df_out.append(df[(df["medication_label"].str.contains(med)==True) & (df["medication_status"].isin(statuses_to_export))])
df_out = df_out.drop(columns=['dob'])
df_out = df_out.join(df_dob)
### calculate age in days at time of medication
df_out['age_at_medication'] = pd.to_datetime(df_out['medication_date'])-pd.to_datetime(df_out['dob'])
### drop columns that are not needed
df_out = df_out.drop(columns=['dob','medication_date','redcap_repeat_instance','redcap_repeat_instrument']).sort_values(['record_id','age_at_medication'])
### output to csv
df_out.to_csv(es.csv_out)

