from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import _mysql


class Command(BaseCommand):
    help = 'Command to create initial database'
    requires_system_checks = False

    def add_argument(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            # your logic here
            self.stdout.write(self.style.SUCCESS('Starting db creation'))

            dbname = settings.DATABASES['default']['NAME']
            user = settings.DATABASES['default']['USER']
            password = settings.DATABASES['default']['PASSWORD']
            host = settings.DATABASES['default']['HOST']

            db = _mysql.connect(host='localhost', user='root')
            self.stdout.write(self.style.SUCCESS('Creating database ' + dbname))
            db.query('CREATE DATABASE ' + dbname + ' CHARACTER SET utf8')
            self.stdout.write(self.style.SUCCESS('database created, \n Creating user'))
            if password:
                db.query("CREATE USER " + "'" + user + "'" + '@' + "'" + host + "'" + ' IDENTIFIED BY ' + "'" + password + "'")
            else:
                db.query("CREATE USER " + "'" + user + "'" + '@' + "'" + host + "'")
            self.stdout.write(self.style.SUCCESS('created user successfully \n granting user permission'))
            db.query("GRANT ALL ON " + dbname + ".*" + " TO " + "'" + user + "'" + '@' "'" + host + "'")
            self.stdout.write(self.style.SUCCESS('Permission granted'))
            db.close()

            self.stdout.write(self.style.SUCCESS('All Done, Mission is a success, i repeat, mission is a success'))

        except Exception as e:
            CommandError(repr(e))
