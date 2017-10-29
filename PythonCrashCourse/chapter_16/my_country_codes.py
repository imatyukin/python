from pygal.maps.world import COUNTRIES

def get_country_code(country_name):
    """Return the Pygal 2-digit country code for the given country."""
    for code, name in COUNTRIES.items():
        if country_name == 'Bolivia, Plurinational State of':
            return 'bo'
        if country_name == 'Congo, the Democratic Republic of the':
            return 'cd'
        if country_name == "Cote d'Ivoire":
            return 'ci'
        if country_name == 'Iran, Islamic Republic of':
            return 'ir'
        if country_name == "Korea, Democratic People's Republic of":
            return 'kp'
        if country_name == 'Korea, Republic of':
            return 'kr'
        if country_name == "Lao People's Democratic Republic":
            return 'do'
        if country_name == 'Moldova, Republic of':
            return 'md'
        if country_name == 'Macedonia, the former Yugoslav Republic of':
            return 'mk'
        if country_name == 'Palestine, State of':
            return 'ps'
        if country_name == 'Saint Helena, Ascension and Tristan da Cunha':
            return 'sh'
        if country_name == 'Taiwan, Province of China':
            return 'tw'
        if country_name == 'Tanzania, United Republic of':
            return 'tz'
        if country_name == 'Holy See (Vatican City State)':
            return 'va'
        if country_name == 'Venezuela, Bolivarian Republic of':
            return 've'
        elif name == country_name:
            return code
    # If the country wasn't found, return None.
    return None
