import os
import re
import math

path = '/Users/shalin_patel/Desktop/Artificial Intelligence/Project/Project2/SpamDetector/test'

modelValueHamDict = {}
modelValueSpamDict = {}

model = open('model.txt', 'r')
modelLines = model.readlines()

for line in modelLines:
    modelValueLine = line.split()
    modelValueHamDict[modelValueLine[1]] = modelValueLine[3]
    modelValueSpamDict[modelValueLine[1]] = modelValueLine[5]

files = []

hamTestFiles = []
spamTestFiles = []

dictHamTestFiles = {}
dictSpamTestFiles = {}

counter = 1
correctHamCount = 0
correctSpamCount = 0

result = open("result.txt", "w")

for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))
            if '-ham-' in file:
                hamTestFiles.append(file)
                content = open(path + "/" + file, 'r', encoding="ISO-8859-1").read()
                fileTokens = re.split('[^a-zA-Z]', content.lower())
                fileTokens = list(filter(lambda a: a != '', fileTokens))  # removing of blank spaces
                dictHamTestFiles[file] = fileTokens
            else:
                spamTestFiles.append(file)
                content = open(path + "/" + file, 'r', encoding="ISO-8859-1").read()
                fileTokens = re.split('[^a-zA-Z]', content.lower())
                fileTokens = list(filter(lambda a: a != '', fileTokens))  # removing of blank spaces
                dictSpamTestFiles[file] = fileTokens

for key, value in dictHamTestFiles.items():
    hamProbability = 0
    spamProbability = 0
    for v in value:
        if v in modelValueHamDict:
            hamProbability += math.log10(float(str(modelValueHamDict.get(v))))
        if v in modelValueSpamDict:
            spamProbability += math.log10(float(str(modelValueSpamDict.get(v))))
    result.write(str(counter) + "  " + str(key) + "  ")
    if hamProbability > spamProbability:
        correctHamCount += 1
        result.write(str("ham  ") + str(hamProbability) + "  " + str(spamProbability) + "  ham  right\n")
    else:
        result.write(str("spam  ") + str(hamProbability) + "  " + str(spamProbability) + "  ham  wrong\n")

for key, value in dictSpamTestFiles.items():
    hamProbability = 0
    spamProbability = 0
    for v in value:
        if v in modelValueHamDict:
            hamProbability += math.log10(float(str(modelValueHamDict.get(v))))
        if v in modelValueSpamDict:
            spamProbability += math.log10(float(str(modelValueSpamDict.get(v))))
    result.write(str(counter) + "  " + str(key) + "  ")
    if spamProbability > hamProbability:
        correctSpamCount += 1
        result.write(str("spam  ") + str(hamProbability) + "  " + str(spamProbability) + "  spam  right\n")
    else:
        result.write(str("ham  ") + str(hamProbability) + "  " + str(spamProbability) + "  spam  wrong\n")

result.close()
print("Result File Created")
