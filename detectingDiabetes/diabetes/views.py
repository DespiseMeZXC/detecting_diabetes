# ************************* pip install scikit-learn
from django.shortcuts import render
import pickle
import numpy as np

res = ""
some = ""
infoPat = [" ", " ", " ", " ", " ", " "]
infoAnalyzes = [" ", " ", " ", " ", " ", " ", " ", " "]


menu = [{"name": "Внесение информации о пациенте", "url": "ness"},
        {"name": "Внесение анализов пациента", "url": "detection_diabet"},
        {"name": "Отчёт о пациенте", "url": "p_lab3"}]

loaded_model = pickle.load(open('diabetes/model/Model_cnn', 'rb'))


def necessary_info(request):
    if request.method == 'GET':
        return render(request, 'necessaryInfo.html',
                      {'title': 'Внесение информации о клиенте', 'menu': menu, 'res': ''})
    if request.method == 'POST':
            global  res
            res = "Успешно"
            res_post = []
            for i in request.POST:
                res_post.append(i)
            res_post.pop(0)
            global infoPat
            infoPat = []
            for i in res_post:
                infoPat.append(request.POST[i])
            return render(request, 'detectingDiabet.html', {'title': 'Внесение анализов пациента', 'menu': menu})

def detection_diabet(request):
    if request.method == 'GET':
        global res
        if res != "":
            return render(request, 'detectingDiabet.html', {'title': 'Внесение анализов пациента', 'menu': menu,
                                                        'class_model': ''})
        else:
            return render(request, 'necessaryInfo.html',
                      {'title': 'Внесение информации о клиенте', 'menu': menu, 'res': ''})
    if request.method == 'POST':
        X_new = np.array([[float(request.POST['Pregnancies']),
                           float(request.POST['Glucose']),
                           float(request.POST['BloodPressure']),
                           float(request.POST['SkinThickness']),
                           float(request.POST['Insulin']),
                           float(request.POST['BMI']),
                           float(request.POST['DiabetesPedigreeFunction']),
                           float(request.POST['Age'])]])
        pred = loaded_model.predict(X_new)
        result = pred[0]
        global some
        if result == 1:
            some = "Вероятен диабет"
        else:
            some = "Диабет маловероятен"
        res_post = []
        for i in request.POST:
            res_post.append(i)
        res_post.pop(0)
        global infoAnalyzes
        infoAnalyzes = []
        for i in res_post:
            infoAnalyzes.append(request.POST[i])
        if some!="":
            res = "Успешно"
        else:
            res = "Что то не так"
        if some == "Вероятен диабет" and res == "Успешно":
            some_res = "Подробный анализ даёт понять, что в ближайшие 5 лет у вас может начаться диабет."
            title_recomendation = "Дополнительные рекомендации по профилактики диабета"
            recomendation = """Добавьте активность в вашу повседневную жизнь, проводя меньше времени у телевизора/компьютера. Работайте в саду, сами мойте машину, поднимайтесь по лестнице, ходите пешком в магазин – любое активное времяпрепровождение принесёт пользу
        Самоконтроль. Узнайте о своем недуге больше, купите глюкометр, соблюдайте диету, следите за массой тела.
        Минимизируйте излишние эмоции и стрессы, избегайте инфекций.
        Не курите.
        Исключите алкоголь.
        Занимайтесь спортом."""
        elif some == "Диабет маловероятен" and res == "Успешно":
            some_res = "Подробный анализ даёт понять, что в ближайшие 5 лет у вас врядли начнётся диабет"
            title_recomendation = "Дополнительные рекомендации по профилактике предотвращения развития диабета"
            recomendation = """1. Вести активный образ жизн и контролировать свой вес. Это могут быть пешие прогулки, гимнастические упражнения, плавание, катание на велосипеде, коньках. Любые активные занятия, которые к тому же приносят удовольствие. Диабет напрямую связан с ожирением. Любая физическая активность способствует снижению содержания сахара в крови и уменьшает необходимость инсулина.
        2. Питайтесь правильно. Употребляйте продукты с большим содержанием пищевых волокон, которые нормализуют работу кишечника и понижают уровень холестерина. К таким продуктам относятся все фрукты и овощи, бобовые, молочные продукты, орехи и другие. Снизьте употребление мучных изделий, сладостей, макарон. Употребляйте только цельнозерновой хлеб.
        3. Высыпайтесь. Отдохнувший организм не будет требовать большого количества глюкозы, поэтому для профилактики диабета крайне важно хорошо высыпаться.
        4. Не курите и избегайте стрессов. Стрессы, курение снижают сопротивляемость организма к сахарному диабету и являются одной из причин проявления сахарного диабета.
        5. Контролируйте уровень глюкозы в крови, если вы старше 40 лет. Старайтесь по чаще сдавать анализ на сахар особенно необходимо тем, кто имеет склонность к полноте и ведет малоподвижный образ жизни."""
        else:
            some_res = 'Для получения успешно внесите информацию и анализы пациента'
            title_recomendation = ""
            recomendation = ""
        return render(request, 'PatientReport.html', {'title': 'Отчёт о пациенте', 'menu': menu,
                                                      'namePat': infoPat[0], 'birthDay': infoPat[1],
                                                      'OutpatientCard': infoPat[2], 'adress': infoPat[3],
                                                      'dateResearch': infoPat[4], 'nameDoctor': infoPat[5],
                                                      'Pregnancies': infoAnalyzes[0], 'Glucose': infoAnalyzes[1],
                                                      'BloodPressure': infoAnalyzes[2],
                                                      'SkinThickness': infoAnalyzes[3],
                                                      'Insulin': infoAnalyzes[4], 'BMI': infoAnalyzes[5],
                                                      'DiabetesPedigreeFunction': infoAnalyzes[6],
                                                      'Age': infoAnalyzes[7], 'result': some_res,
                                                      'recomendation': recomendation,
                                                      'title_recomendation': title_recomendation})


