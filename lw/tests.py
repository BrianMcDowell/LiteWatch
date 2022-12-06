from django.test import TestCase
from .models import Search, Result
from django.contrib.auth.models import User


def create_single_user_search_result():
    """
    Creates items for single user,
    including search and results
    """
    user = User.objects.create(email="test@email.com", username='testuser', password="password")

    search = [
        Search.objects.create(keyword='testkeyword', url='www.test.com', user_id=user.id),
        Search.objects.create(keyword='secondtestkeyword', url='www.secondtest.org', user_id=user.id)
    ]
    result = [
        Result.objects.create(sample='testkeyword plus', url='www.test.com/blah', sourceSearch_id=search[0].id),
        Result.objects.create(sample='secondtestkeyword and', url='www.secondtest.org', sourceSearch_id=search[1].id)
    ]
    return [user, search, result]


def create_multiple_user_search_result():
    """
    Creates multiple users
    each with searches and results
    """
    user = [
        User.objects.create(
            email="test@email.com",
            username='testuser',
            password="password"
        ),
        User.objects.create(
            email="anothertest@email.gov",
            username="seconduser",
            password="password2"
        )
    ]
    search = [
        Search.objects.create(
            keyword='testkeyword',
            url='www.test.com',
            user_id=user[0].id
        ),
        Search.objects.create(
            keyword='secondtestkeyword',
            url='www.secondtest.org',
            user_id=user[1].id)
    ]
    result = [
        Result.objects.create(
            sample='testkeyword plus',
            url='www.test.com/blah',
            sourceSearch_id=search[0].id),
        Result.objects.create(
            sample='secondtestkeyword and',
            url='www.secondtest.org',
            sourceSearch_id=search[1].id)
    ]
    return [user, search, result]


class CreateSearchTest(TestCase):
    """
    Tests that new search is
    added to database
    """

    @staticmethod
    def createsearch(
            keyword='Bulldog',
            url='https://prodogsdirect.org.uk/category/dogs/',
            user_id=1, state=True):
        """Create search"""
        User.objects.create(
            id=1,
            email="test@test.test",
            password="password",
            username="testuser"
        )
        return Search.objects.create(
            url=url,
            keyword=keyword,
            user_id=user_id,
            state=state)

    def testcreation(self):
        """TEst search creation"""
        s = self.createsearch()
        self.assertTrue(isinstance(s, Search))


class CreateUserTest(TestCase):
    """Tests that new user is added"""

    @staticmethod
    def createuser(
                   newusername="NewUser",
                   newuseremail="new@user.email",
                   password="password"):
        """Create user"""
        return User.objects.create(
            username=newusername,
            email=newuseremail,
            password=password
        )

    def testcreation(self):
        """Test user creation"""
        u = self.createuser()
        self.assertTrue(isinstance(u, User))
        self.assertTrue(len(User.objects.filter(username="NewUser")) == 1)
        self.assertTrue(User.objects.get(
            username="NewUser").email == "new@user.email")


class UserToSearchForeignKeysTest(TestCase):
    """
    Tests foreign keys.
    Search item should reference id of user
    """

    @staticmethod
    def createuser(thisuser="thisuser",
                   thisemail="this@email.com",
                   password="Password"):
        """Create user"""
        return User.objects.create(
            username=thisuser,
            email=thisemail,
            password=password
        )

    @staticmethod
    def createSearch(keyword="keyword",
                     url="www.test.com", thisuser="thisuser"):
        """Create search"""
        return Search.objects.create(
            keyword=keyword,
            url=url,
            user_id=User.objects.get(username=thisuser).id,
            state=True
        )

    def testforeignkey(self):
        """Tests for matching foreign key"""
        thisuser = self.createuser()
        thissearch = self.createSearch()
        self.assertTrue(thissearch.user_id == thisuser.id)


class SearchToResultForeignKeyTest(TestCase):
    """
    Tests foreign keys.
    Result item should reference id of search
    """

    @staticmethod
    def createuser(
                   thisuser="thisuser",
                   thisemail="this@email.com",
                   password="Password"):
        """Create user"""
        return User.objects.create(
            username=thisuser,
            email=thisemail,
            password=password
        )

    @staticmethod
    def createSearch(
            keyword="keyword",
            url="www.test.com",
            thisuser="thisuser"):
        """Create search"""
        return Search.objects.create(
            keyword=keyword,
            url=url,
            user_id=User.objects.get(username=thisuser).id,
            state=True
        )

    @staticmethod
    def createresult(sourcesearch,
                     url="www.test.com",
                     sample="Some text",
                     sent=True,
                     ):
        """Create result"""
        return Result.objects.create(
            sample=sample,
            url=url,
            sent=sent,
            sourceSearch_id=sourcesearch
        )

    def testforeignkey(self):
        """Tests for matching foreign keys"""
        thisuser = self.createuser()
        thissearch = self.createSearch()
        thisresult = self.createresult(sourcesearch=thissearch.id)
        self.assertTrue(thisresult.sourceSearch_id == thissearch.id)


class CascadingDelete(TestCase):
    """
    Tests whether deleting user data also deletes
    user's searches and results
    """

    @staticmethod
    def createuser(thisuser="thisuser",
                   thisemail="this@email.com",
                   password="Password"):
        """Create user"""
        return User.objects.create(
            username=thisuser,
            email=thisemail,
            password=password
        )

    @staticmethod
    def createSearch(keyword="keyword",
                     url="www.test.com", thisuser="thisuser"):
        """Create search"""
        return Search.objects.create(
            keyword=keyword,
            url=url,
            user_id=User.objects.get(username=thisuser).id,
            state=True
        )

    @staticmethod
    def createresult(sourcesearch, url="www.test.com",
                     sample="Some text", sent=True,
                     ):
        """create result"""
        return Result.objects.create(
            sample=sample,
            url=url,
            sent=sent,
            sourceSearch_id=sourcesearch
        )

    def testdelete(self):
        """Test deleting search"""
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
