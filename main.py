from faker import Faker
import datetime
import re

fake = Faker()
"""for _ in range(40):
    print('- [' + str(fake.day_of_month()) + '/' + str(fake.month()) + '/' + str(fake.date_this_decade().year) + '](date)')
for _ in range(40):
    print('- [' + str(fake.day_of_month()) + '/' + str(fake.month()) + '/' + str(2022) + '](date)')
"""

"""for i in range(30):
    print('- [' + str(i) + '](number)')"""

"""for i in range(50):
    print(fake.company_email())"""

r = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
if r.match("louise@gmailm"):
    print('ok')
else:
    print('not ok')