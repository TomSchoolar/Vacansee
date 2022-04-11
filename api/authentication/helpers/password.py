


def correctPassword(givenPassword, user):
    # function to check given password is correct
    # TODO replace with hashing system
    if givenPassword != user['PasswordHash']:
        return False
    return True