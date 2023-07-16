# **Debt Visual**
**Debt Visual** is an application that accurately depicts a country’s debt. Almost everything will include links to the source, fomenting transparency.

## ✏️ **Develop**
To begin you should have the following applications installed on your local development system:

- Python >= 3.11
- [pip](http://www.pip-installer.org/) >= 20


### 💪🏽 **Setup**

**1. Get the project**

First clone the repository from Github and switch to the new directory:

```linux
    $ git clone
    $ cd debt_visual
```

**2. Set up virtual environment**

Set it up as you please

**3. Install dependencies**

```
pip install -r requirements.txt
```

**4. Pre-commit**

pre-commit is used to enforce a variety of community standards. CI runs it,
so it's useful to setup the pre-commit hook to catch any issues before pushing
to GitHub and reset your pre-commit cache to make sure that you're starting fresh.

To install, run:

```linux
    $ pre-commit clean
    $ pre-commit install
```

**5. Database**
Note: For simplicity, the project is currently running SQLite3

**6. Migrate and create a superuser**

```linux
    $ python manage.py migrate
    $ python manage.py createsuperuser
```

**7. Run the server**

```linux
    $ python manage.py migrate
```

**8. Run tests**

The project uses [pytest-django](https://pytest-django.readthedocs.io/en/latest/index.html) for testing.

To run tests, run:

```linux
    $ pytest
```
