from models.mongua import Mongua

Model = Mongua


class Reply(Model):
    __fields__ = Mongua.__fields__ + [
        ('content', str, ''),
        ('topic_id', int, 0),
        ('user_id', int, 0),
    ]

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u
