#!/usr/bin/python3
"""Unittests for the HBNB command interpreter (create with parameters)."""
import unittest
from os import getenv
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db',
                 "create with parameters is only tested with FileStorage")
class TestConsoleCreate(unittest.TestCase):
    """Test the do_create parameter parsing feature."""

    def _create(self, line):
        """Run a create command and return the printed id."""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd(line)
        return out.getvalue().strip()

    def test_create_missing_class(self):
        """create with no class prints an error."""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("create")
        self.assertEqual(out.getvalue().strip(), "** class name missing **")

    def test_create_invalid_class(self):
        """create with an unknown class prints an error."""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("create DoesNotExist")
        self.assertEqual(out.getvalue().strip(), "** class doesn't exist **")

    def test_create_string_param(self):
        """A string param has underscores replaced by spaces."""
        obj_id = self._create('create State name="My_little_house"')
        obj = storage.all()['State.' + obj_id]
        self.assertEqual(obj.name, "My little house")

    def test_create_escaped_quote(self):
        """An escaped double quote inside a string is kept."""
        obj_id = self._create('create State name="a\\"b"')
        obj = storage.all()['State.' + obj_id]
        self.assertEqual(obj.name, 'a"b')

    def test_create_int_param(self):
        """An integer param is parsed as int."""
        obj_id = self._create('create Place number_rooms=4')
        obj = storage.all()['Place.' + obj_id]
        self.assertEqual(obj.number_rooms, 4)
        self.assertIs(type(obj.number_rooms), int)

    def test_create_float_param(self):
        """A float param is parsed as float."""
        obj_id = self._create('create Place latitude=37.77')
        obj = storage.all()['Place.' + obj_id]
        self.assertEqual(obj.latitude, 37.77)
        self.assertIs(type(obj.latitude), float)

    def test_create_negative_float(self):
        """A negative float param is parsed correctly."""
        obj_id = self._create('create Place longitude=-122.43')
        obj = storage.all()['Place.' + obj_id]
        self.assertEqual(obj.longitude, -122.43)

    def test_create_skips_bad_param(self):
        """A malformed param is skipped, the rest are kept."""
        obj_id = self._create('create State name="ok" badtoken =alsobad')
        obj = storage.all()['State.' + obj_id]
        self.assertEqual(obj.name, "ok")
        self.assertFalse(hasattr(obj, 'badtoken'))

    def test_create_unclosed_string_skipped(self):
        """An unterminated string value is skipped."""
        obj_id = self._create('create State name="oops')
        obj = storage.all()['State.' + obj_id]
        self.assertFalse(hasattr(obj, 'name') and obj.name == 'oops')


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db',
                 "MySQL database checks are only relevant for DBStorage")
class TestConsoleCreateDB(unittest.TestCase):
    """Validate that console commands change the MySQL database state.

    These tests talk to MySQL directly through MySQLdb (not SQLAlchemy)
    so the database state is checked independently of the storage engine.
    """

    def _connect(self):
        """Open a raw MySQLdb connection from the environment."""
        import MySQLdb
        return MySQLdb.connect(
            host=getenv('HBNB_MYSQL_HOST'),
            user=getenv('HBNB_MYSQL_USER'),
            passwd=getenv('HBNB_MYSQL_PWD'),
            db=getenv('HBNB_MYSQL_DB'),
            port=3306)

    def _count(self, table):
        """Return the number of rows in the given table."""
        db = self._connect()
        cur = db.cursor()
        cur.execute("SELECT COUNT(*) FROM {}".format(table))
        count = cur.fetchone()[0]
        cur.close()
        db.close()
        return count

    def test_create_state_adds_record(self):
        """create State adds exactly one row to the states table."""
        before = self._count('states')
        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd('create State name="California"')
        after = self._count('states')
        self.assertEqual(after - before, 1)

    def test_create_user_adds_record(self):
        """create User adds exactly one row to the users table."""
        before = self._count('users')
        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd(
                'create User email="a@b.com" password="pwd"')
        after = self._count('users')
        self.assertEqual(after - before, 1)


if __name__ == "__main__":
    unittest.main()
    