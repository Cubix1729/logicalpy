# Contributing to LogicalPy

The project welcomes any type of contribution.
This document provides guidelines concerning how to contribute to LogicalPy.

## How to make contributions

### 1. Fork the project

First, fork the project in GitHub.
Then, you can clone your forked repository to your local computer:

```
git clone https://github.com/<your-username>/logicalpy.git
cd logicalpy
```

### 2. Set up your development environment

In order to contribute to the project, you will need to install it locally.

 - You can first optionally create a virtual environment
 - Then, locally install the project in editable mode and with all of the development dependencies using:
    ```
    pip install -e .[dev]
    ```

### 3. Make and commit your changes

Once your are ready, create a new branch, make your changes and commit them with
descriptive messages (preferably use the past tence).

### 4. Create a pull request

After pushing your changes to your forked repository, create a pull request to the
`master` branch of the original repository. Provide a clear explanation of what you have done,
as well as any relevant context.

### 5. Review and merge

Your pull request will then be reviewed, and once it has been approved, it will be
merged to the main project 🎉.

## Project dependencies

The project uses:

 - `lark` for parsing logical formulae
 - `tabulate` for making truth tables

## Code style and testing guidelines

To meet the project's code style, please format the code with `black` using the command
`black <path-to-the-code>`. (The maximum line length used is the default one, i.e. 88 
characters).

If you implement any new feature or change an existing one, please update the tests in
consequence. They are written with the `unittest` library of the Python standard library.

For any modification you make, ensure the tests still pass by running (from the main folder
or from the `tests` folder):

```
python -m unittest
```

The project uses `coverage` to generate test coverage reports. The coverage badge present in both
the README.md and the documentation homepage is then generated with the `coverage-badge`
Python package.

## Documentation changes

The documentation is written in Markdown and built using `mkdocs` (more precisely with `mkdocs-material`).
The `mkdocs` documentation configuration is in the file `mkdocs.yml`.

If you make changes to the documentation, you can use `mkdocs serve` to build the documentation locally and
view it your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Opening an issue

If you find a bug or issue in the project, please [open an issue](https://github.com/Cubix1729/logicalpy/issues/new)
to report it. Be sure to include:

 - A clear description of the bug
 - How to reproduce it
 - Expected and actual behaviour
 - The error message if there is one
 - The LogicalPy version used and your environment setup

You can also open an issue if you want to suggest a feature or if you have a question.

## Thank you

Thank you for your interest in contributing to LogicalPy!

Happy propositional logic and programming! 🤓👨‍💻
