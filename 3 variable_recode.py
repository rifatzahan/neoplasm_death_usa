import pandas as pd
import numpy as np
from matplotlib_venn import venn3
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset (adjust file path as needed)
df = pd.read_csv(r"C:\Users\rzahan\OneDrive - University of Saskatchewan\LUC\Research\Sharuf Research\Cancer Data\US_Mortality_2019_2023_malignant_neoplasms_with_subtypes.csv", low_memory=False)

# Boolean series
# Create boolean columns for selected subtypes
df['is_breast'] = df['malignant_type'] == 'breast'
df['is_lung'] = df['malignant_type'] == 'trachea_bronchus_lung'
df['is_prostate'] = df['malignant_type'] == 'prostate'
df['is_colorectal'] = df['malignant_type'] == 'colon_rectum_anus'
df['is_pancreas'] = df['malignant_type'] == 'pancreas'
df['is_leukemia'] = df['malignant_type'] == 'leukemia'
df['is_other_malignant'] = df['malignant_type'] == 'other_malignant'


# Calculate mutually exclusive
only_breast = df['is_breast'].sum()
only_lung = df['is_lung'].sum()
only_prostate = df['is_prostate'].sum()
only_colorectal = df['is_colorectal'].sum()
only_pancreas = df['is_pancreas'].sum()
only_leukemia = df['is_leukemia'].sum()
only_other = df['is_other_malignant'].sum()

print("Breast cancer deaths:", only_breast)
print("Lung cancer deaths:", only_lung)
print("Prostate cancer deaths:", only_prostate)
print("Colorectal cancer deaths:", only_colorectal)
print("Pancreatic cancer deaths:", only_pancreas)
print("Leukemia deaths:", only_leukemia)
print("Other malignant neoplasms:", only_other)

# # Example (in case of multi-classification in the future)
# df['breast_and_lung'] = df['is_breast'] & df['is_lung']
# print("Breast + Lung:", df['breast_and_lung'].sum())


summary = {
    "breast": only_breast,
    "lung": only_lung,
    "prostate": only_prostate,
    "colorectal": only_colorectal,
    "pancreas": only_pancreas,
    "leukemia": only_leukemia,
    "other_malignant": only_other
}

print("\nSummary of Malignant Neoplasm Deaths by Subtype:")
for k, v in summary.items():
    print(f"{k.capitalize():<20}: {v}")


# Convert all column names to lowercase for consistency
# df.columns = df.columns.str.strip()

# Recode SEX (from location 69)
sex_map = {
    ' M': "Male",
    ' F': "Female"
}
df['Sex'] = df['Sex'].map(sex_map)


# Create a dictionary to map the resident status codes to their corresponding descriptions
resident_status_mapping = {
    1: 'Residents',
    2: 'Intrastate Non-Residents',
    3: 'Interstate Non-Residents',
    4: 'Foreign Residents'
}

# Recode 'resident_status' based on the mapping
df['Resident_Status'] = df['Resident_Status'].map(resident_status_mapping)

# Define a new mapping for broader occupation groups

occupation_group_mapping = {
    1: 'Management and Business',
    2: 'Management and Business',
    3: 'Technology and Science',
    4: 'Technology and Science',
    5: 'Technology and Science',
    6: 'Legal and Social Services',
    7: 'Legal and Social Services',
    8: 'Education and Arts',
    9: 'Education and Arts',
    10: 'Technology and Science',
    11: 'Technology and Science',
    12: 'Service and Protective',
    13: 'Service and Protective',
    14: 'Service and Protective',
    15: 'Service and Protective',
    16: 'Management and Business',
    17: 'Management and Business',
    18: 'Labor and Production',
    19: 'Labor and Production',
    20: 'Labor and Production',
    21: 'Labor and Production',
    22: 'Labor and Production',
    24: 'Military',
    25: 'Miscellaneous and Other',
    26: 'Miscellaneous and Other'
}


# don't get scared. There are tons of missing values for occupation, hispanic origin, and so on.
# Replace blank spaces with NaN or an appropriate placeholder (e.g., 0)
df['Occupation'] = df['Occupation_Recode'].replace(' ', np.nan)

