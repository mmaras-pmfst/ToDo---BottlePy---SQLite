class Todo():

    def __init__(self,id,user_id,title,desc,datetime,datetime_complete):
        self._id=id
        self._user_id=user_id
        self._title=title
        self._desc=desc
        self._datetime=datetime
        self._datetime_complete=datetime_complete

    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id

    @property
    def title(self):
        return self._title

    @property
    def desc(self):
        return self._desc

    @property
    def datetime(self):
        return self._datetime

    @property
    def datetime_complete(self):
        return self._datetime_complete

    def __str__(self):
        return """
        id: {0}
        user_id: {1}
        title: {2}
        desc: {3}
        datetime: {4}
        datetime_complete: {5}

        ------------------------
        """.format(self._id,self._user_id,self._title,self._desc,self._datetime,self._datetime_complete)
    
