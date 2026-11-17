from abc import ABC, abstractmethod
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from File import get_file_path, read_file, write_file


class file_exists(ABC):
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)

    def resolve_path(self, filename):
        if filename is None:
            raise ValueError("filename cannot be None")
        if isinstance(filename, Path):
            return filename
        return self.base_dir / str(filename)

    @abstractmethod
    def _check_path(self, path):
        raise NotImplementedError("file_exists subclasses must implement _check_path().")

    def __call__(self, filename):
        return self._check_path(self.resolve_path(filename))


class DefaultFileExists(file_exists):
    def _check_path(self, path):
        return path.exists() and path.is_file()


checker = DefaultFileExists(get_file_path(""))

print(get_file_path("test1"))
print(checker("test1"))

print("test 2: Write to file", get_file_path("test2"))
write_file("test2", "Hello, this is charmaine!")
print("written successfully", checker("test2"))

print("test 3: check if file exists")
print(checker("test3"))

print("test 4: read from file")
try:
    content = read_file("test2")
    print(f"Content of test2: {content}")
except FileNotFoundError as e:
    print(e)