from experta import *
import os
from common import Severity

class Symptom(Fact):
    name = Field(str, mandatory=True)
    disease = Field(list)

class Disease(Fact):
    name = Field(str, mandatory=True)
    symptom = Field(list)
    severity = Field(list)

class Task(Fact):
    pass

class Query(Fact):
    symptom = Field(str, mandatory=True)
    severity = Field(Severity, mandatory=True)

def DataBase_Read():
    with open("diseases.txt") as diseases_t:
        diseases_list = [a.strip()  for a in diseases_t.read().split("\n") if a != '']
    disease_symptom_dict = {}
    print(diseases_list)
    for disease in diseases_list:
        with open(os.path.join(os.getcwd(), "Disease symptoms", "{}.txt".format(disease))) as disease_temp_file:
            disease_temp_data = disease_temp_file.read()
            disease_symptom_dict[disease] = {}
            temp_symp = []
            temp_sev = []
            for idx, data in enumerate(disease_temp_data.split("\n")):
                if idx % 2 == 0:
                    temp_symp.append(data)
                else:
                    temp_sev.append(tuple([Severity(int(x.strip())) for x in data.split(",")]))
            disease_symptom_dict[disease]['symp'] = temp_symp
            disease_symptom_dict[disease]['sev'] = temp_sev
    symptom_disease_dict = {}
    symptom_list = []
    for disease in diseases_list:
        for symptom in disease_symptom_dict[disease]['symp']:
            if symptom not in symptom_disease_dict:
                symptom_disease_dict[symptom] = []
            symptom_disease_dict[symptom].append(disease)
            if symptom not in symptom_list:
                symptom_list.append(symptom)
    return (disease_symptom_dict, symptom_disease_dict, diseases_list, symptom_list)


def get_details(disease):
    with open(os.path.join(os.getcwd(), "Disease descriptions", "{}.txt".format(disease))) as fd:
        discription = fd.read()
    return discription


def get_treatments(disease):
    with open(os.path.join(os.getcwd(), "Disease treatments", "{}.txt".format(disease))) as fd:
        treatment = fd.read()
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


class Diagnose(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self, dis_symp_dict, symp_dis_dict, symp_list):
        for symptom in symp_dis_dict:
            yield Symptom(name=symptom, disease=symp_dis_dict[symptom])
        for disease in dis_symp_dict:
            yield Disease(name=disease, symptom=dis_symp_dict[disease]['symp'], severity=dis_symp_dict[disease]['sev'])
        self.symp_list = symp_list

    @Rule(salience=1000)
    def startup(self):
        self.patients = input("Patient's Name: ").strip().upper()
        print("Hello! I am a Custom Diagnosis Expert System, Made by Dravyansh, Harsh, Janhvi, Mahen.\n"
                "I am here to help you diagnose your disease.\n"
                "Please start typing in your symptoms and its severity. ")
        self.declare(Task('type-symptom'))

    @Rule(AS.f1 << Task('type-symptom'))
    def type_symptom(self, f1):
        ans = ' '
        sev = ' '
        while ans != '' and sev != '':
            ans = input('Symptom>').strip()
            autofill = list(filter(lambda x: x.startswith(ans), self.symp_list))
            if len(autofill) == 1 or ans.replace(" ", "_").strip() in self.symp_list:
                ans = autofill[0]
                sev = input('Severity (0-5)>')
                try:
                    sev = Severity(int(sev))
                except ValueError:
                    print("Please enter a number")
                    sev = ' '
                    continue
                self.declare(Query(symptom=ans, severity=sev))
                print(self.facts)
            elif len(autofill) == 0:
                suggestions = list(filter(lambda x: ans.replace(" ", "_") in x, self.symp_list))
                if len(suggestions) == 0:
                    print("Could not find any matching symptoms.\n")
                else:
                    print("Did you mean:")
                    print(suggestions)
                ans = ' '
            elif ans != '':
                print("Did you mean:")
                print(autofill)
                ans = ' '
                sev = ' '
        self.retract(f1)

    @Rule(AS.f1 << Query(symptom=MATCH.symp, severity=MATCH.sev))

    '''
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
    '''
if __name__ == "__main__":
    dis_symp_dict, symp_dis_dict, dis_list, symp_list = DataBase_Read()
    print(dis_symp_dict)
    print(symp_dis_dict)
    print(dis_list)
    print(symp_list)
    engine = Diagnose()
    engine.reset(dis_symp_dict=dis_symp_dict, symp_dis_dict=symp_dis_dict, symp_list=symp_list)  # Preparing the engine for the execution.
    print(engine.facts)
    engine.run()  # Runing
    print(engine.facts)
