def run(dict):
    print("הזן סיסמה בעלת 6 תווים לפחות")
    newPassword = input()

    while len(newPassword) < 6:
        print("הזן סיסמה בעלת 6 תווים לפחות")
        newPassword = input()

    ''' TODO: save pass somewhere '''
    print(newPassword)
