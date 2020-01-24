def User():

    def __init__(self, id, username, password,email):
        self._id = id
        self._username = username
        self._password = password
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def email(self):
        return self._email

    def __str__(self):
        return """

        id: {0}
        username: {1}
        password: {2}
        email: {3}

        ----------------

        """.format(self._id,self._username,self._password,self._email)

    
