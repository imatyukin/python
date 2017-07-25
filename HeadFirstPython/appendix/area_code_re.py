#!/usr/bin/env python3

import re

phone_number = "Home: (555) 265-2901"

results = re.search('\((\d{3})\)', phone_number)
area_code = results.group(1)

print('The area code is: ' + area_code)