class User(object):

    def __init__(idd, username, password,email):
        if " " in username:
            raise ValueError("Username can not have space!")
        if len(password)<5:
            raise ValueError("Password must be longer than 5!")
        if "@" not in mail:
            raise ValueError("Mail must have @!")
            
        User._id = idd
        User._username = username
        User._password = password
        User._email = email

        
    @property
    def id(self):
        return User._id

    @property
    def username(self):
        return User._username

    @property
    def password(self):
        return User._password

    @property
    def email(self):
        return User._email

    def __str__(self):
        return """

        id: {0}
        username: {1}
        password: {2}
        email: {3}

        ----------------

        """.format(User._id,User._username,User._password,User._email)

    