# Convert to integers (with NaN handled)
df['Occupation'] = pd.to_numeric(df['Occupation'], errors='coerce')

# Reapply the mapping for grouped occupation
df['Occupation'] = df['Occupation'].map(occupation_group_mapping)

# Create a dictionary to map the education codes to their corresponding descriptions
education_mapping = {
    1: 'Less than High School',
    2: 'Less than High School',
    3: 'High School / GED',
    4: 'Some College',
    5: 'Associate and Bachelors Degree',
    6: 'Associate and Bachelors Degree',
    7: 'Graduate Degrees',
    8: 'Graduate Degrees'
}

# Recode 'education' based on the mapping
df['Education'] = df['Education'].map(education_mapping)




# Create a dictionary to map the month codes to their corresponding month names
month_mapping = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

# Recode 'month_of_death' based on the mapping
df['Month_Of_Death'] = df['Month_Of_Death'].map(month_mapping)


# Step 1: Strip spaces and convert to integer
df['Race_Recode_6'] = df['Race_Recode_6'].astype(str).str.strip()
df['Race_Recode_6'] = pd.to_numeric(df['Race_Recode_6'], errors='coerce')

# Step 2: Map to race categories
race_mapping = {
    1: 'White (only)',
    2: 'Black (only)',
    3: 'American Indian and Alaska Native (only)',
    4: 'Asian (only)',
    5: 'Native Hawaiian or Other Pacific Islander (only)',
    6: 'More than one race'
}

df['Race'] = df['Race_Recode_6'].map(race_mapping)



# Create a dictionary to map the hispanic_origin codes to their corresponding descriptions
hispanic_origin_mapping = {
    1: 'Mexican',
    2: 'Puerto Rico',
    3: 'Cuban',
    4: 'Dominican',
    5: 'Central American',
    6: 'South American',
    7: 'Other or Unknown Hispanic',
    8: 'Non-Hispanic White (only)',
    9: 'Non-Hispanic Black (only)',
    10: 'Non-Hispanic American Indian and Alaska Native (only)',
    11: 'Non-Hispanic Asian (only)',
    12: 'Non-Hispanic Native Hawaiian or Other Pacific Islander (only)',
    13: 'Non-Hispanic more than one race',
    14: 'Hispanic origin unknown or not stated'
}

# Recode 'hispanic_origin' based on the mapping
df['Hispanic_Origin'] = df['Hispanic_Origin'].map(hispanic_origin_mapping)


# Recode Age_Recode_12
age_recode_map = {
    '01': "<= 14 years",
    '02': "<= 14 years",
    '03': "<= 14 years",
    '04': "15 - 24 years",
    '05': "25 - 34 years",
    '06': "35 - 44 years",
    '07': "45 - 54 years",
    '08': "55 - 64 years",
    '09': "65 - 74 years",
    '10': "75 - 84 years",
    '11': "85 years and older",
    '12': "Age not stated"
}

df['Age Group'] = df['Age_Recode_12'].astype(str).str.zfill(2)  # Pad single digits
df['Age Group'] = df['Age Group'].map(age_recode_map)



# Drop rows with age not stated
# df = df[df['Age Group'] != "Age not stated"]
# df = df[df['Age Group'] != "<= 14 years"] # after removing occupation and education missing values, this category had no values


# Recode MARITAL STATUS (from location 84)
marital_status_map = {
    ' S': "Never Married",
    ' M': "Married",
    ' W': "Widowed",
    ' D': "Divorced",
    ' U': "Unknown"
}
df['Marital Status'] = df['Marital_Status'].map(marital_status_map)

# df = df[df['Marital Status'] != "Unknown"]

df['Data Year'] = df['Data_Year'].astype(str)

# View a few rows to confirm
# print(df[['variable names']].head())

# Export to CSV if needed
output_path = r"C:\Users\rzahan\OneDrive - University of Saskatchewan\LUC\Research\Sharuf Research\Cancer Data\US_Mortality_2019_2023_neoplasm_with_subtypes_recoded.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

print(f"Recoded data exported to: {output_path}")
