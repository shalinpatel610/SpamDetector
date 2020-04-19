import os
import re
from collections import Counter

path = '/Users/shalin_patel/Desktop/Artificial Intelligence/Project/Project2/SpamDetector/train'

files = []

hamTrainFiles = []
spamTrainFiles = []

dictHamTrainFiles = {}
dictSpamTrainFiles = {}

totalHamCount = 0
totalSpamCount = 0

frequencyListHam = []
frequencyListSpam = []

frequencyDictHam = {}
frequencyDictSpam = {}

conditionalProbabilityHam = {}
conditionalProbabilitySpam = {}

priorProbabilityHam = 0
priorProbabilitySpam = 0

wordList = []

for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))
            if '-ham-' in file:
                hamTrainFiles.append(file)
                content = open(path + "/" + file, 'r', encoding="ISO-8859-1").read()
                fileTokens = re.split('[^a-zA-Z]', content.lower())
                fileTokens = list(filter(lambda a: a != '', fileTokens))  # removing of blank spaces
                dictHamTrainFiles[file] = fileTokens
            else:
                spamTrainFiles.append(file)
                content = open(path + "/" + file, 'r', encoding="ISO-8859-1").read()
                fileTokens = re.split('[^a-zA-Z]', content.lower())
                fileTokens = list(filter(lambda a: a != '', fileTokens))  # removing of blank spaces
                dictSpamTrainFiles[file] = fileTokens

'''
Merge all the words.
Count the occurrence of each word.
'''
for key, value in dictHamTrainFiles.items():
    totalHamCount += len(value)
    frequencyListHam.extend(value)
    # nestedDictHamWordCount[key] = dict((x, value.count(x)) for x in set(value))  # Count the occurrence of each word in list

for key, value in dictSpamTrainFiles.items():
    totalSpamCount += len(value)
    frequencyListSpam.extend(value)
    # nestedDictSpamWordCount[key] = dict((x, value.count(x)) for x in set(value))  # Count the occurrence of each word in list

frequencyDictHam = Counter(frequencyListHam)
frequencyDictSpam = Counter(frequencyListSpam)

'''
word list will have all the words from ham and spam files.
'''
wordList.extend(frequencyListHam)
wordList.extend(frequencyListSpam)
wordList = set(wordList)

'''
Add 0.5 for smoothing for all the words which are missing in frequency dict
'''
for word in wordList:
    if word in frequencyDictHam:
        frequencyDictHam[word] = frequencyDictHam.get(word) + 0.5
    else:
        frequencyDictHam[word] = 0.5

    if word in frequencyDictSpam:
        frequencyDictSpam[word] = frequencyDictSpam.get(word) + 0.5
    else:
        frequencyDictSpam[word] = 0.5

'''
Calculate the conditional probability
'''
for key, value in frequencyDictHam.items():
    value = value/(totalHamCount + len(wordList))
    conditionalProbabilityHam[key] = value

for key, value in frequencyDictSpam.items():
    value = value/(totalSpamCount + len(wordList))
    conditionalProbabilitySpam[key] = value

'''
Calculate the prior probability
'''
priorProbabilityHam = len(hamTrainFiles)/(len(hamTrainFiles)+len(spamTrainFiles))
priorProbabilitySpam = len(spamTrainFiles)/(len(hamTrainFiles)+len(spamTrainFiles))


'''
Create a model text file
'''
model = open("model.txt", "w")
for i, word in enumerate(sorted(wordList)):
    model.write(str(i) + "  " + str(word) + "  " + str(frequencyDictHam.get(word)) + "  " + str(conditionalProbabilityHam.get(word)) + "  " +
                str(frequencyDictSpam.get(word)) + "  " + str(conditionalProbabilitySpam.get(word)) + "\n")
model.close()

print("Model File Created")
