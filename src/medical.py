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

class Error(Fact):
    pass

class Result(Fact):
    name = Field(str, mandatory=True)

class DiseaseWatch(Fact):
    diseases = Field(list, mandatory=True)
    completed = Field(bool, mandatory=True)

class DiseaseStub(Fact):
    name = Field(str)

class Count(Fact):
    name = Field(str, mandatory=True)
    required = Field(int, mandatory=True)
    obtained = Field(int, mandatory=True)
    symptom = Field(list, mandatory=True)

class MaxCount(Count):
    pass

class Ratio(Fact):
    ratio=Field(float, mandatory=True)

class Transaction(Fact):
    symptom = Field(str)
    severity = Field(Severity)
    disease = Field(str)

class Query(Fact):
    symptom = Field(str, mandatory=True)
    severity = Field(Severity, mandatory=True)

def DataBase_Read():
    with open("diseases.txt") as diseases_t:
        diseases_list = [a.strip()  for a in diseases_t.read().split("\n") if a != '']
    disease_symptom_dict = {}
    #print(diseases_list)
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


def print_likely_disease(disease):
    id_disease = disease
    disease_details = get_details(id_disease)
    treatments = get_treatments(id_disease)
    print("\n\nA likely disease that you have is: {}".format(id_disease))
    print("A short description of the disease is given below :\n")
    print(disease_details)
    print("The common medications and procedures suggested by other real doctors are:\n")
    print(treatments)

def print_definite_disease(disease):
    id_disease = disease
    disease_details = get_details(id_disease)
    treatments = get_treatments(id_disease)
    print("\n\nThe most probable disease that you have is {}".format(disease))
    print("\nA short description of the disease is given below :\n")
    print(disease_details)
    print("\nThe common medications and procedures suggested by other real doctors are:\n")
    print(treatments)

