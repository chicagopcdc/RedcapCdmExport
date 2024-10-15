import pandas as pd
import ExportSettings as es

def main():
    try:

        identity_map_filename = es.usi_mapping_file_in
        treatment_data_filename = es.treatment_file_out

        df_identity = pd.read_csv(identity_map_filename)
        print(str(len(df_identity.index)) + " identity mapping records read.")
        df_treatment_data = pd.read_csv(treatment_data_filename)
        print(str(len(df_treatment_data.index)) + " treatment records read.")

        df_collated = pd.merge(left=df_identity, right=df_treatment_data, how='inner')

        df_collated.to_csv(es.usi_bound_treatment_file_out, index=False, columns=[es.usi_field, 'medication_label', 'medication_status', 'age_at_medication']) 
        print(str(len(df_collated.index)) + " USI bound treatment records written to " + es.usi_bound_treatment_file_out)
        print(str(len(df_collated[es.usi_field].unique())) + " unique patients with treatment data out of a total of " + str(len(df_identity.index)) + " patients")

    except Exception as e:
        print("Uncaught error: " + str(e))

if __name__ == '__main__':
    main()
