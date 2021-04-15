from experta import *

diseases_list = list()
diseases_symptoms = list()
symptom_map = dict() # key: list of symptoms; value: Disease Name


def DataBase_Read():
    global diseases_list, diseases_symptoms, symptom_map
    diseases_t = open("diseases.txt")
    diseases_list = diseases_t.read().split("\n")
    diseases_t.close()
    for disease in diseases_list:
        disease_temp_file = open("Disease symptoms/" + disease + ".txt")
        disease_temp_data = disease_temp_file.read()
        s_list = disease_temp_data.split("\n")
        diseases_symptoms.append(s_list)
        symptom_map[str(s_list)] = disease
        disease_temp_file.close()


def get_details(disease):
    global diseases_list, diseases_symptoms, symptom_map
    _file_ = open("Disease descriptions/" + disease + ".txt")
    discription = _file_.read()
    _file_.close()
    return discription


def get_treatments(disease):
    global diseases_list, diseases_symptoms, symptom_map
    _file_ = open("Disease treatments/" + disease + ".txt")
    treatment = _file_.read()
    _file_.close()
    return treatment


def if_not_matched(disease, patient):
    id_disease = disease
    disease_details = get_details(id_disease)
    treatments = get_treatments(id_disease)
    print("\n\n"+ patient +", The most probable disease that you have is: \t\t %s" % id_disease)
    print("A short description of the disease is given below :\n")
    print(disease_details)
    print("The common medications and procedures suggested by other real doctors are:\n")
    print(treatments)


