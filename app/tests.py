from app.models import Add_user, Donor, Fundraiser, GeneralAdmin, Group, Idea, Message, Response, Stories, Tech, UploadInvite, UserProfile
from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
# test for class Userprofile
class TestUserProfile(TestCase):
    def setUp(self):
        self.user = User(username="mylo", password="mylo123")
        self.user.save()
        self.group= Group(name='test name',description='this is a group',date_created="1/1/1111",creator= self.user, admin=self.user)
        self.group.save()
        self.userprofile = UserProfile(bio='my bio',photo_path='image.jpg', group=self.group, user = self.user)


    def test_instance_true(self):
        self.assertFalse(isinstance(self.userprofile.save, UserProfile))

    def test_save_userprofile(self):
        pp = UserProfile.objects.all()
        self.assertTrue(len(pp) > 0)

# test for class Group
class TestGroup(TestCase):
    def setUp(self):
        self.user = User(username='mylo')
        self.user.save()
        self.group = Group(name='test group',description='this is a group',date_created='1/1/1111', creator= self.user, admin=self.user)
        self.group.save()


    def tearDown(self):
        Group.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.group,Group))

# test for class Message
class TestMessage(TestCase):
    def setUp(self):
        self.user = User(username='mylo')
        self.user.save()
        self.group = Group(name='test group',description='this is a group',date_created='1/1/1111', creator= self.user, admin=self.user)
        self.group.save()
        self.message = Message(title='test',description='this is a message',date_created='1/1/1111',group=self.group,creator=self.user)


    def tearDown(self):
        Message.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.message,Message))
# test for class Response
class TestResponse(TestCase):
    def setUp(self):
        self.user = User(username='mylo')
        self.user.save()
        self.message = Message(title='test',description='this is a message',date_created='1/1/1111',creator=self.user)
        self.message.save()
        self.response = Response(message=self.message,creator=self.user,reply='this is a reply',date_created='1/1/1111')


    def tearDown(self):
        Response.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.response,Response))

    def test_save_response(self):
        pp = Response.objects.all()
        self.assertFalse(len(pp) > 0)

    def test_get_response(self):
        self.response.save_response()

# test for class Stories 
class TestStories(TestCase):
    def setUp(self):
        self.user = User(username='mylo')
        self.user.save()
        self.stories = Stories(title='test',description='this is a story',image_path='image.jpg',date_created='1/1/1111',creator=self.user,link='https://abcd.com')
        self.stories.save()


    def tearDown(self):
        Stories.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.stories,Stories))

    def test_get_stories(self):
        self.stories.save()

# test for class Tech
class TestTech(TestCase):
     def setUp(self):

        self.user = User(username='mylo')
        self.user.save()
        self.tech = Tech(title='test',description='this is tech',image_path='image.jpg',date_created='1/1/1111',creator=self.user,link='https://abcd.com')
        self.tech.save()
    
# test for class Fundraiser
class TestFundraiser(TestCase):
     def setUp(self):
        self.user = User(username='mylo')
        self.user.save()
        self.fundraiser= Fundraiser(title='test',description='this is a fundraiser',image_path='image.jpg',creator=self.user,event_date='2/08/2021',date_created='1/1/1111')
        self.fundraiser.save()
        self.group= Group(name='test name',description='this is a group',date_created="1/1/1111",creator= self.user, admin=self.user)
        self.group.save()
        self.userprofile = UserProfile(bio='my bio',photo_path='image.jpg', group=self.group, user = self.user)

# test for class Donor
class TestDonor(TestCase):
    def setUp(self):
        self.user = User(username='mylo')
        self.user.save()
        self.fundraiser= Fundraiser(title='test',description='this is a fundraiser',image_path='image.jpg',creator=self.user,event_date='2/08/2021',date_created='1/1/1111')
        self.fundraiser.save()
        self.donor= Donor(name='test name',occupation='engineer',pledge='this is my pledge',fundraiser= self.fundraiser, date_created='1/11/1111')
        self.donor.save()

# test for class UploadInvite
class TestUploadInvite(TestCase):
    def setUp(self):
        self.uploadinvite= UploadInvite(file_path='Documents')
        self.uploadinvite.save()

# test for class Add_user
class TestAddUser(TestCase):
    def setUp(self):
        self.adduser= Add_user(full_name='test',username='mylo',student_id='1234567',phone_number='072345678',email='test@gmail.com')
        self.adduser.save()

    

