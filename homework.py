from pyknow import *
from enum import Enum
from PyInquirer import *


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

class RisedualRisk():
    risedual_nationality = 0
    risedual_business = 0
    risedual_transaction =0

def calculate_the_risk(reputaion , financial_legal , operational , adherence , control_system , procedures):
    inherent_risk = ((reputaion.value * reputaion.weight + financial_legal.value * financial_legal.weight + operational.value * operational.weight)
    / (reputaion.weight + financial_legal.weight + operational.weight))

    control_risk = ((adherence.value * adherence.weight + control_system.value * control_system.weight + procedures.value * procedures.weight)
    /(adherence.weight + control_system.weight + procedures.weight))

    risk = (inherent_risk + (2*(100 - control_risk)))/3
    return risk

class InferenceEngine(KnowledgeEngine):
    #another dumb shit i think but i don't know any other way to represent it and i don't think the deffacts can do the same thing i am trying to do
    high_risk_nations = ["afghanistan","algeria","argentina","bahrain","brazil","china","colombia","cuba","djibouti","egypt","equatorial guinea","gibraltar","greece",
                            "india","indonesia","iran","iraq","lebanon","korea DPR","kuwait"]
    high_risk_business = ["lawyer","accountant","broker"]
    medium_risk_business = ["real estate","jewlery","cars"]
    
    #high risk nations rule
    @Rule(Nationality(P(lambda x: str(x) in InferenceEngine.high_risk_nations)))
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
        print("nationality risk:",risk)
        

    #high risk business rule
    @Rule(BusinessNature(P(lambda nature: str (nature) in InferenceEngine.high_risk_business)))
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
        print("business risk:",risk)

    #medium risk business rule
    @Rule(BusinessNature(P(lambda nature : str (nature) in InferenceEngine.medium_risk_business)))
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
        print("business risk: ",risk)


    # withdrawal limit rule
    @Rule(Transaction(MATCH.trans ,  MATCH.threshold))
    def trans_limit_exceeded(self,trans, threshold):
        if(trans > threshold):
            reputaion = RiskFactor(50,100)
            financial_legal = RiskFactor(80,80)
            operational = RiskFactor(80,60)

            adherence = RiskFactor(80,100)
            control_system = RiskFactor(80,80)
            procedures = RiskFactor(80,60)

            risk = calculate_the_risk(reputaion, financial_legal,operational,
                    adherence,control_system,procedures)
            print("transactions risk:",risk)

    @Rule(EXISTS(InquiredByCML()))
    def inquiredbycml(self):
        print("high risk")

    @Rule(Beneficiary(),salience = 6)
    def beneficiary(self):
        print("high risk")

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
        #to do validate the number
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
        'default' : "syria"
    },
    {
        'type' : 'checkbox',
        'name' : 'gender',
        'message' : 'choose your gender',
        'choices' : [{'name' : 'male'} , {'name' : 'female'},{'name': 'non binary'}]
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
        #TODO validate it's a valid job
    },
    {
        'type' : 'input',
        'name' : 'source_of_income',
        'message' : 'enter your source of income:'
    },
    {
        'type' : 'input',
        'name' : 'average_yearly_income',
        'message' : 'enter your average yearly income:'
        #TODO :validate it's a number
    },
    {
        'type' : 'input',
        'name' : 'deposit_threshold',
        'message' : 'enter your deposit threshold'
        #TODO :validate it's a number
    },
    {
        'type' : 'input',
        'name' : 'withdrawal_threshold',
        'message' : 'enter you withdrawal threshold'
        #TODO :validate it's a number
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

user_trans = int(input("enter  your transaction:"))
inferenceEngine = InferenceEngine()
inferenceEngine.reset()
inferenceEngine.declare(Nationality(customer.nationality),Beneficiary(),BusinessNature(customer.business_nature),
Transaction(user_trans, customer.withdrawal_threshold))
inferenceEngine.run()