class Greetings(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        self.patients = input("Patient's Name: ").strip().upper()
        print("Hello! I am Diagnosis Expert System, Made by Dravyansh, Harsh, Janhvi, Mahen.\n" +
                "I am here to help you diagnose your disease.\n" + 
                "For that you'll have to answer a few questions about your conditions.\n" +
                "Do you feel any of the following symptoms:")
        yield Fact(action="find_disease")

    @Rule(Fact(action='find_disease'), NOT(Fact(headache=W())), salience=15)
    def symptom_0(self):
        self.declare(Fact(headache=input("headache: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(back_pain=W())), salience=14)
    def symptom_1(self):
        self.declare(Fact(back_pain=input("back pain: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(chest_pain=W())), salience=13)
    def symptom_2(self):
        self.declare(Fact(chest_pain=input("chest pain: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(cough=W())), salience=12)
    def symptom_3(self):
        self.declare(Fact(cough=input("cough: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(fainting=W())), salience=11)
    def symptom_4(self):
        self.declare(Fact(fainting=input("fainting: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(fatigue=W())), salience=9)
    def symptom_5(self):
        self.declare(Fact(fatigue=input("fatigue: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(sunken_eyes=W())), salience=4)
    def symptom_6(self):
        self.declare(Fact(sunken_eyes=input("sunken eyes: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(low_body_temp=W())), salience=7)
    def symptom_7(self):
        self.declare(Fact(low_body_temp=input("low body temperature: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(restlessness=W())), salience=8)
    def symptom_8(self):
        self.declare(Fact(restlessness=input("restlessness: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(sore_throat=W())), salience=10)
    def symptom_9(self):
        self.declare(Fact(sore_throat=input("sore throat: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(fever=W())), salience=6)
    def symptom_10(self):
        self.declare(Fact(fever=input("fever: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(nausea=W())), salience=3)
    def symptom_11(self):
        self.declare(Fact(nausea=input("Nausea: ").lower().strip()))

    @Rule(Fact(action='find_disease'), NOT(Fact(blurred_vision=W())), salience=-13)
    def symptom_12(self):
        self.declare(Fact(blurred_vision=input("blurred_vision: ").lower().strip()))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="yes"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="yes"), Fact(sunken_eyes="no"), Fact(nausea="yes"),
          Fact(blurred_vision="no"))
    def disease_0(self):
        self.declare(Fact(disease="Jaundice"))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="yes"),
          Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"),
          Fact(blurred_vision="no"))
    def disease_1(self):
        self.declare(Fact(disease="Alzheimers"))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="yes"), Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="yes"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"),
          Fact(blurred_vision="no"))
    def disease_2(self):
        self.declare(Fact(disease="Arthritis"))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="yes"),
          Fact(cough="yes"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="yes"), Fact(sunken_eyes="no"), Fact(nausea="no"),
          Fact(blurred_vision="no"))
    def disease_3(self):
        self.declare(Fact(disease="Tuberculosis"))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="yes"),
          Fact(cough="yes"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="yes"),
          Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"),
          Fact(blurred_vision="no"))
    def disease_4(self):
        self.declare(Fact(disease="Asthma"))

    @Rule(Fact(action='find_disease'), Fact(headache="yes"), Fact(back_pain="no"), Fact(chest_pain="no"),
          Fact(cough="yes"), Fact(fainting="no"), Fact(sore_throat="yes"), Fact(fatigue="no"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="yes"), Fact(sunken_eyes="no"), Fact(nausea="no"),
          Fact(blurred_vision="no"))
    def disease_5(self):
        self.declare(Fact(disease="Sinusitis"))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="yes"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"),
          Fact(blurred_vision="no"))
    def disease_6(self):
        self.declare(Fact(disease="Epilepsy"))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="yes"),
          Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="yes"),
          Fact(blurred_vision="no"))
    def disease_7(self):
        self.declare(Fact(disease="Heart Disease"))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="yes"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="yes"),
          Fact(blurred_vision="yes"))
    def disease_8(self):
        self.declare(Fact(disease="Diabetes"))

    @Rule(Fact(action='find_disease'), Fact(headache="yes"), Fact(back_pain="no"), Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="yes"),
          Fact(blurred_vision="yes"))
    def disease_9(self):
        self.declare(Fact(disease="Glaucoma"))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="yes"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="yes"),
          Fact(blurred_vision="no"))
    def disease_10(self):
        self.declare(Fact(disease="Hyperthyroidism"))

    @Rule(Fact(action='find_disease'), Fact(headache="yes"), Fact(back_pain="no"), Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="yes"), Fact(sunken_eyes="no"), Fact(nausea="yes"),
          Fact(blurred_vision="no"))
    def disease_11(self):
        self.declare(Fact(disease="Heat Stroke"))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fainting="yes"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"),
          Fact(low_body_temp="yes"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"),
          Fact(blurred_vision="no"))
    def disease_12(self):
        self.declare(Fact(disease="Hypothermia"))

    @Rule(Fact(action='find_disease'), Fact(headache="no"), Fact(back_pain="no"), Fact(chest_pain="no"),
          Fact(cough="no"), Fact(fainting="no"), Fact(sore_throat="no"), Fact(fatigue="no"), Fact(restlessness="no"),
          Fact(low_body_temp="no"), Fact(fever="no"), Fact(sunken_eyes="no"), Fact(nausea="no"),
          Fact(blurred_vision="no"))
    def disease_13(self):
        self.declare(Fact(disease="None"))

    @Rule(Fact(action='find_disease'), Fact(disease=MATCH.disease), salience=-998)
    def disease(self, disease):
        id_disease = disease
        disease_details = get_details(id_disease)
        treatments = get_treatments(id_disease)
        print("\n\n" + self.patients + ", The most probable disease that you have is %s" % id_disease)
        print("\nA short description of the disease is given below :\n")
        print(disease_details)
        print("\nThe common medications and procedures suggested by other real doctors are:\n")
        print(treatments)

    @Rule(Fact(action='find_disease'),
          Fact(headache=MATCH.headache),
          Fact(back_pain=MATCH.back_pain),
          Fact(chest_pain=MATCH.chest_pain),
          Fact(cough=MATCH.cough),
          Fact(fainting=MATCH.fainting),
          Fact(sore_throat=MATCH.sore_throat),
          Fact(fatigue=MATCH.fatigue),
          Fact(low_body_temp=MATCH.low_body_temp),
          Fact(restlessness=MATCH.restlessness),
          Fact(fever=MATCH.fever),
          Fact(sunken_eyes=MATCH.sunken_eyes),
          Fact(nausea=MATCH.nausea),
          Fact(blurred_vision=MATCH.blurred_vision),
          NOT(Fact(disease=MATCH.disease)), salience=-999)
    def not_matched(self, headache, back_pain, chest_pain, cough, fainting, sore_throat, fatigue, restlessness,
                    low_body_temp, fever, sunken_eyes, nausea, blurred_vision):
        print("\nDid not find any disease that matches your exact symptoms")
        lis = [headache, back_pain, chest_pain, cough, fainting, sore_throat, fatigue, restlessness, low_body_temp,
               fever, sunken_eyes, nausea, blurred_vision]
        max_count = 0
        max_disease = ""
        for key, val in symptom_map.items():
            count = 0
            temp_list = eval(key)
            for j in range(0, len(lis)):
                if temp_list[j] == lis[j] and lis[j] == "yes":
                    count = count + 1
            if count > max_count:
                max_count = count
                max_disease = val
        if_not_matched(max_disease, self.patients)

DataBase_Read()
engine = Greetings()
engine.reset()  # Preparing the engine for the execution.
engine.run()  # Runing

