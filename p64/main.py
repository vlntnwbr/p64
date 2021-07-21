"""Application and entrypoint for p64."""

import argparse
import base64
import os
import subprocess
import sys


class ApplicationError(BaseException):
    """Non fatal exception to be caught in entrypoint."""


class Application:  # pylint: disable=too-few-public-methods
    """Application object."""

    def __init__(self, level: int, browser: str, silent: bool):
        self.level = level
        self.browser = browser
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
            if self.browser is None:
                err = "No browser specified and env var 'P64_BROWSER' not set"
                print("ERROR", err)
                raise ApplicationError(err)
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
            subprocess.run([self.browser, url], check=True)
        except subprocess.CalledProcessError as exc:
            raise ApplicationError from exc


class ApplicationArgs(argparse.ArgumentParser):
    """Argument Parser for p64 cli."""
    
    DESC = (
        "Decodes base64 input and opens result in given browser. If browser is"
        " not specified p64 will use path in 'P64_BROWSER' environment"
        " variable."
        )
    EPILOGUE = (
        "The application will exit if --silent isn't set and a browser either"
        " isn't specified or it'S executable can't be located."
    )

    def __init__(self):
        super(ApplicationArgs, self).__init__(  # pylint: disable=super-with-arguments
            prog="p64",
            description=self.DESC,
            epilog=self.EPILOGUE
        )
        self.add_argument(
            "-s", "--silent",
            help="skips opening results in browser if set",
            dest="silent",
            action="store_true"
        )
        self.add_argument(
            "-l", "--level",
            help="defines how many times all input is decoded (default = 1)",
            action="count",
            default=1
        )
        self.add_argument(
            "-b", "--browser",
            help="path to browser executable.",
            metavar="",
            default=os.getenv("P64_BROWSER")
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
    print(args.parsed.level)
    p64 = Application(args.parsed.level, args.parsed.browser, args.parsed.silent)
    """for content in args.parsed.base64:
        try:
            p64.run(content)
        except ApplicationError:
            p64.error = None
        except FileNotFoundError:
            sys.exit("p64 could not locate browser.")"""


if __name__ == "__main__":
    main()
