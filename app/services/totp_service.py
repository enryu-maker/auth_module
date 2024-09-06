import pyotp


def make_totp_secret():
    """ 
    Function for generating a secret for TOTP algorithm 
    """
    return pyotp.random_base32()
