import sys
import json
from faker import Faker
from django.conf import settings
from random import choice, sample, randrange

settings.configure()

from django.contrib.auth.hashers import make_password

class Fake():
    userPK = 1000
    profilePK = 1000
    employerPK = 1000
    vacancyPK = 1000
    favouritePK = 1000
    applicationPK = 1000
    outpath = './authentication/fixtures/'

    fake = Faker()

    def __init__(self, type):
        if type == 'full':
            self.outpath += 'fullseed.json'

            self.params = {
                'employees': 34,
                'vacanciesLower': 14,
                'vacanciesUpper': 25,
                'applicantsLower': 8,
                'applicantsUpper': 20,
                'favouritesLower': 3,
                'favouritesUpper': 11,
            }

        elif type == 'test':
            self.outpath += 'testseed.json'

            self.params = {
                'employees': 8,
                'vacanciesLower': 3,
                'vacanciesUpper': 7,
                'applicantsLower': 3,
                'applicantsUpper': 6,
                'favouritesLower': 3,
                'favouritesUpper': 5,
            }



    def User(self, employer = False):
        user = {
            'model': 'authentication.User',
            'pk': self.userPK,
            'fields': {
                'IsEmployer': employer,
                'Email': self.fake.free_email(),
                'Password': make_password('password')
            }
        }

        self.userPK += 1

        return user


    def Profile(self, user):
        if user['fields']['IsEmployer']:
            return

        pronouns = ['He/Him', 'She/Her', 'They/Them']
        quals = [
            f'{ choice(range(2,13))} GCSEs',
            f'{ choice(range(1,5))} A-Levels',
            f'{ choice(range(1,12))} O-Levels',
            'PhD',
            'BSc',
            'BA',
            'MSci',
            'MA'
        ]
        
        profile = {
            'model': 'employee.Profile',
            'pk': self.profilePK,
            'fields': {
                'UserId': user['pk'],
                'FirstName': self.fake.first_name(),
                'LastName': self.fake.last_name(),
                'Pronouns': choice(pronouns),
                'TimeZone': choice(range(-11,12,1)),
                'TopicSentence': self.fake.sentence(nb_words=12, variable_nb_words=True),
                'NotableSkills': [self.fake.bs() for x in range(choice(range(1,4)))],
                'Experience': [self.fake.sentence(nb_words=3, variable_nb_words=True) for x in range(choice(range(1,4)))],
                'Qualifications': [choice(quals) for x in range(choice(range(1,4)))],
                'PhoneNumber': self.fake.phone_number(),
                'Location': self.fake.location_on_land()[2]
            }
        }

        self.profilePK += 1

        return profile

    
    def EmployerDetails(self, user):
        if not user['fields']['IsEmployer']:
            return
        
        employerDetails = {
            'model': 'employer.EmployerDetails',
            'pk': self.employerPK,
            'fields': {
                'UserId': user['pk'],
                'PhoneNumber': self.fake.phone_number(),
                'CompanyName': self.fake.company()[:29]
            }
        }

        self.employerPK += 1

        return employerDetails

    
    def Vacancy(self, user):
        if not user['fields']['IsEmployer']:
            return

        salaries = [f'{ choice(["$", "£"]) }{ choice(range(4,100)) },000', 'Competitive', 'NMW']

        vacancy = {
            'model': 'employer.Vacancy',
            'pk': self.vacancyPK,
            'fields': {
                'VacancyName': self.fake.job(),
                'UserId': user['pk'],
                'Salary': choice(salaries),
                'Description': self.fake.sentence(nb_words=40, variable_nb_words=True)[:149],
                'SkillsRequired': [self.fake.bs() for x in range(choice(range(1,4)))],
                'ExperienceRequired': [self.fake.sentence(nb_words=3, variable_nb_words=True) for x in range(choice(range(1,4)))],
                'TimeZone': choice(range(-11,12,1)),
                'Tags': sample([x for x in range(1,20)], choice(range(2,8))),
                'IsOpen': choice([True, True, True, True, False]),
                'PhoneNumber': self.fake.phone_number(),
                'Email': self.fake.free_email(),
                'Created': self.fake.date_time_this_year().strftime('%Y-%m-%dT%H:%M:%S+00:00'),
                'Location': self.fake.location_on_land()[2]
            }
        }

        self.vacancyPK += 1

        return vacancy


    def Favourite(self, user, vacancy):
        if user['fields']['IsEmployer']:
            return

        if not vacancy['fields']['IsOpen']:
            return
        
        favourite = {
            'model': 'employee.Favourite',
            'pk': self.favouritePK,
            'fields': {
                'UserId': user['pk'],
                'VacancyId': vacancy['pk']
            }
        }
        
        self.favouritePK += 1

        return favourite

    
    def Application(self, user, vacancy):
        if user['fields']['IsEmployer']:
            return

        options = ['MATCHED', 'PENDING', 'PENDING', 'PENDING', 'REJECTED', 'REJECTED']

        application = {
            'model': 'employee.Application',
            'pk': self.applicationPK,
            'fields': {
                'UserId': user['pk'],
                'VacancyId': vacancy['pk'],
                'ApplicationStatus': choice(options),
                'LastUpdated': self.fake.date_time_this_year().strftime('%Y-%m-%dT%H:%M:%S+00:00')
            }
        }

        self.applicationPK += 1

        return application


