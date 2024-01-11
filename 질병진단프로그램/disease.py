class Disease:
    diseaseCategory = ""
    diseaseTag = ""
    diseaseName = ""
    index = ""
    diseaseInfo = ""
    risk = ""
    symptom = ""
    treat = ""
    prevent = ""
    
    def __init__(self, diseaseCategory, diseaseTag, diseaseName, index = -1):
        self.diseaseCategory = diseaseCategory
        self.diseaseTag = diseaseTag
        self.diseaseName = diseaseName
        self.index = index
    
    def show(self):
        print(self.diseaseCategory, '-', self.diseaseTag, '-', self.diseaseName, '-', self.index, '!', sep = "")
    
    def showAll(self):
        print(self.index, " : ", self.diseaseName, '-', self.diseaseTag, '-', self.diseaseCategory, "\n", sep = "")
        print(self.diseaseInfo)
        print(self.risk)
        print(self.symptom)
        print(self.treat)
        print(self.prevent)

    def addExplain(self, diseaseInfo, risk, symptom, treat, prevent):
        self.diseaseInfo = diseaseInfo
        self.risk = risk
        self.symptom = symptom
        self.treat = treat
        self.prevent = prevent