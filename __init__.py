"""
Lazy BSON reader.
"""

import bson
import struct

S_INT32 = 4
ZERO = bson.ZERO

def load(fh, as_class=dict,
              tz_aware=True, uuid_subtype=bson.OLD_UUID_SUBTYPE):
    """Decode BSON data to multiple documents.

    `fh` must be a file-like object of concatenated, valid, 
    BSON-encoded documents.

    :Parameters:
      - `fh`: a file-like object supporting ``.read()``
      - `as_class` (optional): the class to use for the resulting
        documents
      - `tz_aware` (optional): if ``True``, return timezone-aware
        :class:`~datetime.datetime` instances
    """
    while True:
        obj_size = fh.read(S_INT32)
        if len(obj_size) == 0:
            return
        
        obj_size = struct.unpack("<i", obj_size)[0]
        data = fh.read(obj_size - S_INT32)

        if len(data) + S_INT32 < obj_size:
            raise bson.InvalidBSON("objsize too large")
        #if bytes(data[-1]) != ZERO:
        #    raise bson.InvalidBSON("bad eoo")
        if data[-1] != 0:
            raise bson.InvalidBSON("bad eoo")
        
        elements = data[:-1]
        yield bson._elements_to_dict(elements, as_class, tz_aware, uuid_subtype)

def jump(fh, number):
    index = 0
    while index < number:
        index = index + 1
        obj_size = fh.read(S_INT32)
        if len(obj_size) == 0:
            print("\""fh.name + "\" has reached its end, stop jumping." + " index = " + str(index))
            return False

        obj_size = struct.unpack("<i", obj_size)[0]
        fh.read(obj_size - S_INT32)
    return True

