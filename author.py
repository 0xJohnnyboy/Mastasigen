class Author:

    def __init__(self, name, mail, phone, github, available_from, available_until, profile_picture=None):
        self.name = name
        self.mail = mail
        self.phone = phone
        self.github = github
        self.available_from = available_from
        self.available_until = available_until
        self.profile_picture = profile_picture

    def get_author(self):
        return [self.name, self.mail, self.phone, self.github, self.available_from, self.available_until,
                self.profile_picture]
