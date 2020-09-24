class Author:
    
    def __init__(self, name, mail, phone, profile_pic = ''):
        self.name = name
        self.mail = mail
        self.phone = phone
        self.profile_pic = profile_pic

    def get_author(self):

        return [self.name, self.mail, self.phone, self.profile_pic]
