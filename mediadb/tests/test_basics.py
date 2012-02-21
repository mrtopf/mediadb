import pytest
from mediadb import AssetNotFound

def test_add(mediadb, testimage):

    fp = testimage.open()
    asset = mediadb.add(fp, filename="testimage")
    assert asset.d.content_length==5447
    assert asset.filename==asset.d._id
    assert asset.filename == "testimage"


def test_get(mediadb, testimage):

    # add it
    fp = testimage.open()
    asset = mediadb.add(fp, filename="testimage")
    fn = asset.filename

    # get it again
    asset = mediadb.get(fn)
    data = asset.fp.read()
    assert len(data) == asset.d.content_length


def test_delete(mediadb, testimage):

    # add it
    fp = testimage.open()
    asset = mediadb.add(fp, filename="testimage2")
    fn = asset.filename

    # delete it
    asset = mediadb.remove(fn)

    # try to get it again
    pytest.raises(AssetNotFound, mediadb.get, fn)

    

