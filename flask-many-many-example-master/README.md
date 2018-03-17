# Many To Many Example

A departments and employees app that illustrates many to many.

### Setup

* Fork and clone the repository and `cd` into the cloned repository.

* Make a virtual environment

```sh
mkvirtualenv m2m
```

* Make the `many-many-example` database:

```sh
createdb many-many-example
```

* pip install requirements.txt:

```sh
pip install -r requirements.txt
```

* Upgrade the database so that your tables are created correctly:

```sh
flask db upgrade
```

* Start the server!

```sh
flask run
```

### Goal

Right now departments don't implement full CRUD. Modify the functionality so that we have full CRUD on departments, including the ability to add or remove employees from the department when we add or edit it.

### Testing

Unit tests are located in `project/tests`. To run all the tests as once, type `green` in the root of the project.

To run a specific tests (if you want to debug with ipython):

```sh
python -m project.tests.<name_of_test> # no .py at the end
```
