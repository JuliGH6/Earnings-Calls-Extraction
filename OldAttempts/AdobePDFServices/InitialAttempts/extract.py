from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType


import os.path
import zipfile
import json

zip_file = "./ExtractTextInfoFromPDF.zip"

if os.path.isfile(zip_file):
    os.remove(zip_file)

input_pdf = "./test.pdf"


# config = json.load(open('pdfservices-api-credentials.json'))
# #Initial setup, create credentials instance.
# credentials = Credentials.service_principal_credentials_builder() \
#     .with_client_id(config['client_credentials']['client_id']) \
#     .with_client_secret(config['client_credentials']['client_secret']) \
#     .build()

# #Initial setup, create credentials instance.
# credentials = Credentials.service_principal_credentials_builder() \
#     .with_client_id("afcc815c44504352adfab0448911e01a") \
#     .with_client_secret("p8e-h29256rHP0sUq_gBUVPEpVYJSLIhBpmf") \
#     .build()

#Create an ExecutionContext using credentials and create a new operation instance.
execution_context = ExecutionContext.create(credentials)



extract_pdf_operation = ExtractPDFOperation.create_new()

#Set operation input from a source file.
source = FileRef.create_from_local_file(input_pdf)
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

print(data)

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

    if element['Bounds'][3] > 774 or element['Bounds'][1] < 53:
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

with open('outputFull.txt', 'a') as f:
    f.write(extractedText)