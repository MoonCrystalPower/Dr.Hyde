# Dr.hyde
[![Travis CI](https://travis-ci.org/MoonCrystalPower/Dr.Hyde.svg?branch=master)](https://travis-ci.org/MoonCrystalPower/Dr.Hyde)
[![Code Coverage](https://img.shields.io/codecov/c/github/MoonCrystalPower/Dr.Hyde/master.svg?label=branch%20coverage)](https://codecov.io/github/MoonCrystalPower/Dr.Hyde?branch=master)

## Introduction
Dr.Hyde is a Local REST-API server for Dr.Jekyll. And it has a PYHTML2MD module.

## Installation
1. `$> mkvirtualenv --python=$(which python3) hyde_venv`
2. `$> pip install -r test-requirements.txt -r requirements.txt`


## Requirments
* Python3
* [PyHtml2Md](https://github.com/MoonCrystalPower/PyHtml2Md)

## CodeFormat test
`$> coala` 

## Test
`$> pytest --cov=hyde ./tests`

## Run
`python manage.py runserver`

## Contribution Guide
* [Contribution Guide](https://github.com/MoonCrystalPower/Dr.Hyde/blob/master/CONTRIBUTION.md)

## License
```
MIT License

Copyright (c) 2018 MoonCrystalPower

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
