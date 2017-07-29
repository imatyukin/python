#!/usr/bin/env python3

def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
    profile = {}
    profile['first_name'] = first
    profile['last_name'] = last
    for key, value in user_info.items():
        profile[key] = value
    return profile

user_profile = build_profile('igor', 'matyukin',
                             id='1',
                             group='root',
                             shell='/bin/bash')
print(user_profile)
