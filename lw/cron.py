from .crawl import collect
from .mail import send_mail
from .models import Search
from .models import Result
from django.contrib.auth.models import User
from .models import AbstractUser


def trigger():

    users = User.objects.all()
    for u in users:
        username = u.username
        email_address = u.email
        searches = Search.objects.all().filter(user=u.id)

        for s in searches:
            # TODO validate this logical progression:
            # 1. query list of users from db
            # 2. iterate through u in users
            #   2a. for u in users query list of Searches where Status = Enabled
            #       and query list of results
            #   3. iterate through s in searches
            #   3a. load s into parameters below and run collect()

            """
            url = 'https://prodogsdirect.org.uk/category/dogs/'
            search_word = 'Bulldog'
            user = 'brianmcdowell@ufl.edu'
            """
            url = s.url
            search_word = s.keyword
            div_id = 'entry-summary'
            past_result_table = Result.objects.all().filter(sourceSearch=s)
            past_hits = []
            if past_result_table:
                for pr in past_result_table:
                    past_hits.append((pr.sample, pr.url))

            found_word = collect(url, search_word, div_id)
            if found_word:
                message_html = ''
                for f in found_word:
                    if f not in past_hits:
                        message_html += f[0] + '\n'
                        message_html += f[1] + '\n'
                        r = Result(sourceSearch=s, sample=f[0], url=f[1], sent=True)
                        r.save()
                if message_html:
                    success_message = 'Great news {}! We found new results in your search for ' \
                                      '"{}" at {}\n'.format(username, search_word, url)
                    success_message += message_html
                    send_mail(email_address, search_word, success_message)
                    # comment out to reduce emails during testing

# TODO include search field type and div_id (or other field id) in user provided values
# TODO break functionality into reusable code to support calling from other places
