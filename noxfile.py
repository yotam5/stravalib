import os
import pathlib
import shutil

import nox

nox.options.reuse_existing_virtualenvs = True


# Use this for venv envs nox -s test
@nox.session(python=["3.9", "3.10", "3.11"])
def test(session):
    session.install(".[all]")
    session.install("-r", "requirements.txt")
    session.run(
        "pytest",
        "--cov",
        "stravalib",
        "stravalib/tests/unit/",
        "stravalib/tests/integration/",
    )


# Use this for conda/mamba = nox -s test_mamba
@nox.session(venv_backend="mamba", python=["3.9", "3.10", "3.11"])
def test_mamba(session):
    session.install(".[all]")
    session.install("-r", "requirements.txt")
    session.run(
        "pytest",
        "--cov",
        "stravalib",
        "stravalib/tests/unit/",
        "stravalib/tests/integration/",
    )


# Build docs!
build_command = ["-b", "html", "docs/", "docs/_build/html"]


@nox.session
def docs(session):
    session.install("-r", "requirements.txt")
    cmd = ["sphinx-build"]
    cmd.extend(build_command + session.posargs)
    session.run(*cmd)


@nox.session(name="docs-live")
def docs_live(session):
    session.install("-r", "requirements.txt")

    AUTOBUILD_IGNORE = [
        "_build",
        "build_assets",
        "tmp",
    ]
    cmd = ["sphinx-autobuild"]
    for folder in AUTOBUILD_IGNORE:
        cmd.extend(["--ignore", f"*/{folder}/*"])
    cmd.extend(build_command + session.posargs)
    session.run(*cmd)


# Use this for venv envs nox -s test
@nox.session(python=["3.9", "3.10", "3.11"])
def mypy(session):
    session.install(".[all]")
    session.install("-r", "requirements.txt")
    session.run(
        "mypy",
    )


@nox.session(name="docs-clean")
def clean_docs(session):
    """
    Clean out the docs directory used in the
    live build.
    """
    dir_path = pathlib.Path("docs", "_build")
    print(dir_path)
    dir_contents = dir_path.glob("*")

    for content in dir_contents:
        print(f"cleaning content from the {dir_path}")
        if content.is_dir():
            shutil.rmtree(content)
        else:
            os.remove(content)