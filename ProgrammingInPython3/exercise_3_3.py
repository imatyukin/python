#!/usr/bin/env python3
# 3. Modify the generate_usernames.py program so that it prints the details of
#    two users per line, limiting names to 17 characters and outputting a form
#    feed character after every 64 lines, with the column titles printed at the
#    start of every page. Here’s a sample of the expected output:
#
#    Name                ID   Username  Name                ID   Username
#    ----------------- ------ --------- ----------------- ------ ---------
#    Aitkin, Shatha... (2370) saitkin   Alderson, Nicole. (8429) nalderso
#    Allison, Karma... (8621) kallison  Alwood, Kole E... (2095) kealwood
#    Annie, Neervana.. (2633) nannie    Apperson, Lucyann (7282) leappers
#
#    This is challenging. You’ll need to keep the column titles in variables so
#    that they can be printed when needed, and you’ll need to tweak the format
#    specifications to accommodate the narrower names. One way to achieve
#    pagination is to write all the output items to a list and then iterate over
#    the list using striding to get the left- and right-hand items,and using zip()
#    to pair them up. A solution is provided in generate_usernames_ans.py and
#    a longer sample data file is provided in data/users2.txt.

import collections
import sys


ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range(5)

User = collections.namedtuple("User",
            "username forename middlename surname id")


def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(
              sys.argv[0]))
        sys.exit()

    usernames = set()
    users = {}
    for filename in sys.argv[1:]:
        with open(filename, encoding="utf8") as file:
            for line in file:
                line = line.rstrip()
                if line:
                    user = process_line(line, usernames)
                    users[(user.surname.lower(), user.forename.lower(),
                            user.id)] = user
    print_users(users)


def process_line(line, usernames):
    fields = line.split(":")
    username = generate_username(fields, usernames)
    user = User(username, fields[FORENAME], fields[MIDDLENAME],
                fields[SURNAME], fields[ID])
    return user


def generate_username(fields, usernames):
    username = ((fields[FORENAME][0] + fields[MIDDLENAME][:1] +
                 fields[SURNAME]).replace("-", "").replace("'", ""))
    username = original_name = username[:8].lower()
    count = 1
    while username in usernames:
        username = "{0}{1}".format(original_name, count)
        count += 1
    usernames.add(username)
    return username


def print_users(users):
    namewidth = 17
    usernamewidth = 9
    columngap = " " * 2

    headline1 = "{0:<{nw}} {1:^6} {2:{uw}}".format("Name", "ID",
            "Username", nw=namewidth, uw=usernamewidth)
    headline2 = "{0:-<{nw}} {0:-<6} {0:-<{uw}}".format("",
            nw=namewidth, uw=usernamewidth)
    header = (headline1 + columngap + headline1 + "\n" +
              headline2 + columngap + headline2)

    lines = []
    for key in sorted(users):
        user = users[key]
        initial = ""
        if user.middlename:
            initial = " " + user.middlename[0]
        name = "{0.surname}, {0.forename}{1}".format(user, initial)
        lines.append("{0:.<{nw}.{nw}} ({1.id:4}) "
                     "{1.username:{uw}}".format(name, user,
                     nw=namewidth, uw=usernamewidth))

    lines_per_page = 64
    lino = 0
    for left, right in zip(lines[::2], lines[1::2]):
        if lino == 0:
            print(header)
        print(left + columngap + right)
        lino += 1
        if lino == lines_per_page:
            print("\f")
            lino = 0
    if lines[-1] != right:
        print(lines[-1])


main()
