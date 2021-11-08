from django.test import TransactionTestCase
from datetime import date
from reports.models import User

# A class containing all of our User Model tests
class UserTestModels(TransactionTestCase):

    @classmethod
    def setUpClass(self):
        self.user = User.objects.create(
            username = 'Bob',
            email = 'bob@example.co.uk',
            birth_date = date(1982, 4, 10),
            is_active = False,
            reports = 0,
        )

    def test_user_serialize(self):
        self.assertEqual(self.user.serialize(), {
            'id': 1,
            'username': self.user.username,
            'email': self.user.email,
            'birth date': 'Apr 10 1982',
            'is_active': self.user.is_active,
            'reports': self.user.reports,
        })

    def test_user__str__(self):
        self.assertEqual(self.user.__str__(), 'bob@example.co.uk')
