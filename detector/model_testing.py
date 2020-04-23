import os
import re
import math

'''
Reading the model file and storing the ham and spam values
'''
modelValueHamDict = {}
modelValueSpamDict = {}

model = open('model.txt', 'r')
modelLines = model.readlines()

for line in modelLines:
    modelValueLine = line.split()
    modelValueHamDict[modelValueLine[1]] = modelValueLine[3]
    modelValueSpamDict[modelValueLine[1]] = modelValueLine[5]

path = '/Users/shalin_patel/Desktop/Artificial Intelligence/Project/Project2/SpamDetector/test'

files = []

hamTestFiles = []
spamTestFiles = []

dictHamTestFiles = {}
dictSpamTestFiles = {}

counter = 1
correctHamCount = 0
correctSpamCount = 0

result = open("result.txt", "w")

hamCorrect = 0
hamNotCorrect = 0

spamCorrect = 0
spamNotCorrect = 0

'''
Reading all the test files and string the tokens in dict
'''
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

'''
Evaluating each file ans saving the result for ham files
'''
for key, value in sorted(dictHamTestFiles.items()):
    hamProbability = 0
    spamProbability = 0
    for v in value:
        if v in modelValueHamDict:
            hamProbability += math.log10(float(str(modelValueHamDict.get(v))))
        if v in modelValueSpamDict:
            spamProbability += math.log10(float(str(modelValueSpamDict.get(v))))
    result.write(str(counter) + "  " + str(key) + "  ")
    counter += 1
    if hamProbability > spamProbability:
        correctHamCount += 1
        hamCorrect += 1
        result.write(str("ham  ") + str(hamProbability) + "  " + str(spamProbability) + "  ham  right\n")
    else:
        hamNotCorrect += 1
        result.write(str("spam  ") + str(hamProbability) + "  " + str(spamProbability) + "  ham  wrong\n")

'''
Evaluating each file ans saving the result for spam files
'''
for key, value in sorted(dictSpamTestFiles.items()):
    hamProbability = 0
    spamProbability = 0
    for v in value:
        if v in modelValueHamDict:
            hamProbability += math.log10(float(str(modelValueHamDict.get(v))))
        if v in modelValueSpamDict:
            spamProbability += math.log10(float(str(modelValueSpamDict.get(v))))
    result.write(str(counter) + "  " + str(key) + "  ")
    counter += 1
    if spamProbability > hamProbability:
        correctSpamCount += 1
        spamCorrect += 1
        result.write(str("spam  ") + str(hamProbability) + "  " + str(spamProbability) + "  spam  right\n")
    else:
        spamNotCorrect += 1
        result.write(str("ham  ") + str(hamProbability) + "  " + str(spamProbability) + "  spam  wrong\n")

result.close()
print("\nResult File Created\n")

'''
Confusion Matrix
'''
print("CONFUSION MATRIX\n")
print("          " + "HAM   " + "   SPAM   ")
print("HAM   |   " + str(hamCorrect) + "   |   " + str(hamNotCorrect))
print("SPAM  |   " + str(spamNotCorrect) + "   |   " + str(spamCorrect))

print("\nACCURACY  - " + str((hamCorrect+spamCorrect)/(hamCorrect+hamNotCorrect+spamNotCorrect+spamCorrect)))

hamRecall = hamCorrect / (hamCorrect + hamNotCorrect)
spamRecall = spamCorrect / (spamCorrect + spamNotCorrect)
print("\nHAM RECALL  - " + str(hamRecall))
print("SPAM RECALL - " + str(spamRecall))

hamPrecision = hamCorrect / (hamCorrect + spamNotCorrect)
spamPrecision = spamCorrect / (spamCorrect + hamNotCorrect)
print("\nHAM PRECISION  - " + str(hamPrecision))
print("SPAM PRECISION - " + str(spamPrecision))

hamFMeasure = (2*hamRecall*hamPrecision) / (hamRecall + hamPrecision)
spamFMeasure = (2*spamRecall*spamPrecision) / (spamRecall + spamPrecision)
print("\nHAM F-Measure  - " + str(hamFMeasure))
print("SPAM F-Measure - " + str(spamFMeasure))
