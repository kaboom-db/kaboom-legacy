def util_calculate_age(dob, dod) -> int:
    return dod.year - dob.year - ((dod.month, dod.day) < (dob.month, dob.day))