def f_lab3(request):
    if some == "Вероятен диабет" and res == "Успешно":
        some_res = "Подробный анализ даёт понять что в ближайшие 5 лет у вас может начаться диабет."
        title_recomendation = "Дополнительные рекомендации по профилактики диабета"
        recomendation = """Добавьте активность в вашу повседневную жизнь, проводя меньше времени у телевизора/компьютера. Работайте в саду, сами мойте машину, поднимайтесь по лестнице, ходите пешком в магазин – любое активное времяпрепровождение принесёт пользу
    Самоконтроль. Узнайте о своем недуге больше, купите глюкометр, соблюдайте диету, следите за массой тела.
    Минимизируйте излишние эмоции и стрессы, избегайте инфекций.
    Не курите.
    Исключите алкоголь.
    Занимайтесь спортом."""

        return render(request, 'PatientReport.html', {'title': 'Отчёт о пациенте', 'menu': menu,
                                                  'namePat': infoPat[0], 'birthDay': infoPat[1],
                                                  'OutpatientCard': infoPat[2], 'adress': infoPat[3],
                                                  'dateResearch': infoPat[4], 'nameDoctor': infoPat[5],
                                                  'Pregnancies': infoAnalyzes[0], 'Glucose': infoAnalyzes[1],
                                                  'BloodPressure': infoAnalyzes[2], 'SkinThickness': infoAnalyzes[3],
                                                  'Insulin': infoAnalyzes[4], 'BMI': infoAnalyzes[5],
                                                  'DiabetesPedigreeFunction': infoAnalyzes[6],
                                                  'Age': infoAnalyzes[7], 'result': some_res,
                                                  'recomendation': recomendation,
                                                  'title_recomendation': title_recomendation})
    elif some == "Диабет маловероятен" and res == "Успешно":
        some_res = "Подробный анализ даёт понять что в ближайшие 5 лет у вас врядли начнётся диабет"
        title_recomendation = "Дополнительные рекомендации по профилактике предотвращения развития диабета"
        recomendation = """1. Вести активный образ жизн и контролировать свой вес. Это могут быть пешие прогулки, гимнастические упражнения, плавание, катание на велосипеде, коньках. Любые активные занятия, которые к тому же приносят удовольствие. Диабет напрямую связан с ожирением. Любая физическая активность способствует снижению содержания сахара в крови и уменьшает необходимость инсулина.
    2. Питайтесь правильно. Употребляйте продукты с большим содержанием пищевых волокон, которые нормализуют работу кишечника и понижают уровень холестерина. К таким продуктам относятся все фрукты и овощи, бобовые, молочные продукты, орехи и другие. Снизьте употребление мучных изделий, сладостей, макарон. Употребляйте только цельнозерновой хлеб.
    3. Высыпайтесь. Отдохнувший организм не будет требовать большого количества глюкозы, поэтому для профилактики диабета крайне важно хорошо высыпаться.
    4. Не курите и избегайте стрессов. Стрессы, курение снижают сопротивляемость организма к сахарному диабету и являются одной из причин проявления сахарного диабета.
    5. Контролируйте уровень глюкозы в крови, если вы старше 40 лет. Старайтесь по чаще сдавать анализ на сахар особенно необходимо тем, кто имеет склонность к полноте и ведет малоподвижный образ жизни."""
        return render(request, 'PatientReport.html', {'title': 'Отчёт о пациенте', 'menu': menu,
                                                  'namePat': infoPat[0], 'birthDay': infoPat[1],
                                                  'OutpatientCard': infoPat[2], 'adress': infoPat[3],
                                                  'dateResearch': infoPat[4], 'nameDoctor': infoPat[5],
                                                  'Pregnancies': infoAnalyzes[0], 'Glucose': infoAnalyzes[1],
                                                  'BloodPressure': infoAnalyzes[2], 'SkinThickness': infoAnalyzes[3],
                                                  'Insulin': infoAnalyzes[4], 'BMI': infoAnalyzes[5],
                                                  'DiabetesPedigreeFunction': infoAnalyzes[6],
                                                  'Age': infoAnalyzes[7], 'result': some_res,
                                                  'recomendation': recomendation,
                                                  'title_recomendation': title_recomendation})
    else:
         return render(request, 'necessaryInfo.html',
                      {'title': 'Внесение информации о клиенте', 'menu': menu, 'res': ''})
        # some_res = 'Для получения успешно внесите информацию и анализы пациента'
        # title_recomendation = ""
        # recomendation = ""
        # return render(request, 'PatientReport.html', {'title': 'Отчёт о пациенте', 'menu': menu,
        #                                           'namePat': infoPat[0], 'birthDay': infoPat[1],
        #                                           'OutpatientCard': infoPat[2], 'adress': infoPat[3],
        #                                           'dateResearch': infoPat[4], 'nameDoctor': infoPat[5],
        #                                           'Pregnancies': infoAnalyzes[0], 'Glucose': infoAnalyzes[1],
        #                                           'BloodPressure': infoAnalyzes[2], 'SkinThickness': infoAnalyzes[3],
        #                                           'Insulin': infoAnalyzes[4], 'BMI': infoAnalyzes[5],
        #                                           'DiabetesPedigreeFunction': infoAnalyzes[6],
        #                                           'Age': infoAnalyzes[7], 'result': some_res,
        #                                           'recomendation': recomendation,
        #                                           'title_recomendation': title_recomendation})

    