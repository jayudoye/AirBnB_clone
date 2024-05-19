#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    __commands = {
        'all': r'^\.all(\(\))$',
        'count': r'^\.count(\(\))$',
        'show': r'^\.show(\(.*?\))$',
        'destroy': r'^\.destroy(\(.*?\))$',
        'update': r'^\.update(\(.*?\))$',
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        return True

    def _split(self, arg):
        """Split the line in to substrings based on double quotes and spaces"""
        pattern = r'("[^"]+"|\{[^}]*\}|\S+)'
        res = re.findall(pattern, arg)
        for i in range(len(res)):
            try:
                v = eval(res[i])
                if type(v) in (int, str, float, dict):
                    res[i] = v
            except (NameError, SyntaxError, TypeError):
                continue
        return res

    def do_create(self, arg):
        """Creates an instance of the passed class if it exists,
        saves it and prints its id"""
        arg = self._split(arg)
        if not arg:
            return print("** class name missing **")
        klas = arg[0]
        if klas not in self.__classes:
            return print("** class doesn't exist **")
        obj = eval(klas)()
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """prints the string representation of an instance"""
        arg = self._split(arg)
        if not arg:
            return print("** class name missing **")
        if arg[0] not in self.__classes:
            return print("** class doesn't exist **")
        if len(arg) < 2:
            return print("** instance id missing **")
        key = "{}.{}".format(arg[0], arg[1])
        instance = storage.all().get(key)
        if not instance:
            return print("** no instance found **")
        print(instance)

    def do_destroy(self, arg):
        """deletes an instance given a classname and instance id"""
        arg = self._split(arg)
        if not arg:
            return print("** class name missing **")
        if arg[0] not in self.__classes:
            return print("** class doesn't exist **")
        if len(arg) < 2:
            return print("** instance id missing **")
        key = "{}.{}".format(arg[0], arg[1])
        instance = storage.all().get(key)
        if not instance:
            return print("** no instance found **")
        del instance
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """prints all instances of a given model"""
        arg = self._split(arg)
        if not arg:
            return print([str(instance) for k, instance in
                          storage.all().items()])
        klas = arg[0]
        if klas not in self.__classes:
            return print("** class doesn't exist **")
        instances = [str(instance) for k, instance in storage.all().items() if
                     k.startswith("{}.".format(klas))]
        print(instances)

    def do_count(self, arg):
        """Count instances based on className"""
        args = self._split(arg)
        klas = args[0]
        match = list(filter(lambda k: k.startswith('{}.'.format(klas)),
                            storage.all().keys()))
        print(len(match))

    def _eval(self, value):
        """Adds double quotes to a string"""
        if type(value) is str:
            return '"{}"'.format(value)
        return str(value)

    def do_update(self, arg):
        """updates a model instance"""
        arg = self._split(arg)
        if not arg:
            return print("** class name missing **")
        if arg[0] not in self.__classes:
            return print("** class doesn't exist **")
        if len(arg) < 2:
            return print("** instance id missing **")
        key = "{}.{}".format(arg[0], arg[1])
        instance = storage.all().get(key)
        if not instance:
            return print("** no instance found **")
        if len(arg) < 3:
            return print("** attribute name missing **")
        kw = {}
        if type(arg[2]) is dict:
            kw = arg[2]
        if not kw and len(arg) < 4:
            return print("** value missing **")
        if not kw:
            kw = {arg[2]: arg[3]}
        for k, v in kw.items():
            setattr(instance, k, v)
        instance.save()

    def parse_line(self, line, klas):
        """parse the input string"""

        command = line[len(klas):]
        for c in self.__commands.keys():
            match = re.match(self.__commands[c], command)
            if match:
                args = eval(match.group(1))
                if not args:
                    return "{} {}".format(c, klas)
                if type(args) is not tuple:
                    args = [args]
                args = " ".join([self._eval(arg) for arg in args])
                return "{} {} {}".format(c, klas, args)
        return line

    def onecmd(self, line):
        """Override to handle advanced commands"""
        if line in ['all', '.all()']:
            return self.do_all("")
        pattern = r"([a-zA-Z]*)\.(all|count|show|destroy|update)"
        match = re.search(pattern, line)
        if match:
            klas = match.group(1)
            if not klas:
                return print("** class name missing **")
            elif klas not in self.__classes:
                return print("** class doesn't exist **")
            line = self.parse_line(line, klas)
        return super(HBNBCommand, self).onecmd(line)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
