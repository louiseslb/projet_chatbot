from faker import Faker
import datetime

fake = Faker()
"""for _ in range(40):
    print('- [' + str(fake.day_of_month()) + '/' + str(fake.month()) + '/' + str(fake.date_this_decade().year) + '](date)')
for _ in range(40):
    print('- [' + str(fake.day_of_month()) + '/' + str(fake.month()) + '/' + str(2022) + '](date)')
"""

"""for i in range(30):
    print('- [' + str(i) + '](number)')"""

"""for i in range(50):
    print('- [' + fake.company_email() + '](mail)')"""