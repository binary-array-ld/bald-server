# bald-server
This repo provides landing pages and web APIs for BALD graphs - exposed as RDF triples or JSON-LD (schema.org profile).

## Current features
* REST API
* HTML Templated content with schema.org embedded in

## To do
* RDF Triple store backend serving BALD graphs


## Pre-requisites
* Docker 1.6+
* docker-compose 1.3+

## Quickstart

Spin up the python flask app and mongo via docker-compose
```
$ docker-compose up -d
```

Your application should be now running on http://localhost:4000

## Usage

## Loading schema.org descriptions

Assuming you have a directory of schema.org descriptions as json-ld, you can use the `example-uploader.sh` (as-is or customised),
to upload content to via APIs. This will then be listed in the application running on http://localhost:4000

A possible way to get a list of these descriptions is to use the threddsnc2rdf.py tool in the `bald` library.

### Routes

* GET '/' - list of datasets
* GET '/view?id=param1&format=param2' - view the dataset. param1 is the ID of the dataset, param2 (optional) currently allows 'jsonld'
* POST '/new' - add a new dataset description in JSON format (schema.org)
