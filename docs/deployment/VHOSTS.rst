Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess openplan-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/openplan/log/apache2/error.log"
        CustomLog "/srv/sites/openplan/log/apache2/access.log" common

        WSGIProcessGroup openplan-<target>

        Alias /media "/srv/sites/openplan/media/"
        Alias /static "/srv/sites/openplan/static/"

        WSGIScriptAlias / "/srv/sites/openplan/src/openplan/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-openplan-<target>]
    user = <user>
    command = /srv/sites/openplan/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/openplan/src/openplan/wsgi/wsgi_<target>.py
    home = /srv/sites/openplan/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/openplan/log/uwsgi_err.log
    stdout_logfile = /srv/sites/openplan/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_openplan_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/openplan/log/nginx-access.log;
      error_log /srv/sites/openplan/log/nginx-error.log;

      location /500.html {
        root /srv/sites/openplan/src/openplan/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/openplan/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/openplan/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_openplan_<target>;
      }
    }
