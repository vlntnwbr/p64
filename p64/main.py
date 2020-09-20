"""Application and entrypoint for p64."""

import argparse
import base64
import subprocess
import sys


class ApplicationError(BaseException):
    """Non fatal exception to be caught in entrypoint."""


class Application:  # pylint: disable=too-few-public-methods
    """Application object."""

    def __init__(self, level: int, silent: bool):
        self.level = level
        self.silent = silent
        self.error = None

    def run(self, content: str) -> None:
        """Run the Application once."""

        logmsg, logcat = "{:10}{}", "RESULT"
        decoded = self._decode(content)
        if self.error is not None:
            print(logmsg.format("ERROR", str(self.error)))
            raise ApplicationError(self.error)
        if not self.silent:
            logcat = "OPENING"
            self._open(decoded)
        print(logmsg.format(logcat, decoded))

    def _decode(self, content: str) -> str:
        """Return base64 'content' decoded 'level' times."""
        try:
            res = content.encode("utf-8")
            for i in range(self.level):  # pylint: disable=unused-variable
                res = base64.b64decode(res)
            return res.decode("utf-8")
        except:  # pylint: disable=bare-except
            self.error = f"Could not decode '{content}'"

    def _open(self, url: str) -> None:  # pylint: disable=no-self-use
        """Open URL in default webbrowser."""
        try:
            subprocess.run(["chrome", url], check=True)
        except subprocess.CalledProcessError as exc:
            raise ApplicationError from exc


class ApplicationArgs(argparse.ArgumentParser):
    """Argument Parser for p64 cli."""

    def __init__(self):
        super(ApplicationArgs, self).__init__(  # pylint: disable=super-with-arguments
            prog="p64",
            description="Decodes base64 input and opens result in chrome.",
            epilog="p64 exits if chrome isn't found and --silent isn't set."
        )
        self.add_argument(
            "-s", "--silent",
            help="skips opening results in chrome if set",
            dest="silent",
            action="store_true"
        )
        self.add_argument(
            "-l", "--level",
            help="defines how many times all input is decoded (default = 1)",
            metavar="",
            type=int,
            default=1
        )
        self.add_argument(
            "base64",
            help="contains list of base64 strings to be decoded",
            type=str,
            nargs="+"
        )
        self.parsed = self.parse_args()


def main():
    """Entrypoint for p64."""

    args = ApplicationArgs()
    p64 = Application(args.parsed.level, args.parsed.silent)
    for content in args.parsed.base64:
        try:
            p64.run(content)
        except ApplicationError:
            p64.error = None
        except FileNotFoundError:
            sys.exit("p64 could not locate Chrome.")


if __name__ == "__main__":
    main()
