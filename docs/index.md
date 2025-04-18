# LogicalPy

[![PyPi version](https://badgen.net/pypi/v/logicalpy/)](https://pypi.org/project/logicalpy)
[![License](https://img.shields.io/github/license/Cubix1729/logicalpy)](https://github.com/Cubix1729/logicalpy/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

LogicalPy is a small Python library providing basic functionalities for manipulating propositional logic.

## Description

The library allows to work with classical propositional logic formulae.
The main features include:

 - The construction of logical formulae either directly or from a string
 - The visualisation of truth tables
 - The implementation of semantic notions: satisfiability, entailment...
 - The conversion to normal forms (NNF, CNF, or DNF)
 - Automated theorem proving with the resolution procedure

## Installation

With pip:
```
pip install logicalpy
```

Note that the library needs a Python version higher than 3.9.

## Usage

For getting started, see the [usage](usage/constructing-formulae.md) section.

For a complete project reference, see the [API Reference](api-reference/logicalpy/index.md).

## Contributing

If you want to contribute to this (small) project, you can [open an issue](https://github.com/Cubix1729/logicalpy/issues)
to report a bug or request a feature, or [make a pull request](https://github.com/Cubix1729/logicalpy/pulls).

## Tests

To run the the tests, clone the repository, go into the `tests` directory and run `python -m unittest`.

## License

This project is licensed under the MIT license.
