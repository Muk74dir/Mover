from decouple import config
API_KEY = config('API_KEY')

ACCOUNT_TYPE = (
    ('Passenger', 'Passenger'),
    ('Driver', 'Driver')
)

PERSON_STATUS = (
    ('Busy', 'Busy'),
    ('Available', 'Available')
)