class Diagnose(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self, dis_symp_dict, symp_dis_dict, symp_list):
        for symptom in symp_dis_dict:
            yield Symptom(name=symptom, disease=symp_dis_dict[symptom])
        for disease in dis_symp_dict:
            yield Disease(name=disease, symptom=dis_symp_dict[disease]['symp'], severity=dis_symp_dict[disease]['sev'])
        self.symp_list = symp_list
        self.diagnosis = []
        self.incomplete = False
        self.all_matches = []

    @Rule(salience=1000)
    def startup(self):
        self.patients = input("Patient's Name: ").strip().upper()
        print("Hello! I am a Custom Diagnosis Expert System (CUSTODES)\n"
                "I am here to help you diagnose your disease.\n"
                "Please start typing in your symptoms and its severity."
                "Press enter on a blank line to get diagnosis")
        self.declare(Task('type-symptom'))

    @Rule(AS.f1 << Task('type-symptom'))
    def type_symptom(self, f1):
        ans = ' '
        sev = ' '
        to_check_duplicates = {}
        while ans != '' and sev != '':
            ans = input('Symptom>').strip().lower()
            autofill = list(filter(lambda x: x.startswith(ans), self.symp_list))
            if len(autofill) == 1 or ans.replace(" ", "_").strip() in self.symp_list:
                if not ans.replace(" ", "_").strip() in self.symp_list:
                    ans = autofill[0]
                    print(ans.replace("_", " "))
                sev = input('Severity (0-5)>')
                try:
                    sev = Severity(int(sev))
                except ValueError:
                    print("Please enter a number between 0 - 5")
                    sev = ' '
                    continue
                to_check_duplicates[ans] = sev
            elif len(autofill) == 0:
                suggestions = list(filter(lambda x: ans.replace(" ", "_") in x, self.symp_list))
                if len(suggestions) == 0:
                    print("Could not find any matching symptoms.\n")
                else:
                    print("Did you mean:")
                    print([x.replace("_", " ") for x in suggestions])
                ans = ' '
            elif ans != '':
                print("Did you mean:")
                print(autofill)
                ans = ' '
                sev = ' '
        for symp in to_check_duplicates:
            self.declare(Query(symptom=symp, severity=to_check_duplicates[symp]))
        self.retract(f1)
        print(self.facts)

    @Rule(NOT(Task()),
          AS.f1 << Query(symptom=MATCH.symp, severity=MATCH.sev),
          Symptom(name=MATCH.symp, disease=MATCH.dis))
    def process_input_query(self, f1, symp, sev, dis):
        for disease in dis:
            self.declare(Transaction(symptom=symp, severity=sev, disease=disease))
        self.retract(f1)

    @Rule(Transaction(symptom=MATCH.symp, severity=MATCH.sev, disease=MATCH.dis),
          Disease(name=MATCH.dis, symptom=MATCH.sy, severity=MATCH.se))
    def create_count(self, dis, sy):
        self.declare(Count(name=dis, required=len(sy), obtained=0, symptom=[]))
        self.declare(DiseaseStub(name=dis))

    @Rule(AS.f1 << Transaction(symptom=MATCH.symp, severity=MATCH.sev, disease=MATCH.dis),
          Disease(name=MATCH.dis, symptom=MATCH.syflist, severity=MATCH.sevflist),
          AS.f2 << Count(name=MATCH.dis, required=MATCH.req, obtained=MATCH.obt, symptom=MATCH.clist))
    def count_activations(self, f1, f2, symp, sev, syflist, sevflist, req, obt, clist):
        try:
            idx = syflist.index(symp)
            sev0, sev1 = sevflist[idx]
            if sev.value <= sev1.value and sev.value >= sev0.value:
                in_list = list(clist)
                in_list.append(tuple([symp, sev]))
                self.modify(f2, obtained=obt+1, symptom=in_list)
        except ValueError:
            self.declare(Error("Something went wrong."))
        self.retract(f1)

    @Rule(NOT(Transaction()), NOT(DiseaseWatch()),
          EXISTS(Count()))
    def add_disease_watcher(self):
        self.declare(DiseaseWatch(diseases=[], completed=False))

    @Rule(AS.f1 << DiseaseWatch(diseases=MATCH.dis_list, completed=MATCH.com),
          AS.f2 << DiseaseStub(name=MATCH.dis))
    def add_diseases_to_watcher(self, f1, f2, dis, dis_list):
        in_list = list(dis_list)
        if dis not in in_list:
            in_list.append(dis)
        self.modify(f1, diseases=in_list)
        self.retract(f2)

    @Rule(AS.f1 << DiseaseWatch(diseases=MATCH.dis_list, completed=MATCH.com),
          TEST(lambda com: not com),
          NOT(DiseaseStub()))
    def mark_disease_completion(self, f1):
        self.modify(f1, completed=True)

    @Rule(AS.f1 << DiseaseWatch(diseases=MATCH.dis_list, completed=MATCH.com),
          TEST(lambda dis_list: len(dis_list) > 0),
          TEST(lambda com: com),
          AS.f2 << Count(name=MATCH.dis, required=MATCH.req, obtained=MATCH.obt, symptom=MATCH.clist))
    def obtain_exact_diagnosis(self, f1, f2, dis, req, obt, dis_list):
        if req == obt:
            self.retract(f2)
            self.all_matches.append(dis)
            self.declare(Result(name=dis))
        if dis in dis_list:
            in_list = list(dis_list)
            try:
                in_list.remove(dis)
            except ValueError:
                in_list = []
                self.declare(Error("Something went wrong while obtaining exact diagnosis"))
            self.modify(f1, diseases=in_list)

    @Rule(AS.f1 << DiseaseWatch(diseases=MATCH.dis_list, completed=MATCH.com),
          TEST(lambda dis_list: len(dis_list) == 0),
          TEST(lambda com: com),
          NOT(Task()),
          Result())
    def signal_exact_completion():
        self.declare(Task('store-result'))
        self.retract(f1)

    @Rule(AS.f1 << DiseaseWatch(diseases=MATCH.dis_list, completed=MATCH.com),
          TEST(lambda dis_list: len(dis_list) == 0),
          TEST(lambda com: com),
          NOT(Task()),
          NOT(Result()))
    def incomplete_information(self, f1):
        self.incomplete = True
        self.retract(f1)
        self.declare(Task('best-match'))
        self.declare(Ratio(ratio=0.0))

    @Rule(Task('best-match'),
          AS.f1 << Count(name=MATCH.dis, required=MATCH.req, obtained=MATCH.obt, symptom=MATCH.clist),
          AS.f2 << Ratio(ratio=MATCH.ratio),
          TEST(lambda req, obt, ratio: obt/req > ratio))
    def compute_max(self, f1, f2, req, obt):
        self.modify(f2, ratio=obt/req)

    @Rule(Task('best-match'),
          AS.f1 << Count(name=MATCH.dis, required=MATCH.req, obtained=MATCH.obt, symptom=MATCH.clist),
          AS.f2 << Ratio(ratio=MATCH.ratio),
          TEST(lambda req, obt, ratio: obt/req < ratio))
    def remove_mins(self, f1, f2, dis, req, obt):
        self.retract(f1)
        self.all_matches.append(tuple((dis, obt, req)))

    @Rule(Task('best-match'),
        AS.f1 << Count(name=MATCH.dis, required=MATCH.req, obtained=MATCH.obt, symptom=MATCH.clist),
        AS.f2 << Ratio(ratio=MATCH.ratio),
        TEST(lambda req, obt, ratio: obt/req == ratio))
    def keep_max(self, f1, f2, dis, req, obt, clist):
        self.retract(f1)
        self.all_matches.append(tuple((dis, obt, req)))
        self.declare(MaxCount(name=dis, required=req, obtained=obt, symptom=clist))

    @Rule(AS.f2 << Task('best-match'), NOT(Count()), AS.f1 << Ratio(ratio=MATCH.ratio))
    def cleanup_max_operation(self, f1, f2):
        self.retract(f1)
        self.retract(f2)
        self.declare(Task('store-result'))

    @Rule(AS.f1 << MaxCount(name=MATCH.dis, required=MATCH.req, obtained=MATCH.obt, symptom=MATCH.clist))
    def max_to_result(self, f1, dis):
        self.retract(f1)
        self.declare(Result(name=dis))

    @Rule(Task('store-result'),
          AS.f3 << Result(name=MATCH.dis))
    def store_result(self, f3, dis):
        self.diagnosis.append(dis)
        self.retract(f3)

if __name__ == "__main__":
    dis_symp_dict, symp_dis_dict, dis_list, symp_list = DataBase_Read()
    '''
    Print debugging!
    print(dis_symp_dict)
    print(symp_dis_dict)
    print(dis_list)
    print(symp_list)
    '''
    engine = Diagnose()
    engine.reset(dis_symp_dict=dis_symp_dict, symp_dis_dict=symp_dis_dict, symp_list=symp_list)  # Preparing the engine for the execution.
    '''
    print(engine.facts)
    '''
    engine.run()
    '''
    print(engine.facts)
    print(engine.all_matches)
    print(engine.diagnosis)
    print(engine.incomplete)
    '''
    print("Hey {},".format(engine.patients))
    if not engine.incomplete:
        for dis in engine.diagnosis:
            print_definite_disease(dis)
        likely_disease = engine.all_matches
        for item in engine.diagnosis:
            try:
                likely_disease.remove(item)
            except ValueError:
                pass
        for dis, obt, req in likely_disease:
            print_likely_disease(dis)
    else:
        likely_disease = engine.diagnosis
        for dis in likely_disease:
            print_likely_disease(dis)
