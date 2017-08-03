#!/usr/bin/env python3
from users import Admin

admin = Admin('root', '', '0', 'wheel')
admin.privileges.show_privileges()
