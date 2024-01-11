from matchChecker import TextSimilarityChecker
from diseaseAranger import getDiseaseData
from diseaseAranger import DiseaseData
import time

def getPercentage(diseases, word):
    access_key = "c5dd01ba-7adb-4ae6-ae1e-3f494a9c29c6" 

    textSimilarityChecker = TextSimilarityChecker()

    for disease in diseases:
        if (disease.symptom == None):
            disease.symptomAve = 0
        else:
            sum = 0
            for i in range(len(disease.symptom)):
                time.sleep(0.1)
                res = textSimilarityChecker.check_paraphrase(word, disease.symptom[i])
                if (res):
                    similarity_sentence_transformers = textSimilarityChecker.calculate_similarity(word, disease.symptom[i])
                    similarity_tfidf = textSimilarityChecker.calculate_similarity_tfidf(word, disease.symptom[i])
                    koelectra_embedding1 = textSimilarityChecker.get_koelectra_embedding(word)
                    koelectra_embedding2 = textSimilarityChecker.get_koelectra_embedding(disease.symptom[i])
                    similarity_koelectra = textSimilarityChecker.calculate_cosine_similarity(koelectra_embedding1, koelectra_embedding2)*100
                    disease.symptomMatch[i] = (similarity_sentence_transformers + similarity_tfidf + similarity_koelectra) / 3
                    sum += disease.symptomMatch[i]
                else:
                    disease.symptomMatch[i] = 0
            print(sum, len(disease.symptom))
            disease.symptomAve = sum / len(disease.symptom)
    
    return diseases

def pickThree(diseases):
    diseases.append(DiseaseData("", "", "", "", [], [], [], []))
    numList = [len(diseases) - 1, len(diseases) - 1, len(diseases) - 1]
    for i in range(len(diseases) - 1):
        if (diseases[i].symptomAve > diseases[numList[0]].symptomAve):
            numList[0] = i
        elif (diseases[i].symptomAve > diseases[numList[1]].symptomAve):
            numList[1] = i
        elif (diseases[i].symptomAve > diseases[numList[2]].symptomAve):
            numList[2] = i
    return numList

'''
diseases = getDiseaseData()
diseases = diseases[:10]

print(diseases[0].name, diseases[0].symptomAve)
word = input("단어 입력하세요 : ")
diseases = getPercentage(diseases, word)

print(diseases[0].name, diseases[0].symptomAve)

numList = pickThree(diseases)
print(numList)

for i in range(3):
    print(diseases[numList[i]].name, diseases[numList[i]].symptom, diseases[numList[i]].symptomMatch, diseases[numList[i]].symptomAve)

print("\n\n\n\n\n-----------------------------\n\n\n\n\n")

for disease in diseases:
    print(disease.name, disease.symptom, disease.symptomMatch, disease.symptomAve)


'''