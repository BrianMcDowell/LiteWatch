from django.test import TestCase
from .models import Search, Result
from django.contrib.auth.models import User
# import cron
# Create your tests here.

#Regex-Based Tests
#Test 1 -- User Valid Input
#This test may involve the use of a regex. It should be simple, as all it has to match is that if the words match any valid character.


#Test 2 -- Website Valid Input
#This test is the same as test 1, but instead it will check the following (to be determined):
#If it has "www." and/or the ".com", ".org"... any valid website extension.

#Test 3 -- Valid Email
#for as long as it has the valid email extension, this should pass

#Databse based tests
#Test 4 -- Email Notification Successful
#This test case tests if the email notifications were successful

#Test 5 -- Account Creation
#It should detect if there is a new account created. It should not pass if there are accounts that are already created.
#Basically, if let's say... if the size increased by 1, then this test should pass.

#Test 6 -- Account Deletion
#The reverse of test 5. If the size of the account list decreased by 1, then this test should pass.

#Test 7- - Duplicate Account Creation
#If someone attempts to create a user with the same email credentials, then... Account creation should FAIL!

#Test 8 -- Duplicate Passwords
#Test if a new user attempts to use a password that has already been use. Account creation should FAIL!

#Test 9 -- No results by typing gibberish on the webcrawler search
#This test should "pass" if there are no generated results if gibberish is typed. It should match for words.

class CreateSearchTest(TestCase):
    """
    Tests that new search is added to database
    """
    def createsearch(self, keyword='Bulldog',
                     url='https://prodogsdirect.org.uk/category/dogs/',
                     user_id=1, state=True):
        User.objects.create(id=1, email="test@test.test", password="password", username="testuser")
        return Search.objects.create(url=url, keyword=keyword, user_id=user_id, state=state)

    def testcreation(self):
        s = self.createsearch()
        self.assertTrue(isinstance(s, Search))


class CreateUserTest(TestCase):
    """
    Tests that new user is added
    """
    def createuser(self, newusername="NewUser",
                   newuseremail="new@user.email",
                   password="password"):
        User.objects.create(username=newusername, email=newuseremail, password=password)
    def testcreation(self):
        self.createuser()
        self.assertTrue(len(User.objects.filter(username="NewUser")) == 1)
        self.assertTrue(User.objects.get(username="NewUser").email == "new@user.email")

class UserToSearchForeignKeysTest(TestCase):
    """
    Tests foreign keys. Search item should reference id of user
    """
    def createuser(self, thisuser="thisuser",
                   thisemail="this@email.com",
                   password="Password"):
        return User.objects.create(username=thisuser, email=thisemail, password=password)

    def createSearch(self, keyword="keyword",
                     url="www.test.com", thisuser="thisuser"):
        return Search.objects.create(keyword=keyword, url=url,
                              user_id=User.objects.get(username=thisuser).id, state=True)

    def testforeignkey(self):
        thisuser = self.createuser()
        thissearch = self.createSearch()
        print(thisuser)
        self.assertTrue(thissearch.user_id == thisuser.id)


class SearchToResultForeignKeyTest(TestCase):
    """
    Tests foreign keys. Result item should reference id of search
    """
    def createuser(self, thisuser="thisuser",
                   thisemail="this@email.com",
                   password="Password"):
        return User.objects.create(username=thisuser, email=thisemail, password=password)

    def createSearch(self, keyword="keyword",
                     url="www.test.com", thisuser="thisuser"):
        return Search.objects.create(keyword=keyword, url=url,
                              user_id=User.objects.get(username=thisuser).id, state=True)

    def createresult(self, sourcesearch, url="www.test.com",
                     sample="Some text", sent=True,
                     ):
        return Result.objects.create(sample=sample, url=url, sent=sent, sourceSearch_id=sourcesearch)

    def testforeignkey(self):
        thisuser = self.createuser()
        thissearch = self.createSearch()
        thisresult = self.createresult(sourcesearch=thissearch.id)
        self.assertTrue(thisresult.sourceSearch_id == thissearch.id)


class CascadingDelete(TestCase):
    """
    Tests whether deleting user data also deletes
    user's searches and results
    """
    def createuser(self, thisuser="thisuser",
                   thisemail="this@email.com",
                   password="Password"):
        return User.objects.create(username=thisuser, email=thisemail, password=password)

    def createSearch(self, keyword="keyword",
                     url="www.test.com", thisuser="thisuser"):
        return Search.objects.create(keyword=keyword, url=url,
                              user_id=User.objects.get(username=thisuser).id, state=True)

    def createresult(self, sourcesearch, url="www.test.com",
                     sample="Some text", sent=True,
                     ):
        return Result.objects.create(sample=sample, url=url, sent=sent, sourceSearch_id=sourcesearch)

    def testdelete(self):
        thisuser = self.createuser()
        thissearch = self.createSearch()
        thisresult = self.createresult(sourcesearch=thissearch.id)
        beforeres = len(Result.objects.all())
        beforesearch = len(Search.objects.all())
        thisuser.delete()
        afterres = len(Result.objects.all())
        aftersearch = len(Search.objects.all())
        self.assertTrue(beforesearch > aftersearch)
        self.assertTrue(beforeres > afterres)
