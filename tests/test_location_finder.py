import os
import sys

TEST_DIR   = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

from lib.factory.finder import FinderFactory

def test_find():
	finder    = FinderFactory.get_finder(FinderFactory.LOCATION)
	locations = finder.find()
	assert len(locations) != 0

def test_find_all():
	finder    = FinderFactory.get_finder(FinderFactory.LOCATION)
	locations = finder.find_all()
	assert len(locations) == 4207
