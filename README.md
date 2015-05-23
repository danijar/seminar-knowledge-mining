Seminar Knowledge Mining
========================

Set up instructions
-------------------

1. Install the dependencies listed below using your system's package manager if
you don't have them already.
2. Create a virtual environment inside the repository root by runnning
`virtualenv .` or if you have multiple Python versions `virtualenv -p python3
.`.
3. Activate your virtual environment using `source bin/activate`. Make sure you
the repository name is in front of your shell promt now.
4. Install dependencies inside your virtual environment using `pip install -r
requirements.txt`.

# System dependencies

| Depdendency |   Debian package   |    Arch package   |
| ----------- | ------------------ | ----------------- |
| Python 3    | python3            | python            |
| Pip         | python3-pip        | python-pip        |
| Virtualenv  | python3-virtualenv | python-virtualenv |
| Cython      | cython3            | cython            |
| Fortran     | gfortran           | gcc-fortran       |
| Blas        | libblas-dev        | blas              |
| Lapack      | liblapack-dev      | lapack            |
