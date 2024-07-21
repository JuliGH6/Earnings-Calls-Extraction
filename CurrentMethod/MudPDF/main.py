import os
import pymupdf

# FUNCTIONS---------------------

# removes all duplicate files in a folder
def removeDuplicateFiles(inFolderPath):
    print('\n\nFilesRemoved:')
    fileNames = os.listdir(inFolderPath)
    prefixDict = {}
    filesToRemove = []
    
    for fileName in fileNames:
        if fileName[:-25] in prefixDict: filesToRemove.append(fileName)
        else: prefixDict[fileName[:-25]] = fileName
    
    for fileName in filesToRemove:
        os.remove(os.path.join(inFolderPath, fileName))
        print(f"File '{fileName}' deleted")

# gets starting page and returns page number where phrase was found or -1 if nothing was found
def getStartingPage(inFilePath, startingPhrase1, startingPhrase2):
    doc = pymupdf.open(inFilePath) # open a document
    for i in range(len(doc)): # iterate the document pages
        page = doc[i]
        text = page.get_text()
        if (startingPhrase1 in text) or (startingPhrase2 in text): return i
    return -1

# reads pdf and writes text file from starting page
def convertFile(inFilePath, outFilePath, startingPage):
    outputList = []
    doc = pymupdf.open(inFilePath) # open a document
    for page in doc[startingPage:]: # iterate the document pages
        text = page.get_text('blocks', sort = True)
        text = text[:-1]
        for i in text:
            if i[1] < 50.0: continue
            block = i[4].replace('\n',' ')
            if block[0].isupper(): outputList.append(block)
            else: outputList[-1] = outputList[-1] + block
    outputList = outputList[:-1] + ['End of transcript.']

    out = open(outFilePath, 'w')
    out.write('\n'.join(outputList))
    out.close()


# SETUP-------------------------

# Starting phrase
startingPhrase1 = "FINAL TRANSCRIPT"
startingPhrase2 = 'INITIAL DRAFT TRANSCRIPT'

# Folder paths
inFolderPath = folder_path = os.getcwd() + '/Pdfs'
outFolderPath = os.getcwd() + '/Results'
if not os.path.exists(outFolderPath):
    os.makedirs(outFolderPath)

removeDuplicateFiles(inFolderPath)

# List Filenames
inFileNames = [file for file in os.listdir(inFolderPath) if not file.startswith('.')]
outFileNames = [file for file in os.listdir(outFolderPath) if not file.startswith('.')]


print('\n\n No starting Phrase:')


# FOLDER ITERATION--------------

for inFileName in inFileNames:
    inFilePath = os.path.join(inFolderPath, inFileName)
    outFileName = inFileName[:-4] + '_RESULT.txt'
    outFilePath = os.path.join(outFolderPath, outFileName)

    startingPage = getStartingPage(inFilePath, startingPhrase1, startingPhrase2)
    if startingPage == -1:
        print(f'No StartingPhrases Found: {inFilePath}')
        continue

    convertFile(inFilePath, outFilePath, startingPage)





