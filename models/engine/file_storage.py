#!/usr/bin/python3
"""Defines the FileStorage class."""
import json


class FileStorage:
    """Class that serializes instances to a JSON file 
    and deserializes JSON file to instances.

    Attributes:
        __file_path (str):  string - path to the JSON file (ex: file.json)
        __objects (dict): dictionary - empty but will store all objects by
        class.
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        data = {k: obj.to_dict() for k, obj in
                self.__objects.items()}
        with open(self.__file_path, "w") as f:
            json.dump(data, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        try:
            with open(self.__file_path) as f:
                data = f.read()
                if not data:  # empty file
                    return
                obj_dict = json.loads(data)
                for o in obj_dict.values():
                    cls_name = o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
