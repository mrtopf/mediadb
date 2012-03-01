import shutil
import uuid
import os
from mongoquery import AttributeMapper

class FilesystemStore(object):
    """a filesystem storage"""

    def __init__(self, base_path="/tmp"):
        """initialize the filestore
        
        :param base_path: The path under which the files are supposed to be stored

        TODO:
        - check file existence
        - add path generation e.g. via date and time
        
        """
        self.base_path = base_path

    def add(self, fp, filename = None, **kw):
        """add a new file to the store

        :param fp: the file pointer to the file to be stored
        :param filename: An optional filename. If not given, a filename will be generated
        :param kw: optional keyword arguments (ignored by this storage)
        :return: A dictionary containing ``filename``, the filesystem ``path`` and the ``content_length``
        """
        if filename is None:
            filename = unicode(uuid.uuid4())

        path = os.path.join(self.base_path, filename)
        dirpath = os.path.split(path)[0]
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        dest_fp = open(path, "wb")
        shutil.copyfileobj(fp, dest_fp)
        dest_fp.close()

        content_length = os.path.getsize(path)

        return AttributeMapper(
            filename = filename, 
            path = path,
            content_length = content_length
        )

    def get(self, filename):
        """return a file based on the filename"""
        path = os.path.join(self.base_path, filename)
        return open(path, "rb")

    def remove(self, filename):
        """remove a file"""
        path = os.path.join(self.base_path, filename)
        os.remove(path) 

