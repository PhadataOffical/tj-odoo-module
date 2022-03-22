

#### Usage:

1. Install Ubuntu Server 20.04+

   [Get Ubuntu | Download | Ubuntu](https://ubuntu.com/download)

2. Install Docker-compose && PostgreSQL

   Docker-compose:

   ```shell
   $ sudo apt-get update && sudo apt-get dist-upgrade
   $ sudo apt-get install docker-compose
   ```

   PostgreSQL:

   ```shell
   $ sudo vim docker-compose.xml ## eg. docker-comppose.xml content.
   $ sudo vim odoo_pg_pass ## eg. 123456; database password
   $ sudo docker-compose up -d
   $ sudo docker-compose ps -a ## verify success.
   ```

   eg. *docker-compose.xml*

   ```dockerfile
   version: '3.1'
   services:
     db:
       image: postgres:13
       ports:
         - "5432:5432"
       environment:
         - POSTGRES_DB=postgres
         - POSTGRES_PASSWORD_FILE=/run/secrets/postgresql_password
         - POSTGRES_USER=odoo
         - PGDATA=/var/lib/postgresql/data/pgdata
       volumes:
         - odoo-db-data:/var/lib/postgresql/data/pgdata
       secrets:
         - postgresql_password
   volumes:
     odoo-db-data:
   
   secrets:
     postgresql_password:
       file: odoo_pg_pass
   ```

   

3. Install Odoo14.0

   If `Python 3` is already installed, make sure that the version is `3.6` or above, as previous versions are not compatible with Odoo.

   ```shell
   $ python3 --version
   ```

   `Verify` also that [pip](https://pip.pypa.io/) is installed for this version.

   ```shell
   $ pip3 --version
   ```

   `Install virtualenv`

   ```shell
   $ sudo apt-get install virtualenv
   ```

   `Download/Git Odoo14`

   ```shell
   $ git clone -b 14.0 https://github.com/odoo/odoo.git
   ```

   `Dependencies`

   For libraries using native code, it is necessary to install development tools and native dependencies before the Python dependencies of Odoo. They are available in `-dev` or `-devel` packages for Python, PostgreSQL, libxml2, libxslt1, libevent, libsasl2 and libldap2.

   On Debian/Unbuntu, the following command should install all the required libraries:

   ```shell
   $ sudo apt install python3-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
       libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev libfreetype6-dev \
       liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev libpq-dev
   ```

   `Insatll`

   ```shell
   $ cp ${odoo_baseDir}/tj-odoo-module/requirements.txt ${odoo_baseDir}
   $ cd ${odoo_baseDir}
   $ virtualenv venv
   $ source venv/bin/activate
   $ pip3 install -r requirements.txt
   ```

   `Set Odoo.conf`

   ```shell
   $ cd ${odoo_baseDir}
   $ vim odoo.conf
   [options]
   admin_passwd = 123456
   db_host = 192.168.0.6
   db_port = 5432
   db_user = odoo
   ; db_name = odoo14
   db_password = 123@abcd
   addons_path = addons,odoo/addons,tj-odoo-module
   ```

   `Running Odoo`

   ```shell
   (venv)$ python3 odoo-bin -c odoo.conf --dev=xml
   ...
   ```

   

#### Notes

[Odoo Documentation — Odoo 14.0 documentation](https://www.odoo.com/documentation/14.0/)

