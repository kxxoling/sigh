What a sigh day!
================

I made this site just for fun and sigh based on Flask and its extensions
and many other open sourced projects with ❤️!

Open source
-----------

This site is open sourced as an open source project under GPL v3
license. You can use and modify it for any purpose and free.

Start
-----

Install dependencies
~~~~~~~~~~~~~~~~~~~~

You can install all the Python dependencies by running as pip is
installed::

    pip install -r requirements.txt

Initiate you database
~~~~~~~~~~~~~~~~~~~~~

You can initiate the database by running::

    ./manage.py db upgrade

Run it
~~~~~~

A web site should be served on port 5000 after running
``./manage.py manage.py runserver``, execute
``open http://localhost:5000`` to see what you've got!

Or you can deploy it with WSGI servers like gunicorn by::

    gunicorn wsgi:application