def readFixtures():
    employees = []
    employers = []
    profiles = []
    employerDetails = []
    vacancies = []
    favourites = []
    applications = []
    tags = []

    with open('./authentication/fixtures/fixtures.json', 'r') as file:
        data = json.load(file)

    for x in data:
        model = x['model']

        if model == 'authentication.User':
            userType = x['fields']['IsEmployer']

            if userType:
                employers.append(x)
                continue
            employees.append(x)
        
        
        
        if model == 'employee.Profile':
            profiles.append(x)
            continue
            
        if model == 'employer.EmployerDetails':
            employerDetails.append(x)
            continue
    
        if model == 'employer.Vacancy':
            vacancies.append(x)
            continue

        if model == 'employee.Favourite':
            favourites.append(x)
            continue
            
        if model == 'employee.Application':
            applications.append(x)

        if model == 'employer.Tag':
            tags.append(x)

    return [
        employees,
        employers,
        profiles, 
        employerDetails, 
        vacancies, 
        favourites, 
        applications,
        tags
    ]


def generateData(limits):
    fixtures = readFixtures()
    
    employees = fixtures[0]
    employers = fixtures[1]
    profiles = fixtures[2]
    employerDetails = fixtures[3]
    vacancies = fixtures[4]
    favourites = fixtures[5]
    applications = fixtures[6]
    tags = fixtures[7]


    for x in range(limits['employees']):  # full: 25, test: 2
        # add employees
        user = f.User()
        employees.append(user)
        profile = f.Profile(user)

        if profile != None:
            profiles.append(profile)

    # do not switch around
    emptyEmployer = [emp for emp in employers if emp['pk'] == 7]
    employers = [emp for emp in employers if emp['pk'] != 7]    

    # do not switch around
    emptyEmployerDetails = [emp for emp in employerDetails if emp['fields']['UserId'] == 7]
    employerDetails = [emp for emp in employerDetails if emp['fields']['UserId'] != 7]

    # for x in range(25):
    #     user = f.User(True)
    #     employers.append(user)
    #     details = f.EmployerDetails(user)

    #     if details != None:
    #         employerDetails.append(details)

    for employer in employers:
        vacs = [f.Vacancy(employer) for x in range(choice(range(limits['vacanciesLower'], limits['vacanciesUpper'])))] # full: 14,25  test: 3,7
        vacancies += [el for el in vacs if el != None]

    for vacancy in vacancies:
        applicants = [employees.pop(randrange(len(employees))) for _ in range(choice(range(limits['applicantsLower'], limits['applicantsUpper'])))] # full: 8,20  test: 3,6
        #applicants = sample(employees, choice(range(limits['applicantsLower'], limits['applicantsUpper'])))   # full: 8,20  test: 3,6
        for applicant in applicants:
            app = f.Application(applicant, vacancy)

            if app != None:
                applications.append(app)
        
        favouriters = sample(employees, choice(range(limits['favouritesLower'], limits['favouritesUpper'])))   # full: 3,11  test: 2,5
        
        for favouriter in favouriters:
            fav = f.Favourite(favouriter, vacancy)
            if fav != None:
                favourites.append(fav)

        employees += applicants

    compiledData = employees + employers + profiles + employerDetails + vacancies + favourites + applications + tags + emptyEmployer + emptyEmployerDetails

    prettierData = json.dumps(compiledData, indent=4)

    return prettierData



if __name__ == '__main__':
    try:
        type = sys.argv[1].lower()
        
        if type not in ['test', 'full']:
            print('Invalid dataset type: must be either \'test\' or \'full\' (default)')
            exit()
    except IndexError as err:
        type = 'full'

    f = Fake(type)

    data = generateData(f.params)

    with open(f.outpath, 'w') as outfile:
        outfile.write(data)



