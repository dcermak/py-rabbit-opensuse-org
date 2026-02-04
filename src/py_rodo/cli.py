"""Command-line interface entry points for py_rodo."""

import argparse
import sys


def try_listening() -> None:
    """Entry point for try-listening command.

    Configures the backend before importing the actual implementation.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--backend",
        "-b",
        choices=["pydantic", "dataclassy"],
        default="pydantic",
        help="Backend to use for message payload classes (default: pydantic)",
    )
    args, remaining = parser.parse_known_args()

    from py_rodo import config

    config.set_backend(args.backend)

    sys.argv = [sys.argv[0]] + remaining

    from py_rodo.callback import try_listening as _try_listening

    _try_listening()
