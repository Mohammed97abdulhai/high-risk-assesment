from pyknow import *
from enum import Enum
from PyInquirer import prompt
import numpy as np


class Nationality(Fact):
    pass

class BusinessNature(Fact):
    pass

class Transaction(Fact):
    pass

class InquiredByCML(Fact):
    pass

class Beneficiary(Fact):
    pass

class calculateTotalRisk(Fact):
    pass

class CusomerType(Enum):
    individiual = 1
    joint = 2
    minor = 3
    VIP = 4
    non_profit_entity = 5


class Customer(Fact):
    def set_personal_info(self, first_name, last_name,father_name,mobile,address,country,city, nationality, gender, birth_date, martial_status):
        self.first_name = first_name
        self.last_name = last_name
        self.father_name = father_name
        self.mobile = mobile
        self.address = address
        self.country = country
        self.city = city
        self.nationality = nationality

    def set_customer_information(self,c_type,branch,business_nature,source_of_income,avg_yearly_income,deposit_threshold,withdrawal_threshold,is_beneficiary):
        self.customer_type = c_type
        self.branch = branch
        self.business_nature = business_nature
        self.source_of_income = source_of_income
        self.avg_yearly_income = avg_yearly_income
        self.deposit_threshold = deposit_threshold
        self.withdrawal_threshold = withdrawal_threshold
        self.is_beneficiary = is_beneficiary


class RiskFactor():
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight


def calculate_the_risk(reputaion , financial_legal , operational , adherence , control_system , procedures):
    inherent_risk = ((reputaion.value * reputaion.weight + financial_legal.value * financial_legal.weight + operational.value * operational.weight)
    / (reputaion.weight + financial_legal.weight + operational.weight))

    control_risk = ((adherence.value * adherence.weight + control_system.value * control_system.weight + procedures.value * procedures.weight)
    /(adherence.weight + control_system.weight + procedures.weight))

    risk = (inherent_risk + (2*(100 - control_risk)))/3
    return risk

maxx = 15
class RiskValue(Enum):
    high = maxx/3
    medium = (maxx/3)/2
    low = 0



class MainFactors():
    nationality_risk = RiskValue.low
    business_nature_risk = RiskValue.low
    transaction_risk = RiskValue.low



risk_array = np.array([
    [RiskValue.high, RiskValue.high, RiskValue.high, RiskValue.high],
    [RiskValue.high, RiskValue.high, RiskValue.medium, RiskValue.high],
    [RiskValue.high, RiskValue.high, RiskValue.low ,RiskValue.medium],
    [RiskValue.high, RiskValue.medium, RiskValue.high, RiskValue.high],
    [RiskValue.high, RiskValue.medium, RiskValue.medium, RiskValue.medium],
    [RiskValue.high, RiskValue.medium, RiskValue.low, RiskValue.medium],
    [RiskValue.high, RiskValue.low, RiskValue.high, RiskValue.medium],
    [RiskValue.high, RiskValue.low, RiskValue.medium, RiskValue.medium],
    [RiskValue.high, RiskValue.low, RiskValue.low, RiskValue.low],
    
    [RiskValue.medium, RiskValue.high, RiskValue.high, RiskValue.high],
    [RiskValue.medium, RiskValue.high, RiskValue.medium, RiskValue.medium],
    [RiskValue.medium, RiskValue.high, RiskValue.low, RiskValue.medium],
    [RiskValue.medium, RiskValue.medium, RiskValue.high, RiskValue.medium],
    [RiskValue.medium, RiskValue.medium, RiskValue.medium, RiskValue.medium],
    [RiskValue.medium, RiskValue.medium, RiskValue.low, RiskValue.low],
    [RiskValue.medium, RiskValue.low, RiskValue.high, RiskValue.medium],
    [RiskValue.medium, RiskValue.low, RiskValue.medium, RiskValue.low],
    [RiskValue.medium, RiskValue.low, RiskValue.low,RiskValue.low],

    [RiskValue.low, RiskValue.high, RiskValue.high, RiskValue.medium],
    [RiskValue.low, RiskValue.high, RiskValue.medium, RiskValue.medium],
    [RiskValue.low, RiskValue.high, RiskValue.low, RiskValue.low],
    [RiskValue.low, RiskValue.medium, RiskValue.high, RiskValue.medium],
    [RiskValue.low, RiskValue.medium, RiskValue.medium, RiskValue.low],
    [RiskValue.low, RiskValue.medium, RiskValue.low, RiskValue.low],
    [RiskValue.low, RiskValue.low, RiskValue.high, RiskValue.medium],
    [RiskValue.low, RiskValue.low, RiskValue.medium, RiskValue.low],
    [RiskValue.low, RiskValue.low, RiskValue.low, RiskValue.low],
])

def calculate_riskFactor_value(risk):
    if(risk >=23 and risk <= 35):
        return RiskValue.low
    elif(risk >= 36 and risk <=55):
        return RiskValue.medium
    elif(risk >=56 and risk <=73):
        return RiskValue.high

