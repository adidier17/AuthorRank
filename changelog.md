# Changelog
All notable changes to `author_rank` will be documented in this Changelog.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) 
and adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.1.3
### Fixed 
- An issue that caused AuthorRank to fail when documents 
without authors are accidentally provided as part of the
set of documents. Additional checks have been added to
`author_rank/graph.py`.

## 0.1.2 
### Fixed
- An identified issue that resulted in disconnected (i.e. non-co-authoring) 
authors to be connected in the AuthorRank graph. Several code changes 
were introduced to address this issue. 

## 0.1.1
### Changed 
- The progress bar functionality such that it indicates progress on the 
`.fit()` function across both the graph creation and scoring of authors 
(previously the progress bar only covered the former). 

### Fixed
- A typo in `author_rank/__init__.py` that referred to the library as 
`NetworkX` and not `AuthorRank`. 


## 0.1.0
### Changed 
- The manner in which users interact with the library to more
closely mirror the conventions of the [scikit-learn](https://scikit-learn.org/) 
and [NetworkX](https://networkx.github.io/) libraries, as described in 
[this issue](https://github.com/adidier17/AuthorRank/issues/10). 
- Example code and Jupyter notebooks to align with the changes 
described in the above line item. 

### Added 
- A warning to users when attempting to fit AuthorRank with a 
document set that has a single author. AuthorRank requires at 
least 2 authors in the document set. 
- A warning in the case that users attempt to call `top_authors` 
prior to `fit`. The AuthorRank approach must first be fit 
to a set of documents before returning the top authors.
- A test to ensure that data processing occurs within a specified 
time bound (in seconds). 

### Fixed 
- A bug whereby the incorrect list of authors per document 
was being processed into the AuthorRank graph. 


## 0.0.3
### Added

- A progress bar as an optional argument for creating the `graph.create` 
and `score.top_authors` functions, which provides users an indication of 
how far along the processing is on the input documents. 

### Fixed 
- An ZeroDivisionError that would result in the top_authors calculation 
failing in some cases. A dataset that results in this case has been 
added to the testing suite and a fix developed.

### Changed 
- Libraries required listed in `setup.py`. 

## 0.0.2
### Changed 

- Updates the normalization of scores in `top_authors` to a pure Python 
approach, removing the `numpy` and `scikit-learn` requirements. 

## 0.0.1
### Added
- An example dataset in the `data` directory.
- `examples` and `notebooks` directories that contain code that 
demonstrates how to use AuthorRank.
- Unit tests within the `tests` directory. 
- Support for continuous integration and coverage reporting with Travis CI 
and coveralls.io. 
- The MIT license.
- `requirements.txt`, `requirements_ci.txt`, and `requirements_notebooks.txt` 
files that list dependencies for author_rank, continuous integration, and
notebooks, respectively.
- A `setup.py` file for pip installs. 
- This changelog.

### Changed
- Refactored the code for improved readability, usability and maintainability. 
- Reorganized the repository for improved maintainability.

