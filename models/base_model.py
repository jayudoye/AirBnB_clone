#!/usr/bin/python3
"""
This is an abstraction class to be inherited by other classes of the project
"""
from . import storage
import uuid
from datetime import datetime


class BaseModel:
    """
    Defines all common attributes/methods for other classes
    """

    def __init__(self, *args, **kwargs):
        """Initialization"""
        if len(kwargs) != 0:
            forbidden_keys = ['__class__']
            datetime_keys = ['created_at', 'updated_at']
            for k, v in kwargs.items():
                if k in forbidden_keys:
                    continue
                if k in datetime_keys:
                    # convert to datetime object
                    v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
                setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            now = datetime.now()
            self.created_at = now
            self.updated_at = now
            storage.new(self)

    def __str__(self):
        """Returns the string representation of an instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """updates the public instance attribute updated_
        at with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of an object"""
        res = self.__dict__.copy()
        res['__class__'] = self.__class__.__name__
        res['created_at'] = self.created_at.isoformat()
        res['updated_at'] = self.updated_at.isoformat()
        return res
