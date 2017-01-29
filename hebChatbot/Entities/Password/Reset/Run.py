import os, random, string

def run(dict):
    print("מיד תקבל סיסמה חדשה")
    length = 13
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))

    newPassword = ''.join(random.choice(chars) for i in range(length))

    print(newPassword)
