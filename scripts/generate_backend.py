#!/usr/bin/env python3
"""Generate backend.py for development and type checking."""

import argparse
import os
import sys

BACKENDS = {
    "dataclassy": """from dataclassy import dataclass

@dataclass(frozen=True, kw_only=True, slots=True)
class ObsMessageBusPayloadBase:
    '''Base class for all OBS message bus payload types'''
    pass

__backend__ = 'dataclassy'
""",
    "pydantic-v1": """from pydantic import BaseModel

class ObsMessageBusPayloadBase(BaseModel):
    '''Base class for all OBS message bus payload types'''

    class Config:
        frozen = True
        extra = 'forbid'

__backend__ = 'pydantic-v1'
""",
    "pydantic-v2": """from pydantic import BaseModel, ConfigDict

class ObsMessageBusPayloadBase(BaseModel):
    '''Base class for all OBS message bus payload types'''

    model_config = ConfigDict(frozen=True, extra='forbid')

__backend__ = 'pydantic-v2'
""",
}


def generate_backend(backend, output_path):
    if backend not in BACKENDS:
        print(f"Error: Invalid backend '{backend}'", file=sys.stderr)
        print(f"Valid backends: {', '.join(BACKENDS.keys())}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(BACKENDS[backend])

    print(f"Generated {output_path} with backend={backend}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate backend.py for py-rodo development"
    )
    parser.add_argument("backend", choices=BACKENDS.keys(), help="Backend to use")
    parser.add_argument(
        "--output", default="src/py_rodo/backend.py", help="Output path"
    )

    args = parser.parse_args()
    generate_backend(args.backend, args.output)


if __name__ == "__main__":
    main()
