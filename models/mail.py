from models.mongua import Mongua


class Mail(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('sender_id', int, 0),
        ('receiver_id', int, 0),
        ('read', bool, False),
    ]

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.save()

    def mark_read(self):
        self.read = True
        self.save()
