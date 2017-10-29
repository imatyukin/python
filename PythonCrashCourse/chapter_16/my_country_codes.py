from pygal.maps.world import COUNTRIES

def get_country_code(country_name):
    """Return the Pygal 2-digit country code for the given country."""
    for code, name in COUNTRIES.items():
        if country_name == 'Yemen, Rep.':
            return 'ye'
        elif name == country_name:
            return code
    # If the country wasn't found, return None.
    return None
