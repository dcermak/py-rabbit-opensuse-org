from setuptools import setup

setup(
    name="py-rodo",
    version="0.0.1",
    description="Helper library to process messages on rabbit.opensuse.org",
    author="Dan Čermák",
    author_email="dcermak@suse.com",
    license="LGPL-2.1-or-later",
    python_requires=">=3.10",
    packages=["py_rodo", "py_rodo.backends"],
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pika>=1.3.2",
        "packaging",
    ],
    extras_require={
        "dataclassy": ["dataclassy>=1.0.1 ; python_version < '3.14'"],
        "pydantic": ["pydantic>=1.10"],
    },
    entry_points={
        "console_scripts": [
            "try-listening=py_rodo.cli:try_listening",
        ],
    },
)
