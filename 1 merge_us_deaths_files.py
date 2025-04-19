import os

# Directory where all the files are stored
data_dir = r"C:\Users\rzahan\OneDrive - University of Saskatchewan\LUC\Research\Sharuf Research"


# List of all data files from 2019 to 2023
data_files = [
    "VS19MORT.DUSMCPUB_r20210304", 
    "VS20MORT.DUSMCPUB_r20220105", 
    "VS21MORT.DUSMCPUB_r20230320.txt", 
    "VS22MORT.DUSMCPUB_r20240307", 
    "VS23MORT.DUSMCPUB_r20241030"
]



# Output CSV file
output_dir =  r"C:\Users\rzahan\OneDrive - University of Saskatchewan\LUC\Research\Sharuf Research\Cancer Data"
output_file_path = os.path.join(output_dir, "US_Mortality_2019_2023.csv")
fileOutObj = open(output_file_path, "w")

# Write header
fileOutObj.write('Resident_Status, Occupation_Recode, Education, Month_Of_Death, Sex, Age_Value, Age_Recode_12, Place_Of_Death, Marital_Status, DOW_of_Death, ' +
                 'Data_Year, Injured_At_Work, Manner_Of_Death, Method_Of_Disposition, Autopsy, Activity_Code, Place_Of_Causal_Injury, icd_10, ' +
                 'MCODs, Race_Recode_6, Hispanic_Origin\n')

# Process each file
for filename in data_files:
    filepath = os.path.join(data_dir, filename)
    try:
        with open(filepath, 'r') as fileObj:
            for line in fileObj:
                try:
                    # Extract Record-Axis MCODs (columns 344–443)
                    record_axis_mcods = []
                    for i in range(0, 100, 4):  # 25 codes * 4 chars
                        code = line[343 + i: 343 + i + 4].strip()
                        if code:
                            record_axis_mcods.append(code)
                    mcod_str = ';'.join(record_axis_mcods)

                    # Build output string
                    outStr = (
                        line[19].strip() + ', ' +
                        line[809:811].strip() + ', ' +
                        line[62].strip() + ', ' +
                        line[64:66].strip() + ', ' +
                        line[68].strip() + ', ' +
                        line[69:73].strip() + ', ' +
                        line[78:80].strip() + ', ' +
                        line[82].strip() + ', ' +
                        line[83].strip() + ', ' +
                        line[84].strip() + ', ' +
                        line[101:105].strip() + ', ' +
                        line[105].strip() + ', ' +
                        line[106].strip() + ', ' +
                        line[107].strip() + ', ' +
                        line[108].strip() + ', ' +
                        line[143].strip() + ', ' +
                        line[144].strip() + ', ' +
                        line[145:149].strip() + ', ' +
                        mcod_str + ', ' +
                        line[449].strip() + ', ' +
                        line[486:488].strip() + '\n'
                    )

                    fileOutObj.write(outStr)

                except IndexError:
                    print(f"Line skipped in file {filename}: Data out of bounds")
                    continue

    except FileNotFoundError:
        print(f"File not found: {filename}")
        continue

fileOutObj.close()
print("All files processed and saved to:", output_file_path)
