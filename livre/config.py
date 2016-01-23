# Livre configuration file
# Edit this file to set global configuration variables.


# MAX_CIRCULATION_DAYS is used to calculate the due date when issuing a book.

MAX_CIRCULATION_DAYS = 14


# MAX_ISSUES_PER_USER is used to limit the maximum number of books can be issued to a user.

MAX_ISSUES_PER_USER = 3


# Fine to be collected on books returned after due date.

FINE_PER_DAY = 0.0


# Currency to be used when collecting fines.

CURRENCY = 'INR'


# Website configuration

SITE_CONFIG = {
    'SITE_NAME': 'Livre',
    'SITE_DESCRIPTION': 'Livre Library Management System',
}
