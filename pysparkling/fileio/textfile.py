from __future__ import absolute_import, unicode_literals

import logging
from io import BytesIO, StringIO, TextIOWrapper

from . import codec
from .file import File

log = logging.getLogger(__name__)

# there is no basestring in Python 3, so define string_types:
try:
    string_types = basestring
except NameError:
    string_types = str


class TextFile(File):
    """Derived from :class:`pysparkling.fileio.File`.

    :param file_name:
        Any text file name. Supports the schemes ``http://``, ``s3://`` and
        ``file://``.

    """

    def __init__(self, file_name):
        super(TextFile, self).__init__(file_name)

    def load(self, encoding='utf8', encoding_errors='ignore'):
        """Load the data from a file.

        :param encoding: (optional)
            The character encoding of the file.

        :returns:
            An ``io.StringIO`` instance. Use ``read()`` to get a string.

        """
        if type(self.codec) == codec.Codec and \
           hasattr(self.fs, 'load_text'):
            stream = self.fs.load_text(encoding, encoding_errors)
        else:
            stream = self.fs.load()
            stream = self.codec.decompress(stream)
            stream = TextIOWrapper(stream, encoding, encoding_errors)
        return stream

    def dump(self, stream=None, encoding='utf8', encoding_errors='ignore'):
        """Writes a stream to a file.

        :param stream:
            An ``io.StringIO`` instance. A ``basestring`` is also possible and
            get converted to ``io.StringIO``.

        :param encoding: (optional)
            The character encoding of the file.

        :returns:
            self

        """
        if stream is None:
            stream = StringIO()

        if isinstance(stream, string_types):
            stream = StringIO(stream)

        stream = self.codec.compress(
            BytesIO(stream.read().encode(encoding, encoding_errors))
        )
        self.fs.dump(stream)

        return self
