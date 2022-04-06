def validate_phone_number(phone_number: str):
    import re
    phone_regex = re.compile("^(01)\d{1}\d{3,4}\d{4}$")
    phone_validation = phone_regex.search(phone_number)
    return phone_validation
