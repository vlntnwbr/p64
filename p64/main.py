"""Application and entrypoint for p64."""

import argparse
import base64
import subprocess
import sys


class ApplicationError(BaseException):
    """Non fatal exception to be caught in entrypoint."""


class Application:  # pylint: disable=too-few-public-methods
    """Application object."""

    def __init__(self, level: int, is_url: bool):
        self.level = level
        self.is_url = is_url
        self.error = None

    def run(self, content: str) -> None:
        """Run the Application once."""

        decoded = self._decode(content)

        if self.error is not None:
            self._log("error", str(self.error))
            raise ApplicationError(self.error)

        if self.is_url:
            self._open(decoded)
            self._log("opening", decoded)
        else:
            self._log("result", decoded)

    def _decode(self, content: str) -> str:
        """Return base64 'content' decoded 'level' times."""
        try:
            res = content.encode("utf-8")
            for i in range(self.level):  # pylint: disable=unused-variable
                res = base64.b64decode(res)
            return res.decode("utf-8")
        except:  # pylint: disable=bare-except
            self.error = f"Could not decode '{content}'"

    def _log(self, cat: str, msg: str) -> None:  # pylint: disable=no-self-use
        """Print message with category (9 chars max)."""
        print("{:10}{}".format(cat.upper(), msg))

    def _open(self, url: str) -> None:  # pylint: disable=no-self-use
        """Open URL in default webbrowser."""
        try:
            subprocess.run(["chrome", url], check=True)
        except subprocess.CalledProcessError as exc:
            raise ApplicationError from exc


class ApplicationArgs(argparse.ArgumentParser):
    """Argument Parser for p64 cli."""

    DESC =  "Decode base64 input n times & optionally open result in chrome."
    EPILOG = "p64 will exit if -o, --open is set and chrome can't be located."

    def __init__(self):
        super(ApplicationArgs, self).__init__(  # pylint: disable=super-with-arguments
            prog="p64",
            description=self.DESC,
            epilog=self.EPILOG
        )

        self.add_argument(
            "-l", "--level",
            help="defines how many times all input is decoded (default = 1)",
            dest="level",
            metavar="",
            type=int,
            default=1
        )

        self.add_argument(
            "-o", "--open",
            help="opens all input in chrome if set",
            dest="is_url",
            action="store_true"
        )

        self.add_argument(
            "base64",
            help="contains list of base64 strings to be decoded",
            type=str,
            nargs="+"
        )

        parsed = self.parse_args()
        self.is_url = parsed.is_url
        self.level = parsed.level
        self.content = parsed.base64


def main():
    """Entrypoint for p64."""

    args = ApplicationArgs()
    p64 = Application(args.level, args.is_url)
    for content in args.content:
        try:
            p64.run(content)
        except ApplicationError:
            pass
        except FileNotFoundError:
            sys.exit("p64 could not locate Chrome.")


if __name__ == "__main__":
    main()
