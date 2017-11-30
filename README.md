# Pacifica Python Uploader
[![Build Status](https://travis-ci.org/pacifica/pacifica-python-uploader.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-python-uploader)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-python-uploader/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-python-uploader)
[![Test Coverage](https://codeclimate.com/github/pacifica/pacifica-python-uploader/badges/coverage.svg)](https://codeclimate.com/github/pacifica/pacifica-python-uploader/coverage)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-python-uploader/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-python-uploader)

Pacifica Python Uploader, `PacificaUploader`, is a Python programming language
library for managing, serializing and transporting (over a network) archives of
files (referred to as "bundles"), managing both the data and the metadata of the
bundle, and interacting with
[Pacifica Ingest](https://github.com/pacifica/pacifica-ingest) and
[Pacifica Policy](https://github.com/pacifica/pacifica-policy) servers.

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
> "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be
> interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## API reference

This section gives an overview of the modules, classes and methods that are
exported by the Pacifica Python Uploader library: `PacificaUploader`.

### `uploader.metadata` module

The `uploader.metadata` module exports classes and methods for manipulating and
serializing the metadata for bundles of files.

Encoding and decoding to the JSON data format is supported for compatible
objects (see `uploader.metadata.Json` module for more information).

#### `uploader.metadata.MetaData(list)` class

Instances of the `uploader.metadata.MetaData` class are upper-level objects that
provide the metadata for interacting with the designated
[Pacifica Ingest](https://github.com/pacifica/pacifica-ingest) server.

The `uploader.metadata.MetaData` class is a sub-class of `list` that implements
the index protocol (`__getitem__`, `__setitem__` and `__delitem__`) as a proxy
to the indices of the value of the `metaID` field of the associated instance of
the `uploader.metadata.MetaObj` class.

#### `uploader.metadata.MetaObj(collections.namedtuple)` class

Instances of the `uploader.metadata.MetaObj` class represent units of metadata
whose representation is disjoint to a file, i.e., units of metadata that are
describe but are not stored as part of a file.

The `uploader.metadata.MetaObj` class is a sub-class of the
`collections.namedtuple` class with the following named fields:
* `sourceTable`
* `destinationTable`
* `metaID`
* `displayType`
* `displayTitle`
* `queryDependency`
* `valueField`
* `queryFields`
* `displayFormat`
* `key`
* `value`
* `directoryOrder`
* `query_results`

#### `uploader.metadata.FileObj(collections.namedtuple)` class

Instances of the `uploader.metadata.FileObj` class represent individual files,
including both the data and metadata for the file. During a file upload,
instances of the `uploader.metadata.FileObj` class are automatically associated
with new instances of the `uploader.metadata.MetaData` class.

The `uploader.metadata.FileObj` class is a sub-class of the
`collections.namedtuple` class with the following named fields:
* `destinationTable`
* `name`
* `subdir`
* `size`
* `hashtype`
* `hashsum`
* `mimetype`
* `ctime`
* `mtime`

The above named fields are identical to those of the `metadata.orm.Files` class,
provided by the
[Pacifica Metadata](https://github.com/pacifica/pacifica-metadata) library.

#### `uploader.metadata.metadata_decode(json_str)` method

The `uploader.metadata.metadata_decode()` method deserializes the given
JSON source, `json_str`, and then returns a new instance of the
`uploader.metadata.MetaData` class.

The new instance is automatically associated with new instances of the
`uploader.metadata.MetaObj` and `uploader.metadata.FileObj` classes.

#### `uploader.metadata.metadata_encode(md_obj)` method

The `uploader.metadata.metadata_encode()` method encodes the given
instance of the `uploader.metadata.MetaData` class, `md_obj`, as a JSON object,
and then returns its JSON serialization.

Associated instances of the `uploader.metadata.MetaObj` and
`uploader.metadata.FileObj` classes are automatically included in the JSON
object and the resulting JSON serialization.

#### `uploader.metadata.Json` module

The `uploader.metadata.Json` module exports generators for encoding and decoding
instances of the `collections.namedtuple` class using the JSON data format.

The `uploader.metadata.Json.generate_namedtuple_encoder()` and
`uploader.metadata.Json.generate_namedtuple_decoder()` methods return
sub-classes of the given super-class, which delegate to instances of the
`json.JSONEncoder` and `json.JSONDecoder` classes, respectively.

#### `uploader.metadata.PolicyQuery` module

The `uploader.metadata.PolicyQuery` module exports classes and methods for
interacting with the designated
[Pacifica Policy](https://github.com/pacifica/pacifica-policy) server.

##### `uploader.metadata.PolicyQuery.PolicyQuery(uploader.common.CommonBase)` class

Instances of the `uploader.metadata.PolicyQuery.PolicyQuery` class represent
queries to the designated
[Pacifica Policy](https://github.com/pacifica/pacifica-policy) server.

The HTTP end-point for the designated
[Pacifica Policy](https://github.com/pacifica/pacifica-policy) server is
automatically pulled either from the system environment or from the keyword
arguments, `**kwargs`, for the
`uploader.metadata.PolicyQuery.PolicyQuery(user, *args, **kwargs)` constructor.

The `uploader.metadata.PolicyQuery.PolicyQuery.valid_metadata(md_obj)` method
validates the given instance of the `uploader.metadata.MetaData` class,
`md_obj`, with respect to the capabilities of the designated
[Pacifica Policy](https://github.com/pacifica/pacifica-policy) server.

The `uploader.metadata.PolicyQuery.PolicyQuery.get_results()` method returns a
JSON object that represents the result set for a query to the designated
[Pacifica Policy](https://github.com/pacifica/pacifica-policy) server, i.e., the
entities that match the criteria that is represented by the associated instance
of the `uploader.metadata.PolicyQuery.PolicyQueryData` class.

The success or failure of the query to the designated
[Pacifica Policy](https://github.com/pacifica/pacifica-policy) server is
indicated by the HTTP status code of the query response.

##### `uploader.metadata.PolicyQuery.PolicyQueryData(collections.namedtuple)` class

Instances of the `uploader.metadata.PolicyQuery.PolicyQueryData` class represent
the data for the generation of a query to a designated
[Pacifica Policy](https://github.com/pacifica/pacifica-policy) server.

The `uploader.metadata.PolicyQuery.PolicyQueryData` class is a sub-class of the
`collections.namedtuple` class with the following named fields:
* `user`
* `columns`
* `from_table`
* `where`

#### `uploader.metadata.MetaUpdate` module

The `uploader.metadata.MetaUpdate` module exports classes and methods for
constructing and executing the strategy for modifying the values, including the
parents and children, of instances of the `uploader.metadata.MetaData` class.

##### `uploader.metadata.MetaUpdate.MetaUpdate(uploader.metadata.MetaData)` class

The `uploader.metadata.MetaUpdate.MetaUpdate` class is a sub-class of the
`uploader.metadata.MetaData` class that is specialized to issue and handle
queries to [Pacifica Policy](https://github.com/pacifica/pacifica-policy)
servers.

### `uploader.bundler` module

The `uploader.bundler` module exports classes and methods for constructing and
streaming bundles of files to a designated file descriptor. The file descriptor
is opened once, and the stream is generated by a single pass over the specified
files.

#### `uploader.bundler.Bundler(object)` class

The `uploader.bundler.Bundler.stream()`
method streams a bundle of files to a designated file descriptor. The
`uploader.bundler.Bundler` class is created by providing a `list` of `dict`s
that specifies the arguments to the `tarfile.TarFile.gettarinfo()` method.

> **Note:** The `arcname` keyword argument MUST be provided when calling the
> `tarfile.TarFile.gettarinfo()` method.

The `uploader.bundler.Bundler.stream()` method is a blocking I/O operation.
An asynchronous callback method MAY be provided via the optional `callback`
keyword argument. Periodically, the callback method is provided with the current
percentage of completion.

> **Note:** File handles are opened for reading in binary mode.

### `uploader.Uploader` module

The `uploader.Uploader` module exports classes and methods for interacting with
[Pacifica Ingest](https://github.com/pacifica/pacifica-ingest) servers.

#### `uploader.Uploader.Uploader(uploader.common.CommonBase)` class

The `uploader.Uploader.Uploader` class exports methods that provide an API for
connecting to and handling connections to
[Pacifica Ingest](https://github.com/pacifica/pacifica-ingest) servers.

The `uploader.Uploader.Uploader.upload()` method takes a file-like object as
input that has been opened for reading in binary mode, and returns a `job_id`
for the upload.

The `uploader.Uploader.Uploader.getstate()` method takes a `job_id` as input,
and returns a JSON object, as defined by the
[Pacifica Ingest](https://github.com/pacifica/pacifica-ingest) API for
obtaining the status of the current job.

## Uploader Expectations and Application Flows

This section describes how an end-user of Pacifica Python Uploader is expected
to interact with the modules, classes and methods above, and, by extension,
[Pacifica Ingest](https://github.com/pacifica/pacifica-ingest) and
[Pacifica Policy](https://github.com/pacifica/pacifica-policy) servers.

### Uploader Program Flow

1. The uploader program MUST construct a new instance of the
   `uploader.metadata.MetaUpdate` class. The new instance of the
   `uploader.metadata.MetaUpdate` class MAY be associated with zero or more of
   instances of the `uploader.metadata.MetaObj` class. The
   `uploader.metadata.MetaObj.value` field MAY be `None`. The new instance of
   the `uploader.metadata.MetaUpdate` class MUST NOT be associated with any
   instances of the `uploader.metadata.FileObj` class.

2. To determine completeness, the new instance of the
   `uploader.metadata.MetaUpdate` class SHOULD be validated using the
   `uploader.metadata.MetaData.is_valid()` method (inherited by the
   `uploader.metadata.MetaUpdate` sub-class). Then, the uploader program MUST
   call the `uploader.metadata.PolicyQuery.PolicyQuery.valid_metadata()` method.
   The new instance of the `uploader.metadata.MetaUpdate` class MUST be valid
   prior to bundling.

3. The uploader program MUST dereference the
   `uploader.metadata.MetaObj.displayType` field to determine the mode of
   selection for the `uploader.metadata.MetaObj.value` field. The value of the
   `uploader.metadata.MetaObj.displayType` field is uploader-program-specific,
   i.e., the value MUST be defined by the uploader program.

4. The uploader program MUST assign a non-`None` value to each
   `uploader.metadata.MetaData.query_results` field by calling the
   `uploader.metadata.MetaUpdate.query_results()` method. The
   `uploader.metadata.MetaData.query_results` field is a `list`.

5. The value of the `uploader.metadata.MetaData.query_results` field MUST be
   rendered according to the uploader-program-specific definition that is
   interpreted from the value of the `uploader.metadata.MetaObj.displayFormat`
   field, e.g., in the Python programming language, by calling the `str.format`
   method or by leveraging a template engine, such as
   [Cheetah](https://pypi.python.org/pypi/Cheetah) or
   [Jinja2](https://pypi.python.org/pypi/Jinja2).

6. The uploader program MAY call the
   `uploader.metadata.MetaUpdate.query_results()` method for instances of the
   `uploader.metadata.MetaObj` class whose `value` field is non-`None`.

7. The uploader program MUST handle all instances `uploader.metadata.MetaUpdate`
   class, regardless of validity, i.e., the uploader program MUST NOT reject an
   instance of the `uploader.metadata.MetaUpdate` class under any circumstances,
   e.g., if there are unsatisfied dependencies between instances of the
   `uploader.metadata.MetaData` class.

8. When the uploader program is ready for a given
   `uploader.metadata.MetaObj.value` field to be selected, the uploader program
   MUST assign to the `uploader.metadata.MetaObj.value` field the value of the
   `uploader.metadata.MetaObj.valueField` field, and then call the
   `uploader.metadata.MetaObj.update_parents()` method. The effect of this
   operation is to update the `uploader.metadata.MetaObj.value` fields of
   associated and dependent instances of the `uploader.metadata.MetaObj` class.
   After modification, the new state of the instance of the
   `uploader.metadata.MetaUpdate.MetaUpdate` class SHOULD be displayed to the
   end-user, as previously discussed.

9. The uploader program MUST verify that
   `uploader.metadata.MetaUpdate.MetaUpdate.is_valid() == True`. If the instance
   of the `uploader.metadata.MetaUpdate.MetaUpdate` class is not valid, then the
   uploader program MUST repeat the instructions in the paragraph 8.

10. The uploader program MUST call the
    `uploader.metadata.PolicyQuery.PolicyQueryData.valid_metadata()` method to
    validate the instance of the `uploader.metadata.MetaUpdate.MetaUpdate` class
    prior to upload. This prevents the uploader program from uploading metadata
    that is invalid with respect to the policy of the
    [Pacifica Ingest](https://github.com/pacifica/pacifica-ingest) server.

11. When the uploader program is ready to bundle the data, the uploader program
    MUST construct a `list` of objects, representing the fields of the
    corresponding instance of the `tar.TarInfo` class. Each object MUST export a
    `fileobj` field whose value implements the file protocol, i.e., exports a
    `read()` method.

12. The uploader program MUST construct a new instance of the
    `metadata.bundler.Bundler` class using the instances of the
    `uploader.metadata.MetaUpdate.MetaUpdate` and `tar.TarInfo` classes, as
    previously stated in paragraph 11. Then, the uploader program MUST construct
    a file-like object that can be written to in binary mode, and then call the
    `uploader.bundler.Bundler.stream()` method.

13. The uploader program MUST construct a new instance of the
    `metadata.Uploader.Uploader` class. Then, the uploader program MUST
    construct a file-like object that can be read in binary mode, and then call
    the `uploader.bundler.Bundler.upload()` method.

14. Finally, the uploader program MUST verify the result of the ingest by
    calling the `uploader.Uploader.Uploader.getstate()` method. If an
    ingest-related error occurs, then the uploader program MAY repeat the ingest
    operation.
