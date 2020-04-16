# Changelog
All notable changes to `author_rank` will be documented in this Changelog.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) 
and adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.0.3

### Changed 

- The visualization has been updated with suggested improvements 
from [Edward Barraza](https://github.com/edwardbarraza): 
* Contain the ranks within the vertices shown on the visualization
* Change the color of the vertices to #489FDF
* Change the color of text within the vertices to #ECF2FF
* Change the color of the hover / selection states to #F2A900
* Change the written text color to #3B3B3B
* Subtitles for each vertex label if the `note` field is available for 
the vertex

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

