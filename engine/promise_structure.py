import pathlib
import json
import logging

logger = logging.getLogger(__name__)


class BasicOperator:

    entity_path: pathlib.Path

    def __init__(self, path):
        if type(path) == str:
            self.entity_path = pathlib.Path.cwd() / path
        else:
            self.entity_path = path
        logger.info(f"Created file path {self.entity_path}")

    def is_exists(self):
        return self.entity_path.exists()

    def create(self):
        if not self.entity_path.parent.exists():
            operator = BasicOperator(self.entity_path.parent)
            operator.resolve_as_folder()
        self.create_entity()

    def resolve_as_folder(self):
        if not self.entity_path.parent.exists():
            operator = BasicOperator(self.entity_path.parent)
            operator.resolve_as_folder()
        self.entity_path.mkdir()

    def create_entity(self):
        self.entity_path.touch()


class SourceCodeOperator(BasicOperator):
    err_text = "Source file couldn't be created automatically"

    def create_entity(self):
        raise FileNotFoundError(self.err_text)


class PythonScriptOperator(SourceCodeOperator):
    err_text = "Python script cant be crated automatically "

    def create_entity(self):
        raise FileNotFoundError(self.err_text + self.entity_path.__str__())


class FolderOperator(BasicOperator):
    def create_entity(self):
        logger.error(f"Created folder path {self.entity_path}")
        self.entity_path.mkdir()


class JSONOperator(BasicOperator):
    def create_entity(self):
        with self.entity_path.open('w+') as json_file:
            json.dump({}, json_file)


class ProcfileOperator(BasicOperator):
    def create_entity(self):
        with self.entity_path.open('w') as f:
            f.write("python-10.0.1")


def promise_structure(structure: dict):
    formats = {
        "folder": FolderOperator,
        "json": JSONOperator,
        "procfile": ProcfileOperator,
        "python script": PythonScriptOperator,
        "": BasicOperator
    }

    for path in structure.keys():
        entity_format = formats.setdefault(structure[path], BasicOperator)
        entity_operator = entity_format(path)
        if not entity_operator.is_exists():
            entity_operator.create()
    pass
