# Prezi API

A small application that allows users to request Prezi objects and 
their creators in JSON format via a RESTful API.

## What can you do?

As anonymous user, you can do the following:

- `/api/prezis` - list all Prezi objects
- `/api/prezis/<id>` - get a single Prezi object by id
- `/api/prezis/?order=ASC` - list all Prezi objects by date in ascending order
- `/api/prezis/?order=DESC` - list all Prezi objects by date in descending order
- `/api/prezis/?search=<search term>` - list all Prezi objects with a title that
 contains the search term


As an authenticated user, you can do the following:

- `/api/prezis/<id>` - update a Prezi field via a PATCH request or **update 
multiple fields via a PUT request.

> <sub>** for PUT requests all required fields must be added to the json 
data sent</sub>

## Run the app locally

Clone the project to a local directory, ensure that you have docker installed 
and then run the following commands:

```bash
make migrate
make createsuperuser
make start
```

You can run `make help` to see a list of all of the make commands available.
