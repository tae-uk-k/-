import tkinter
import tkinter.font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from diseaseAranger import getDiseaseData
from diseaseAranger import DiseaseData
from diseaseMatch import getPercentage
from diseaseMatch import pickThree

window = tkinter.Tk()
window_width = 1280
window_height = 720
window.geometry(f'{window_width}x{window_height}')
window.resizable(False, False)

diseases = getDiseaseData()[0:3]

#각종 함수 선언
class A:
    diseases = getDiseaseData()[0:3]
    def result_window(self, diseases):
        res = symptom_entry.get()
        datas = getDiseaseData()
        diseases = getPercentage(datas, res)
        numList = pickThree(diseases)
        print(numList)
        diseases = [diseases[numList[0]], diseases[numList[1]], diseases[numList[2]]]
        self.diseases = diseases
        print(self.diseases[0].name)
        print(self.diseases[1].name)
        print(self.diseases[2].name)
        title_frame.pack_forget()
        make_result_frame()
        result_frame.pack()
a = A()

#타이틀 화면
title_frame = tkinter.Frame(window, width=1280, height=720)

title_label = tkinter.Label(title_frame, text="자가진단 AI", font=tkinter.font.Font(family="맑은 고딕", size=48, weight='bold'))
title_label.place(x=340, y=170)
symptom_entry = tkinter.Entry(title_frame, font=tkinter.font.Font(family="맑은 고딕", size=23, weight='bold'))
symptom_entry.place(x=340, y=320, width=600, height=80)
explain_label  = tkinter.Label(title_frame, text="현재 자신의 증상을 알려주세요", font=tkinter.font.Font(family="맑은 고딕", size=23, weight='bold'))
explain_label.place(x=340, y=265)
search_button = tkinter.Button(title_frame, text="진단 시작", command=lambda: a.result_window(diseases), font=tkinter.font.Font(family="맑은 고딕", size=23, weight='bold'))
search_button.place(x=570, y=413, width=140, height=60)

#결과 화면
result_frame = tkinter.Frame(window, width=1280, height=720)

def make_result_frame():
    disease_title = []
    percentage = []
    disease_label = []
    chart = []
    content = []
    symptoms = []
    details = []

    sizeList = [48, 40, 34]

    xPos = 67
    yPos = 157

    for i in range(3):
        disease_label.append(tkinter.Label(result_frame, text=a.diseases[i].name, font=tkinter.font.Font(family="맑은 고딕", size=int(90/len(a.diseases[i].name)), weight='bold')))
        disease_label[i].place(x = xPos, y = yPos)
        yPos += 210

    xPos = 225
    yPos = 94

    for i in range(3):
        symptomInfo = ""
        if (a.diseases[i].symptom != None):
            for symptom in a.diseases[i].symptom:
                symptomInfo += symptom + ' '
        treatInfo = ""
        if (a.diseases[i].treat != None):
            for treat in a.diseases[i].treat:
                treatInfo += treat + ' '
        preventInfo = ""
        if (a.diseases[i].prevent != None):
            for prevent in a.diseases[i].prevent:
                preventInfo += prevent + ' '
        
        details.append(tkinter.Text(result_frame, 
                                      width=651,
                                      height=187,
                                      wrap="word",
                                      font=tkinter.font.Font(family="맑은 고딕", size=20, weight='normal')))
        details[i].tag_configure("custom_tag1", selectforeground="#000000")
        details[i].insert(tkinter.END, a.diseases[i].info + '\n\n', "custom_tag1")
        details[i].insert(tkinter.END, "증상 : " + symptomInfo + '\n\n', "custom_tag1")
        details[i].insert(tkinter.END, "치료 : " + treatInfo + '\n\n', "custom_tag1")
        details[i].insert(tkinter.END, "예방 : " + preventInfo + '\n\n', "custom_tag1")
        


        details[i].config(state=tkinter.DISABLED)        
        details[i].place(x=xPos, y=yPos, width=651, height=187)
        yPos += 212

    xPos = 916
    yPos = 92

    select_label = tkinter.Label(result_frame, text="사용자에게 나타난 증상", font=tkinter.font.Font(family="맑은 고딕", size=23, weight='bold'))
    select_label.place(x=895, y=45)

    match_symptom = []
    match_symptomMatch = []
    for i in range(3):
        content.append(tkinter.Label(result_frame, background='#00B0F0'))
        content[i].place(x=xPos, y=yPos, width=304, height=187)

        chosenSymptom = ""
        unchosenSymptom = ""
        for j in range(len(a.diseases[i].symptom)):
            if (a.diseases[i].symptomMatch[j] != 0):
                match_symptom.append(a.diseases[i].symptom[j])
                match_symptomMatch.append(a.diseases[i].symptomMatch[j])
            else:
                unchosenSymptom += a.diseases[i].symptom[j] + ' '
                unchosenSymptom += str(int(a.diseases[i].symptomMatch[j])) + '%' + ' '

        symptom_figure = plt.figure()
        line = FigureCanvasTkAgg(symptom_figure, result_frame)
        plt.rcParams['font.family'] ='Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] =False
        plt.ylim(1, 100)
        plt.xticks([])
        symptom_figure.add_subplot(1, 1, 1).bar(match_symptom, match_symptomMatch)
        line.get_tk_widget().place(x=xPos, y=yPos, width=304, height=187)
        yPos += 212

    xPos = 56
    yPos = 250

    percentage.append(tkinter.Label(result_frame, text=(str(int(a.diseases[0].symptomAve)) + '%'), font=tkinter.font.Font(family="맑은 고딕", size=20, weight='bold')))
    percentage[0].place(x=100, y=240)
    percentage.append(tkinter.Label(result_frame, text=(str(int(a.diseases[1].symptomAve)) + '%'), font=tkinter.font.Font(family="맑은 고딕", size=20, weight='bold')))
    percentage[1].place(x=100, y=452)
    percentage.append(tkinter.Label(result_frame, text=(str(int(a.diseases[2].symptomAve)) + '%'), font=tkinter.font.Font(family="맑은 고딕", size=20, weight='bold')))
    percentage[2].place(x=100, y=664)


    def exit_window():
        window.destroy()
    exit_button = tkinter.Button(result_frame, text="X", font=tkinter.font.Font(family="맑은 고딕", size=20, weight='bold'), command=exit_window)
    exit_button.place(x=1222, y=4, width=40, height=40)

title_frame.pack()

window.mainloop()