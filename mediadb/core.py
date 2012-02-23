import uuid
import copy
import colander
import mongoquery.onrm as onrm

from stores import FilesystemStore # default store

__all__ = ['AssetNotFound', 'MediaDatabase', 'Asset', 'AssetSchema']

class AssetNotFound(Exception):
    """raised if an asset was not found"""

class AssetSchema(colander.MappingSchema):
    # filename is _id
    content_length = colander.SchemaNode(colander.Integer())
    content_type = colander.SchemaNode(colander.String())
    metadata = colander.SchemaNode(onrm.AnyData(), missing={})

class Asset(onrm.Record):
    """an asset to be stored in the media database"""

    schema = AssetSchema()

    @property
    def filename(self):
        """return the filename"""
        return self.d._id

    @property
    def fp(self):
        """return the file pointer to the uploaded file"""
        return self.collection.store.get(self.filename)


class MediaDatabase(onrm.Collection):
    """the media database"""

    data_class = Asset

    def __init__(self, collection, config={}): 
        """initialize the media database with the collection to use and a config dictionary.

        :param collection: The MongoDB collection object to be used to store asset data
        :param config: A dictionary containing configuration for the Media Database
        """

        # initialize collection
        super(MediaDatabase, self).__init__(collection, config)

        # initialize media database
        self.store = config.get('store', FilesystemStore())
        self.converters = config.get('converters', [])

    def add(self, 
        fp,
        filename = None,
        content_length = None,
        content_type = "application/octet-stream",
        store_kw = {},
        converter_kw = {},
        metadata = {},
        **kw):
        """add a file to the media database

        :param fp: The file pointer of the file to add, should be seeked to 0
        :param content_length: The size of the file to add (optional, will be computed otherwise)
        :param content_type: The media type of the file to add (optional)
        :param store_kw: optional parameters to be passed to the store
        :param converter_kw: optional parameters to be passed to the converters
        :param **kw: additional parameters stored alongside the file
        :return: A dictionary containing the final filename, content length and type
        """

        if filename is None:
            filename = unicode(uuid.uuid4())

        # store filepointer via store
        res = self.store.add(fp, filename=filename)
        
        # TODO: add metadata
        asset = self.data_class(dict(
            _id = res.filename, 
            content_type = content_type, 
            content_length = res.content_length,
            metadata = metadata,
            **kw))

        # store in database
        self.put(asset)

        return asset

    def get(self, filename):
        """retrieve an asset from the media database based on it's filename.

        This will not directly return the file though, only a pointer to it.

        :param filename: The filename of the asset to retrieve
        :return: An instance of ``Asset``.

        If the filename cannot be found it will raise an ``AssetNotFound`` exception.
        
        """

        try:
            asset = super(MediaDatabase, self).get(filename)
        except onrm.ObjectNotFound, e:
            raise AssetNotFound()
        return asset

    def remove(self, filename):
        """remove an asset

        :param fn: The filename of the asset to remove
        
        """
        self.store.remove(filename)
        self.delete(filename)







        


