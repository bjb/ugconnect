

Website for running User Group Connect event

To make your site:

$ cp secrets.py.template secrets.py

edit it

do not commit it to git - it's for your site's private stuff

$ virtualenv --no-site-packages /usr/local/pythonenv/UGC
$ bash        # this is so you don't lose your terminal when you want to undo the virtualenv
$ source /usr/local/pythonenv/UGC/bin/activate
# chmod +x manage.py   # I don't want to have to type "python" before ./manage.py all the time
# ./manage.py syncdb   # this should ask you to create a superuser
# ./manage.py migrate
# ./manage.py createsuperuser  # if not created yet
# ./manage.py runserver

visit http://localhost:8000/admin

and create more users (for your committee)
Add usergroups and usergroup2s and sponsors (for content)

usergroup has an organization
sponsor has an organization


todo:

At the moment, usergroup logos get uploaded into
the static images directory - not good but that's the
way it works for now.

usergroup2 was invented after usergroup, I should have made
usergroup2 first and then made usergroup on top of it.
Will make that change after the first event is over.


