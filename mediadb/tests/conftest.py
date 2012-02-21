import pymongo
import datetime
import py.path

from mediadb import MediaDatabase

def pytest_funcarg__db(request):
    """return a database object"""
    conn = pymongo.Connection()
    db = conn.mediadb_testdatabase
    return db

def pytest_funcarg__mediadb(request):
    """return a media database instance"""
    db = request.getfuncargvalue("db")
    coll = db.assets
    return MediaDatabase(coll)

def pytest_funcarg__testimage(request):
    p = py.path.local(request.fspath)
    return p.dirpath().join("assets/logo.png")

