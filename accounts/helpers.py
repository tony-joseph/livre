# Accounts helpers


def is_admin(user):
    """ Checks the is_superuser fields in user model.
    :param user: User object
    :return: boolean
    """

    return user.is_superuser


def is_staff(user):
    """ Checks the is_staff fields in user model.
    :param user: User object
    :return: boolean
    """

    return user.is_staff
