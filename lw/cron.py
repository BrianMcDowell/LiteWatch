from .crawl import collect
from .mail import send_mail
from .models import Search
from .models import Result
from django.contrib.auth.models import User
# from .models import AbstractUser


def trigger():
    """
    Performs background search and notification functions
    Called from CRONJOBS in settings.py
    """
    users = User.objects.all()
    for u in users:
        username = u.username
        email_address = u.email
        searches = Search.objects.all().filter(user=u.id)

        for s in searches:
            """
            sample data used for hardcode testing
            url = 'https://prodogsdirect.org.uk/category/dogs/'
            search_word = 'Bulldog'
            user = 'brianmcdowell@ufl.edu'
            """
            url = s.url
            search_word = s.keyword
            elem_type = 'div' # change to s.elemtype
            elem_attr = 'entry-summary' # change to s.elemattr
            past_result_table = Result.objects.all().filter(sourceSearch=s)
            past_hits = []
            if past_result_table:
                for pr in past_result_table:
                    past_hits.append((pr.sample, pr.url))

            found_word = collect(url, search_word, elem_type, elem_attr)
            if found_word:
                message_html = ''
                for f in found_word:
                    if f not in past_hits:
                        message_html += '<h3>' + f[0] + '</h3>'
                        link = '<a clicktracking="off" href="' + f[1] + '">'
                        message_html += link + f[1] + '</a>'
                        r = Result(sourceSearch=s, sample=f[0], url=f[1], sent=True)
                        r.save()
                if message_html:
                    success_message = 'Great news {}! We found new results in your search for ' \
                                      '"{}" at {}\n'.format(username, search_word, url)
                    success_message += message_html
                    send_mail(email_address, search_word, success_message)
                    # comment out to reduce emails during testing

# TODO lines 29 and 30 point to search database instead of hardcoded values
# TODO break functionality into reusable code to support calling from other places
