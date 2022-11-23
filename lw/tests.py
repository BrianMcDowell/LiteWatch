from django.test import TestCase
import cron
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

