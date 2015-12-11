class TipProvv:
    def __init__(self, id, user_email, prof_course, _teaching, _comprehension, _availability, _participation, _material, _books, _attending, _difficulty, _time, _result_rapidity, note):
        self.id = id
        self.user_email=user_email
        self.prof_course = prof_course
        self._teaching = _teaching
        self._comprehension = _comprehension
        self._availability = _availability
        self._participation = _participation
        self._material = _material
        self._books = _books
        self._attending = _attending
        self._difficulty = _difficulty
        self._time = _time
        self._result_rapidity = _result_rapidity
        self.note=note

    def get_info(self):
        info = {'id': self.id, 'user_email': self.user_email, '_teaching': self._teaching, '_comprehension': self._comprehension,
            '_availability': self._availability, '_participation': self._participation, '_material': self._material, '_books': self._books,
            '_attending': self._attending, '_difficulty': self._difficulty, '_time': self._time, '_result_rapidity': self._result_rapidity, 'note': self.note}
        return info