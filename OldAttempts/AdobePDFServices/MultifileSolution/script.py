from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType

from PyPDF2 import PdfReader, PdfWriter

import os.path
import zipfile
import json

def alterPageRange(input_pdf_path, phrase):
    with open(input_pdf_path, 'rb') as infile:
        reader = PdfReader(infile)

        startingPage = -1
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()

            if phrase in text:
                startingPage = page_num
                break
        
        if startingPage == -1:
            return
        
        writer = PdfWriter()
        for page_num in range(startingPage, len(reader.pages)):
            page = reader.pages[page_num]
            writer.addPage(page)
        
        # Write the modified PDF content to a temporary file
        temp_output_pdf = input_pdf_path + ".tmp"
        with open(temp_output_pdf, 'wb') as output_file:
            writer.write(output_file)

    os.replace(temp_output_pdf, input_pdf_path)
    return




# config = json.load(open('pdfservices-api-credentials.json'))
# #Initial setup, create credentials instance.
# credentials = Credentials.service_principal_credentials_builder() \
#     .with_client_id(config['client_credentials']['client_id']) \
#     .with_client_secret(config['client_credentials']['client_secret']) \
#     .build()

zip_file = "./ExtractTextInfoFromPDF.zip"

folder_path = os.getcwd() + '/Pdfs'
outFolderPath = os.getcwd() + '/Results'
if not os.path.exists(outFolderPath):
    os.makedirs(outFolderPath)

phrase = "FINAL TRANSCRIPT"

filenames = [file for file in os.listdir(folder_path) if not file.startswith('.')]
resultFiles = [file for file in os.listdir(outFolderPath) if not file.startswith('.')]

i = 0

# Iterate through all files in the folder
for file_name in filenames:
    i += 1
    # Construct the full path to the file
    file_path = os.path.join(folder_path, file_name)
    # Check if it's a regular file
    if not os.path.isfile(file_path): continue

    if os.path.isfile(zip_file):
        os.remove(zip_file)
    
    outFileName = file_name[:-4] + '_RESULT.txt'
    if outFileName in resultFiles: 
        print (i, 'exists already:', outFileName)
        continue

    #Create an ExecutionContext using credentials and create a new operation instance.
    execution_context = ExecutionContext.create(credentials)

    extract_pdf_operation = ExtractPDFOperation.create_new()

    alterPageRange(file_path, phrase)
    #Set operation input from a source file.
    source = FileRef.create_from_local_file(file_path)
    extract_pdf_operation.set_input(source)

    #Build ExtractPDF options and set them into the operation
    extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
        .with_element_to_extract(ExtractElementType.TEXT) \
        .build()
    extract_pdf_operation.set_options(extract_pdf_options)

    #Execute the operation.
    result: FileRef = extract_pdf_operation.execute(execution_context)

    #Save the result to the specified location.
    result.save_as(zip_file)

    archive = zipfile.ZipFile(zip_file, 'r')
    jsonentry = archive.open('structuredData.json')
    jsondata = jsonentry.read()
    data = json.loads(jsondata)

    extractedText =""

    previousLowerBound = -1
    previousEndsDot = False
    previousFontHeader = False

    for element in data["elements"]:

        newPage = (previousLowerBound < element['Bounds'][3])

        if not "Text" in element:
            previousLowerBound = element['Bounds'][1]
            previousEndsDot = True
            previousFontHeader = True
            continue

        if element['Bounds'][3] > 774 or element['Bounds'][1] < 38:
            continue

        if newPage and not previousEndsDot and not previousFontHeader: extractedText += element['Text']
        else: extractedText += '\n' + element['Text']

        previousLowerBound = element['Bounds'][1]
        previousEndsDot = (element['Text'][-1] == '.' or element['Text'][-2] == '.')
        previousFontHeader = ('B' == element['Font']['name'][0])


    lines = extractedText.split('\n')
        
        # Remove the last line
    lines = lines[:-1]

        # Join the remaining lines back into a single string
    extractedText = '\n'.join(lines)

    # outFileName = file_name[:-4] + '_RESULT.txt'
    outFilePath = os.path.join(outFolderPath, outFileName)

    with open(outFilePath, 'w') as f:
        f.write(extractedText)

    print(i, file_name, 'is processed')
