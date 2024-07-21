import os
import pandas as pd


# Change Names------------------
sector = 'Communications'
inFolderPath = folder_path = os.getcwd() + '/Results'

fileNames = [file for file in os.listdir(inFolderPath) if not file.startswith('.')]

data = {
    'fileName': [],
    'newFileName': [],
    'sector': [],
    'company': [],
    'date': [],
    'quarter': [],
}

for fileName in fileNames:
    date = fileName[:8]

    quarter = ''

    with open(os.path.join(inFolderPath,fileName), 'r') as file:
        quarter = file.read(2)

    endNameIndex = -1
    for i in range(len(fileName)):
        if fileName[i] == '-': 
            endNameIndex = i
            break
        
    company = fileName[9:endNameIndex]

    newFileName = f"{sector}-{company}-{quarter}-{date}.txt"

    data['fileName'].append(fileName)
    data['newFileName'].append(newFileName)
    data['sector'].append(sector)
    data['company'].append(company)
    data['quarter'].append(quarter)
    data['date'].append(date)

df = pd.DataFrame(data)

# Write the DataFrame to an Excel file
outputFilePath = os.path.join(os.getcwd(), 'CommunicationsNames.xlsx')
df.to_excel(outputFilePath, index=False)
