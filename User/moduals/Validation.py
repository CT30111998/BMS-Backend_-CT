import re

class Validation:
    def nullValid(self, fields):
        notNull = True
        for li in fields:
            if li == "" or li is None:
                notNull = False
                break
        return notNull


    def passValid(self, password):
        check = str(password)
        if len(check) >= 8:
            return True
        else:
            return False


    def emailValid(self, email):
        regex = r"^[a-z0-9]+[\._-]*[a-z0-9]*[@][a-z0-9]+[.][a-z]{1,3}[.]?[a-z]{0,2}$"

        if re.fullmatch(regex, email):
            return True
        else:
            return False


# name = None
# email = "kushmewada@gmail.com"
# email2 = "kushmewadagmail.com"
# email3 = "kushmewada@com"
# email4 = "kushmewada.com"
# email5 = "kushmewada@.com"
#
# print("gmail 1 = ", emailValid(email))
# print("gmail 2 = ", emailValid(email2))
# print("gmail 3 = ", emailValid(email3))
# print("gmail 4 = ", emailValid(email4))
# print("gmail 5 = ", emailValid(email5))
# pas = 123
# fi = [name, pas]
#
# print(nullValid(fi))