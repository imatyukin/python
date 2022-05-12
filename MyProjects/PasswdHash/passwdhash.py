import crypt
import getpass

print(crypt.crypt(getpass.getpass(), crypt.mksalt(crypt.METHOD_MD5)))
