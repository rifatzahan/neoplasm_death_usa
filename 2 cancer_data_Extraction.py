import pandas as pd

# Define the file path
csv_file_path = r"C:\Users\rzahan\OneDrive - University of Saskatchewan\LUC\Research\Sharuf Research\Cancer Data\US_Mortality_2019_2023.csv"
df = pd.read_csv(csv_file_path, low_memory=False)

# Clean up column names
df.columns = df.columns.str.strip()

# === Clean function: Normalize ICD codes ===
def normalize_icd(code):
    return str(code).strip().replace('.', '').upper()

# === Extract 3-character root of ICD-10 ===
def icd_root(code):
    return normalize_icd(code)[:3]

# === All malignant ICD-10 3-digit codes ===
malignant_icd_codes = {
    'C00', 'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 
    'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C30', 'C31', 'C32', 'C33', 'C34', 'C37', 'C38',
    'C39', 'C40', 'C41', 'C43', 'C44', 'C45', 'C46', 'C47', 'C48', 'C49', 'C50', 'C51', 'C52', 'C53', 'C54', 'C55', 'C56',
    'C57', 'C60', 'C61', 'C62', 'C63', 'C64', 'C65', 'C66', 'C67', 'C68', 'C69', 'C70', 'C71', 'C72', 'C73', 'C74', 'C75',
    'C76', 'C77', 'C78', 'C79', 'C80', 'C81', 'C82', 'C83', 'C84', 'C85', 'C88', 'C90', 'C91', 'C92', 'C93', 'C94', 'C95', 
    'C96', 'C97'
}

# === Identify malignant neoplasm deaths ===
df['icd_root'] = df['icd_10'].apply(icd_root)
df['is_malignant_neoplasm'] = df['icd_root'].isin(malignant_icd_codes)

# === Define other_malignant codes ===
def expand_icd_range(start, end):
    return [f"C{str(i).zfill(2)}" for i in range(start, end + 1)]

other_malignant_icd_codes = (
    expand_icd_range(0, 15) +
    ['C17'] +
    expand_icd_range(22, 24) +
    expand_icd_range(26, 32) +
    expand_icd_range(37, 49) +
    ['C51', 'C52'] +
    expand_icd_range(57, 60) +
    ['C62', 'C63'] +
    expand_icd_range(69, 81) +
    ['C88', 'C90'] +
    expand_icd_range(96, 97)
)

# === Subtype dictionary ===
malignant_subtypes = {
    'stomach': ['C16'],
    'colon_rectum_anus': ['C18', 'C19', 'C20', 'C21'],
    'pancreas': ['C25'],
    'trachea_bronchus_lung': ['C33', 'C34'],
    'breast': ['C50'],
    'cervix_uterus_ovary': ['C53', 'C54', 'C55', 'C56'],
    'prostate': ['C61'],
    'urinary_tract': ['C64', 'C65', 'C66', 'C67', 'C68'],
    'non_hodgkin_lymphoma': ['C82', 'C83', 'C84', 'C85'],
    'leukemia': ['C91', 'C92', 'C93', 'C94', 'C95'],
    'other_malignant': other_malignant_icd_codes
}

# === Build reverse mapping for fast lookup ===
prefix_to_subtype = {}
for subtype, code_list in malignant_subtypes.items():
    for code in code_list:
        prefix_to_subtype[code] = subtype

# === Classify subtype ===
df['malignant_type'] = df.apply(
    lambda row: prefix_to_subtype.get(row['icd_root'], 'unspecified') if row['is_malignant_neoplasm'] else None,
    axis=1
)

# === Save files ===
# File with only malignant neoplasms
malignant_df = df[df['is_malignant_neoplasm']]
malignant_path = csv_file_path.replace(".csv", "_malignant_neoplasms_with_subtypes.csv")
malignant_df.to_csv(malignant_path, index=False)

print(f"✅ Malignant neoplasm data with subtypes saved to: {malignant_path}")
