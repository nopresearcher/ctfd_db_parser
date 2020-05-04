import argparse
import sqlite3

# argument parsing
parser = argparse.ArgumentParser(description="Parse CTFd database for useful information")
parser.add_argument("-v", "--verbose", help="verbose output", action="store_true")
parser.add_argument("-t", "--team", help="used if CTFd is configured for teams instead of users", action="store_true")
parser.add_argument("-e", "--email", help="output email addresses to file", action="store_true")
parser.add_argument('--db', help="CTFd sqlite3 db file", type=argparse.FileType('r'), required=True)
args = parser.parse_args()

# sqlite3 database connection
conn = sqlite3.connect(args.db.name)
c = conn.cursor()

# args testing
if args.verbose:
    print("Verbose: " + str(args.verbose))
    print("Team: " + str(args.team))
    print("CTFd db: " + str(args.db.name))

# CTF Name
c.execute('SELECT value from config where KEY="ctf_name";')
ctfd_name = c.fetchone()
print("CTFd Name: " + ctfd_name[0])


# CTF Version
c.execute('SELECT value from config where KEY="ctf_version";')
ctfd_version = c.fetchone()
print("CTFd Version: " +  ctfd_version[0])


# CTF Version
c.execute('SELECT value from config where KEY="user_mode";')
user_mode = c.fetchone()
print("CTFd Mode: " +  user_mode[0])

# email
if args.email:
    c.execute('select email from users;')
    email_list = c.fetchall()
    f = open('email_list.txt', 'w')
    for email in email_list:
        f.write(email[0]+'\n')
    f.close()
print(args.db.name)

# Score by user
c.execute('select COUNT(user_id), user_id, users.name, SUM(challenges.value) from [solves] JOIN users ON [solves].user_id = users.id LEFT JOIN challenges ON [solves].challenge_id = challenges.id group by user_id order by SUM(challenges.value) DESC;')
users_by_score = c.fetchall()
print("User       Score")
for user in users_by_score:
    print(user[2] + ' ' + str(user[3]))