class InferenceEngine(KnowledgeEngine):
    @DefFacts()
    def func(self):
        yield calculateTotalRisk('yes')
    
    high_risk_nations = ["afghanistan","algeria","argentina","bahrain","brazil","china","colombia","cuba","djibouti","egypt","equatorial guinea","gibraltar","greece",
                            "india","indonesia","iran","iraq","lebanon","korea DPR","kuwait"]
    high_risk_business = ["lawyer","accountant","broker"]
    medium_risk_business = ["real estate","jewlery","cars"]

    @Rule(salience = 7)
    def startuprule(self):
        question = [
            {'type' : 'confirm',
             'message' : 'is the user inquired by CML?',
             'name' : 'inquired'}]
        inquired_answer = prompt(question)
        if inquired_answer['inquired']:
            self.declare(InquiredByCML())
    
    #high risk nations rule
    @Rule(Nationality(P(lambda x: str(x) in InferenceEngine.high_risk_nations)),salience = 2)
    def fuckogg(self):
        #calculate the inherent risk 
        reputaion = RiskFactor(80,100)
        financial_legal = RiskFactor(80,80)
        operational = RiskFactor(50,60)
        
        #calculate the control risk 
        adherence = RiskFactor(80,100)
        control_system = RiskFactor(80,80)
        procedures = RiskFactor(80,60)

        #calculate the overall risk
        risk = calculate_the_risk(reputaion,financial_legal,operational,adherence,control_system,procedures)
        risk = round(risk)
        print("nationality risk:",risk)
        MainFactors.nationality_risk = calculate_riskFactor_value(risk)
        print(MainFactors.nationality_risk)
        

    #high risk business rule
    @Rule(BusinessNature(P(lambda nature: str (nature) in InferenceEngine.high_risk_business)),salience=2)
    def fukcthishist(self):

        #calculate the inherent risk
        reputaion1 = RiskFactor(50,100)
        finanical_legal1 = RiskFactor(50,80)
        operational1 = RiskFactor(50,60)

        #calculate the control risk
        adherence1 = RiskFactor(80,100)
        control_system1 = RiskFactor(80,80)
        procedures1 = RiskFactor(50,60)

        #calulate the overall risk
        risk = calculate_the_risk(reputaion1,finanical_legal1,operational1,adherence1,control_system1,procedures1)
        risk = round(risk)
        print("business risk:",risk)

        MainFactors.business_nature_risk = calculate_riskFactor_value(risk)
        print(MainFactors.business_nature_risk)

    #medium risk business rule
    @Rule(BusinessNature(P(lambda nature : str (nature) in InferenceEngine.medium_risk_business)),salience=2)
    def sososo(self):
        #assign the corresponding value of the  inherent risk factors
        reputaion = RiskFactor(50,100)
        finanical_legal = RiskFactor(80,80)
        operational = RiskFactor(50,60)

        #assign the corresponding value of  the control risk factors
        adherence = RiskFactor(80,100)
        control_system = RiskFactor(80,80)
        procedures = RiskFactor(80,60)

        
        #calulate the overall risk
        risk = calculate_the_risk(reputaion,finanical_legal,operational,adherence,control_system,procedures)
        risk = round(risk)
        print("business risk: ",risk)
        MainFactors.business_nature_risk = calculate_riskFactor_value(risk)
        print(MainFactors.business_nature_risk)
    
    # withdrawal limit rule
    @Rule(Transaction(MATCH.withdrawal_list , MATCH.deposit_list, MATCH.withdrawal_threshold, MATCH.deposit_threshold),salience=2)
    def trans_limit_exceeded(self,withdrawal_list,deposit_list, withdrawal_threshold, deposit_threshold):
        withdrawal_checker = False
        deposit_checker = False
        for withdrawal in withdrawal_list : 
            if withdrawal > withdrawal_threshold:
                withdrawal_checker = True
                break
        for deposit in deposit_list :
            if deposit > deposit_threshold:
                deposit_checker = True
        if deposit_checker or withdrawal_checker :
            reputaion = RiskFactor(50,100)
            financial_legal = RiskFactor(80,80)
            operational = RiskFactor(80,60)

            adherence = RiskFactor(80,100)
            control_system = RiskFactor(80,80)
            procedures = RiskFactor(80,60)

            risk = calculate_the_risk(reputaion, financial_legal,operational,
                    adherence,control_system,procedures)
            risk = round(risk)
            print("transactions risk:",risk)
            MainFactors.transaction_risk = calculate_riskFactor_value(risk)
            print(MainFactors.transaction_risk)

    @Rule(EXISTS(InquiredByCML()),salience =6)
    def inquiredbycml(self):
        print("high risk")
        self.reset()

    @Rule(Beneficiary(),salience = 6)
    def beneficiary(self):
        print("high risk")
        self.reset()

    @Rule(calculateTotalRisk("yes"),salience = 1)
    def cal(self):
        total = (MainFactors.nationality_risk).value + (MainFactors.transaction_risk).value + (MainFactors.business_nature_risk).value
        print(total)
        if total >=0 and total <= maxx/3:
            print('low risk')
        elif total > maxx/3 and total <= (2* (maxx/3)):
            print('medium risk')
        elif total> (2* (maxx/3)) and total < maxx:
            print('high risk')

