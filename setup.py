import os
import sys

# Add scripts directory to path so we can import generate_backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from generate_backend import generate_backend
from setuptools import setup
from setuptools.command.build_py import build_py

BACKEND = os.getenv("PY_RODO_BACKEND", "dataclassy")

# Compute package name based on backend
# Results in: py-rodo-dataclassy, py-rodo-pydantic-v1, or py-rodo-pydantic-v2
PACKAGE_NAME = f"py-rodo-{BACKEND}"

# Compute dependencies based on backend
INSTALL_REQUIRES = ["pika>=1.3.2"]

if BACKEND == "dataclassy":
    INSTALL_REQUIRES.append("dataclassy>=1.0.1")
elif BACKEND == "pydantic-v1":
    INSTALL_REQUIRES.append("pydantic<2.0")
elif BACKEND == "pydantic-v2":
    INSTALL_REQUIRES.append("pydantic>=2.0")
else:
    raise ValueError(f"Unknown backend: {BACKEND}")


class CustomBuildPy(build_py):
    """Custom build_py command that generates backend.py at build time.

    Backend selection is controlled by the PY_RODO_BACKEND environment variable:
    - Set to 'dataclassy', 'pydantic-v1', or 'pydantic-v2'
    - Defaults to 'dataclassy' if not set
    - Must be set before running `pip install` or `python -m build`
    - The backend dependency is automatically added to the wheel metadata

    Example usage:
        PY_RODO_BACKEND=pydantic-v2 python -m build
        pip install .
    """

    def run(self):
        super().run()

        backend_file = os.path.join(self.build_lib, "py_rodo", "backend.py")

        print(f"Building package: {PACKAGE_NAME}")
        print(f"Wheel will require: {', '.join(INSTALL_REQUIRES)}")

        # Use generate_backend from scripts/generate_backend.py
        generate_backend(BACKEND, backend_file)


setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    description="Helper library to process messages on rabbit.opensuse.org",
    author="Dan Čermák",
    author_email="dcermak@suse.com",
    license="LGPL-2.1-or-later",
    python_requires=">=3.10",
    packages=["py_rodo"],
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    cmdclass={"build_py": CustomBuildPy},
    # Optional dependencies for development
    extras_require={
        "dataclassy": ["dataclassy>=1.0.1 ; python_version < '3.14'"],
        "pydantic-v1": ["pydantic<2.0 ; python_version < '3.14'"],
        "pydantic-v2": ["pydantic>=2.0"],
    },
    entry_points={
        "console_scripts": [
            "try-listening=py_rodo.callback:try_listening",
        ],
    },
)
