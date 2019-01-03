from typing import List, Optional


class Payload:

    def __init__(self,
                 binary: str,
                 arguments: Optional[List[str]] = None) -> None:

        self._binary = binary
        self._arguments = arguments or []

    @property
    def command(self) -> str:
        command_list = [self._binary] + self._arguments
        return ' '.join(command_list)


class Script(Payload):

    def __init__(self, binary: str, path: str) -> None:
        super().__init__(binary, [path])


class Source(Payload):

    def __init__(self, binary: str, code: str, encoding: str = "utf-8") -> None:
        super().__init__(binary)

        self._code = code
        self._encoding = encoding

    @property
    def code(self) -> str:
        return self._code

    @property
    def command(self) -> str:
        raise RuntimeError("Unable to provide a run command for source code")

    def save(self, host_path: str, container_path: str) -> Script:
        with open(host_path, "wb") as script_file:
            script_file.write(bytearray(self._code, self._encoding))
        return Script(self._binary, container_path)


class PythonSource(Source):

    DEFAULT_BINARY: str = "/usr/bin/python3"

    def __init__(self, code: str) -> None:
        super().__init__(self.DEFAULT_BINARY, code)