questions = [
    {
        'type' : 'input',
        'name' : 'first_name',
        'message' : 'enter your first name:',
        'default' : 'khaled'
    },
    {
        'type': 'input',
        'name' : 'last_name',
        'message' : 'enter your last name:',
        'default' : 'shoushara'
    },
    {
        'type':'input',
        'name' : 'father_name',
        'message' : 'enter your father name:',
        'default' : 'mohammad'
    },
    {
        'type' : 'input',
        'name' : 'mobile',
        'message' : 'enter your mobile phone number',
        'default' : '0944245'
    },
    {
        'type' : 'input',
        'name' : 'address',
        'message' : 'enter your address',
        'default' : 'kafersouseh'
    },
    {
        'type' : 'input',
        'name' : 'country',
        'message' : 'enter your current country',
        'default' : 'syria'
    },
    {
        'type' : 'input',
        'name' : 'city',
        'message' : 'enter your current city',
        'default' : 'damascus'
    },
    {
        'type' : 'input',
        'name' : 'nationality',
        'message' : 'enter your noationality',
        'default' : "algeria"
    },
    {
        'type' : 'checkbox',
        'name' : 'gender',
        'message' : 'choose your gender',
        'choices' : [{'name' : 'male'} , {'name' : 'female'}]
    },
    {
        'type' : 'checkbox',
        'name' : 'customer_type',
        'message' : 'choose oyur account type',
        'choices' : [
            {
                'name' : 'individual'
            },
            {
                'name' : 'joint'
            },
            {
                'name' : 'minor'
            },
            {
                'name' : 'vip'
            },
            {
                'name' : 'non_profit entity'
            }
        ]
    },
    {
        'type' : 'input',
        'name' : 'branch',
        'message' : 'enter your branch:',
        'default' : 'damascus'
    },
    {
        'type' : 'input',
        'name' : 'business_nature',
        'message' : 'enter your career job:',
        'default' : 'lawyer'
    },
    {
        'type' : 'input',
        'name' : 'source_of_income',
        'message' : 'enter your source of income:'
    },
    {
        'type' : 'input',
        'name' : 'average_yearly_income',
        'message' : 'enter your average yearly income:',
        'default' : '6000'
    },
    {
        'type' : 'input',
        'name' : 'deposit_threshold',
        'message' : 'enter your deposit threshold',
        'default' : '400'
    },
    {
        'type' : 'input',
        'name' : 'withdrawal_threshold',
        'message' : 'enter you withdrawal threshold',
        'default' : '400'
    },
    {
        'type': 'confirm',
        'message': 'is your the beneficiary?',
        'name': 'beneficiary',
        'default': True,
    }
]
    
    
answers = prompt(questions)
print(answers['first_name'])
customer = Customer()
customer.set_personal_info(answers['first_name'],answers['last_name'], answers['father_name'],answers['mobile'],answers['address'],
answers['country'],answers['city'],answers['nationality'],answers['gender'],97,"single")
customer.set_customer_information(CusomerType.individiual, answers['branch'],answers['business_nature'],"nothing",int(answers['average_yearly_income']),
int(answers['deposit_threshold']),int(answers['withdrawal_threshold']), answers['beneficiary'])
questions1 = [
    {
        'type' : 'confirm',
        'message' : 'do you want to make transaction',
        'name' : 'transaction',
        'default' : True,
    }
]
answers1 = prompt(questions1)
trans = answers1['transaction']
deposit_transaction = []
withdrawal_transaction = []
while trans is True :
    ask_about_trans = [
        {
            'type' : 'checkbox',
            'message' : 'what type of transaction do you want',
            'name' : 'transaction_selection',
            'choices' : [
            {
                'name' : 'deposit',
                'checked' : True
            },
            {
                'name' : 'withdrawal'
            }
        ],
        }
    ]
    trans_answers = prompt(ask_about_trans)
    trans_amount = int(input("enter the amount of your transaction:"))
    print(trans_answers)
    if trans_answers['transaction_selection'][0] == 'deposit':
        deposit_transaction.append(trans_amount)
    else :
        withdrawal_transaction.append(trans_amount)

    answers = prompt(questions1)
    trans = answers['transaction']

print(withdrawal_transaction)
print(deposit_transaction)
inferenceEngine = InferenceEngine()
inferenceEngine.reset()
inferenceEngine.declare(Nationality(customer.nationality),
                        BusinessNature(customer.business_nature),
                        Transaction(withdrawal_transaction, deposit_transaction, customer.withdrawal_threshold, customer.deposit_threshold))

if customer.is_beneficiary:
    inferenceEngine.declare(Beneficiary())

inferenceEngine.run()

