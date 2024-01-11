from openpyxl import load_workbook

class DiseaseData:
    name = ""
    type = ""
    category = ""
    info = ""
    cause = ""
    symptom = []
    symptomMatch = []
    treat = []
    prevent = []
    symptomAve = 0
    
    def __init__(self, name = "", type = "", category = "", info = "", cause = [], symptom = [], treat = [], prevent = []):
        self.name = name
        self.type = type
        self.category = category
        self.info = info
        self.cause = cause
        self.symptom = symptom
        self.symptomMatch = []
        if (symptom != None):
            for i in self.symptom:
                self.symptomMatch.append(0)
        self.symptomAve = 0
        self.treat = treat
        self.prevent = prevent
    
    def getSymptom(self):
        return self.symptom
    def getName(self):
        return self.name
    def getCause(self):
        return self.cause
    

def getDiseaseData():
    #파일 열기
    file = load_workbook("./질병 정보 정리.xlsx", data_only=True)
    sheet = file["diseaseList"]

    #disease라는 배열을 만들고 정보를 다 담음
    diseases = []
    first = True
    for column in sheet:
        if first:
            first = False
            continue
        name = column[0].value
        category = column[1].value
        type = column[2].value
        info = column[3].value


        cause = column[4].value
        if (cause != None):
            if (cause.find(", ") != -1):
                cause = cause.split(", ")
        symptom = column[5].value
        if (symptom != None):
            if (symptom.find(", ") != -1):
                symptom = symptom.split(", ")
        treat = column[6].value
        if (treat != None):
            if (treat.find(", ") != -1):
                treat = treat.split(", ")
        prevent = column[7].value
        if (prevent != None):
            if (prevent.find(", ") != -1):
                prevent = prevent.split(", ")
        diseases.append(DiseaseData(name, category, type, info, cause, symptom, treat, prevent))

    return diseases

    symptomList = []

    for data in diseases:
        contents = data.getSymptom()
        if (contents != None):
            for c in contents:
                if (c != None):
                    for i in symptomList:
                        if (c == i):
                            continue
                    symptomList.append(c)


    print(symptomList)
    print(len(symptomList))



