#!/usr/bin/env python3
from privileges import Admin

admin = Admin('Igor', 'Matyukin', '1', 'wheel')
admin.privileges.show_privileges()