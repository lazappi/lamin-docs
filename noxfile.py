# import os
import shutil
from pathlib import Path
from subprocess import run
from typing import Dict

import nox
from laminci.nox import build_docs, login_testuser1, run_pre_commit

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def install(session: nox.Session) -> None:
    session.run(*"git clone https://github.com/laminlabs/lamindb --depth 1".split())
    session.run(*"pip install ./lamindb[aws,bionty]".split())


EXAMPLES = """
```{toctree}
:maxdepth: 1
:hidden:
:caption: Examples

celltypist
enrichr
bio-lineage
```
"""

INTEGRATIONS = """
```{toctree}
:maxdepth: 1
:hidden:
:caption: Integrations

redun
mnist-local
```
"""

EXTENSIONS = """
```{toctree}
:maxdepth: 1
:hidden:
:caption: Extensions

../bionty/index
```
"""

OTHER_TOPICS_ORIG = """
```{toctree}
:hidden:
:caption: Other topics

../faq/index
../storage/index
```
"""

OTHER_TOPICS = """
```{toctree}
:maxdepth: 1
:hidden:
:caption: Other topics

../faq/index
../architecture
../glossary
../problems
```
"""


def replace_content(filename: Path, mapped_content: Dict[str, str]) -> None:
    with open(filename) as f:
        content = f.read()
    with open(filename, "w") as f:
        for key, value in mapped_content.items():
            content = content.replace(key, value)
        f.write(content)


def pull_from_s3_and_unpack(zip_filename):
    run(
        f"aws s3 cp s3://lamin-site-assets/docs/{zip_filename} {zip_filename}",
        shell=True,
    )
    shutil.unpack_archive(zip_filename, zip_filename.replace(".zip", ""))


@nox.session
def pull_artifacts(session):
    # lamindb
    pull_from_s3_and_unpack("lamindb_docs.zip")
    Path("lamindb_docs/README.md").rename("README.md")
    Path("lamindb_docs/guide").rename("docs/guide")
    Path("lamindb_docs/biology").rename("docs/biology")
    Path("lamindb_docs/faq").rename("docs/faq")
    Path("lamindb_docs/changelog.md").rename("docs/changelog.md")
    # lamindb_setup
    pull_from_s3_and_unpack("lamindb_setup_docs.zip")
    Path("lamindb_setup_docs/guide").rename("docs/setup")
    for file in Path("docs/setup").glob("*"):
        print(file)
        replace_content(
            file,
            {
                "import lamindb_setup as ln_setup": "import lamindb as ln",
                "ln_setup": "ln.setup",
                "lamindb_setup": "lamindb.setup",
            },
        )
    # lamindb guide
    replace_content(
        "docs/guide/index.md",
        {"\nfiles-folders\n": "\n../setup/index\nfiles-folders\n"},
    )
    replace_content("docs/guide/index.md", {OTHER_TOPICS_ORIG: ""})
    # bionty
    pull_from_s3_and_unpack("bionty_docs.zip")
    Path("bionty_docs").rename("docs/bionty")
    replace_content("docs/bionty/index.md", {"../README.md": "./README.md"})
    # integrations
    pull_from_s3_and_unpack("redun_lamin_fasta_docs.zip")
    Path("redun_lamin_fasta_docs/guide/1-redun.ipynb").rename("docs/guide/redun.ipynb")
    Path("redun_lamin_fasta_docs/guide/2-redun-run.ipynb").rename(
        "docs/guide/redun-run.ipynb"
    )
    pull_from_s3_and_unpack("pytorch_lamin_mnist_docs.zip")
    Path("pytorch_lamin_mnist_docs/guide/mnist-local.ipynb").rename(
        "docs/guide/mnist-local.ipynb"
    )
    # examples
    pull_from_s3_and_unpack("lamin_examples_docs.zip")
    Path("lamin_examples_docs/biology/celltypist.ipynb").rename(
        "docs/guide/celltypist.ipynb"
    )
    Path("lamin_examples_docs/biology/enrichr.ipynb").rename("docs/guide/enrichr.ipynb")
    Path("lamin_examples_docs/biology/lineage.ipynb").rename(
        "docs/guide/bio-lineage.ipynb"
    )

    with open("docs/guide/index.md") as f:
        content = f.read()
    with open("docs/guide/index.md", "w") as f:
        content += EXAMPLES
        content += INTEGRATIONS
        content += EXTENSIONS
        content += OTHER_TOPICS
        f.write(content)


@nox.session
def docs(session):
    session.run(*"pip install lamindb==0.42a6".split())
    login_testuser1(session)
    session.run(*"lamin init --storage ./docsbuild".split())
    build_docs(session)
