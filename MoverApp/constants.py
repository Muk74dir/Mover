from decouple import config
API_KEY = config('API_KEY')
STRIPE_API_KEY = config('STRIPE_API_KEY')

ACCOUNT_TYPE = (
    ('Passenger', 'Passenger'),
    ('Driver', 'Driver')
)

PERSON_STATUS = (
    ('Busy', 'Busy'),
    ('Available', 'Available')
)

VEHICLE_TYPE = (
    ('BIKE', 'BIKE'),
    ('CAR', 'CAR')
)