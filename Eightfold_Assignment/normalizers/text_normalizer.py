def normalize_name(name):

    if not name:
        return None

    return name.strip().title()


def normalize_email(email):

    if not email:
        return None

    return email.strip().lower()