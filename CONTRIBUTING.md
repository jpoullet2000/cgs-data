# How to contribute

`cgs-data` is part of the [`cgs` project](https://github.com/jpoullet2000/cgs). This package and all the packages within the `cgs` project are open to anyone who wants to get involved.

## Getting Started

* Create a new, Python 2.7+ virtualenv and install the requirements via pip: `pip install -r requirements.txt`
* Make sure you have a [GitHub account](https://github.com/signup/free)
* Either sumbit an issue directly on [GitHub](https://github.com/jpoullet2000/cgs-data) page
  * For bugs, clearly describe the issue including steps to reproduce
  * For enhancement proposals, be sure to indicate if you're willing to work on implementing the enhancement
* Fork the repository on GitHub

## Making changes

* **cgs-data** uses git-flow as the git branching model
  * No commits should be made directly to `master`
  * [Install git-flow](https://github.com/nvie/gitflow) and create a `feature` branch like so: `$ git flow feature start <name of your feature>`
* Make commits of logical units.
* Check for unnecessary whitespace with `git diff --check` before committing.
* Test coverage should be added soon to track whether 100% of the code is tested (see [coveralls.io](https://coveralls.io/r/jeffknupp/sandman?branch=develop) for more information).

## Submitting Changes

* Push your changes to the feature branch in your fork of the repository.
* Submit a pull request to the main repository

## Additional Resources

* [General GitHub documentation](http://help.github.com/)
* [GitHub pull request documentation](http://help.github.com/send-pull-requests/)
