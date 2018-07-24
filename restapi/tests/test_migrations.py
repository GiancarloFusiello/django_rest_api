from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test.testcases import TransactionTestCase


class MigrationTestCase(TransactionTestCase):

    # These must be defined by subclasses.
    migrate_from = None
    migrate_to = None

    def setUp(self):
        super(MigrationTestCase, self).setUp()

        self.executor = MigrationExecutor(connection)
        self.executor.migrate(self.migrate_from)

    def migrate_to_dest(self):
        self.executor.loader.build_graph()  # reload.
        self.executor.migrate(self.migrate_to)

    @property
    def old_apps(self):
        return self.executor.loader.project_state(self.migrate_from).apps

    @property
    def new_apps(self):
        return self.executor.loader.project_state(self.migrate_to).apps


class TestMigration0002(MigrationTestCase):

    migrate_from = [('restapi', "0001_initial")]
    migrate_to = [('restapi', "0002_load_seed_data")]

    def test_migration_0002(self):
        # Test migrating forward
        Creator = self.old_apps.get_model('restapi', "Creator")
        creators = Creator.objects.all()
        self.assertEquals(len(creators), 0)

        Prezi = self.old_apps.get_model('restapi', "Prezi")
        prezis = Prezi.objects.all()
        self.assertEquals(len(prezis), 0)

        self.migrate_to_dest()

        Creator = self.old_apps.get_model('restapi', "Creator")
        creators = Creator.objects.all()
        self.assertEquals(len(creators), 7000)

        Prezi = self.old_apps.get_model('restapi', "Prezi")
        prezis = Prezi.objects.all()
        self.assertEquals(len(prezis), 7000)

        # Test migrating backward
        self.migrate_from = [('restapi', "0002_load_seed_data")]
        self.migrate_to = [('restapi', "0001_initial")]

        self.migrate_to_dest()

        Creator = self.old_apps.get_model('restapi', "Creator")
        creators = Creator.objects.all()
        self.assertEquals(len(creators), 0)

        Prezi = self.old_apps.get_model('restapi', "Prezi")
        prezis = Prezi.objects.all()
        self.assertEquals(len(prezis), 0)