from django.test import TestCase, Client
from django.db import models

from django.contrib.auth.models import User
from .models import Profile, Fill_Out_Sheet, Message
from django.conf import settings
import stripe

class UserTestCase(TestCase):
    def test_stupid(self):
          self.assertEqual(1,1)
    def setUp(self):
        User.objects.create(email='example@example.com', first_name = 'Emma', last_name = 'Studtmann')

    def test_UserExists_Test(self):
        self.assertNotEquals(User.objects.get(email='example@example.com'), None)
    
    def test_profile(self):
        my_user = User.objects.get(email='example@example.com')
        my_profile = Profile.objects.get(user=my_user) #This will just return the one user's profile
        #profile = Profile.objects.filter(bio='Tutor me') This will return a list of all of the profiles which have this bio
        #profile = Profile.objects.filter(bio='Tutor me').filter(location = 'Roanoke') This will return a list of all of the profiles which have this bio
        self.assertNotEquals(my_profile, None)


class MessageTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='row@row.com', first_name = 'Rowan', last_name = 'Dakota', username='row')
        User.objects.create(email='foo@foo.com', first_name = 'Foo', last_name = 'Bar', username='foo')
        User.objects.create(email='poo@poo.com', first_name = 'Poo', last_name = 'Poo', username='poo')

    def test_Message(self):

         foo = User.objects.get(email='foo@foo.com')
         row = User.objects.get(email='row@row.com')
         poo = User.objects.get(email='poo@poo.com')

         msg = Message(
                 sender = foo,
                 receiver = row,
                 msg_content = "What's up my hommie g dog?",
         )

         msg.save()
         re_msg = Message.objects.get(msg_content="What's up my hommie g dog?")
         self.assertEqual(re_msg.sender, foo)
         self.assertEqual(re_msg.receiver, row)
         self.assertNotEquals(re_msg.sender, poo)
         self.assertNotEquals(re_msg.sender, None)


class requestTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='row@row.com', first_name = 'Rowan', last_name = 'Dakota', username='row')
        User.objects.create(email='foo@foo.com', first_name = 'Foo', last_name = 'Bar', username='foo')
        User.objects.create(email='poo@poo.com', first_name = 'Poo', last_name = 'Poo', username='poo')

    def test_Request(self):
        foo = User.objects.get(email='foo@foo.com')
        row = User.objects.get(email='row@row.com')
        poo = User.objects.get(email='poo@poo.com')

        sheet = Fill_Out_Sheet
        sheet.sender = foo
        sheet.receiver = row 
        class_desc = 'Class 1'
        help_desc = 'Exam 1'
        sheet.no_response = False
        sheet.has_tutor_accepted = True
        sheet.has_tutor_rejected = False    

        self.assertEquals(sheet.sender, foo)
        self.assertEquals(sheet.receiver, row)
        self.assertNotEquals(sheet.has_tutor_accepted, False)
        self.assertNotEquals(sheet.has_tutor_rejected, True)

class paymentTestCase(TestCase):
    def test_Payment(self):
        #Test 1 (Attempts to make a sample "charge" call to Stripe API)
        chargeSuccess = None

        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            charge = stripe.Charge.create(
                amount=2000,
                currency='usd',
                description='A Django Test Charge',
                source="tok_visa",
            )
            chargeSuccess = True;
        except:
            chargeSuccess = False;
        
        self.assertEquals(chargeSuccess, True)

        #Test 2 (Attempts to "capture the request - should throw exception")
        try:
            stripe.Charge.capture(charge.id)
            self.fail("No error was thrown (when it should have)")
        except:
            pass #passes if error is thrown