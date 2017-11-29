# Pacifica Python Uploader
[![Build Status](https://travis-ci.org/pacifica/pacifica-python-uploader.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-python-uploader)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-python-uploader/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-python-uploader)
[![Test Coverage](https://codeclimate.com/github/pacifica/pacifica-python-uploader/badges/coverage.svg)](https://codeclimate.com/github/pacifica/pacifica-python-uploader/coverage)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-python-uploader/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-python-uploader)

Python library to handle bundling, metadata and uploading files to an ingester.

## Object Reference

The following objects and short descriptions are available as follows.

### MetaData

The `MetaData` module handles the required metadata needed to create a successful
upload. The logic for encoding and decoding into JSON is also present in the library.
This object must encode into JSON compatible with the ingest service.

#### MetaData Object

The `MetaData()` object is the upperlevel object storing all the required upload and
file metadata. This object is currently a child of `list` to allow for easy integration
with other python objects. Additions to the `list` methods have been made to index off
the `metaID` attribute in the `MetaObj` class.

#### MetaObj Object

The `MetaObj()` object is an instance of a single piece of uploaded metadata. This
means that it's not file metadata. The `MetaObj()` object allows for references
between attributes of the class and allows for updates to occure at the `MetaData()`
layer. This is currently implemented as a `namedtuple` for easy integration with
other python objects.

#### FileObj Object

The `FileObj()` object is an instance of a single files metadata. This is meant to
be appended to the `MetaData()` object when an upload occures. The attributes of the
`FileObj()` directly match with the file object stored in
[Pacifica Metadata](https://github.com/pacifica/pacifica-metadata)
so please refer to that for what the
values are supposed to be. This is currently implemented as a `namedtuple` for easy
integration with other python objects.

#### Metadata Decode

The `metadata_decode()` method decodes a JSON string into a `MetaData()` object
filled with `MetaObj()` and `FileObj()` objects. The method returns the resulting
`MetaData()` object.

#### Metadata Encoding

The `metadata_encode()` method encodes a `MetaData()` object with a number of
`MetaObj()` and `FileObj()` objects into a JSON string. The method returns the
resulting JSON string.

#### Json

The `Json` module encapsulates the JSON parsing logic into a common library.
This module contains the general generators for creating `json.Encoder` and
`json.Decoder` child classes.

##### NamedTuple Encoders and Decoders

The `generate_namedtuple_encoder` and `generate_namedtuple_decoder` methods
return `json.Encoder` and `json.Decoder` child classes, respectively. These
classes encode or decode a child class of `collections.namedtuple`.

#### Policy

This module contains all the logic to generate and execute queiries against
the Pacifica Policy service.

##### PolicyQueryData

This `namedtuple` contains the data required to generate a valid Policy
service query.

##### PolicyQuery

This object contains a `PolicyQueryData` object, mangles the object to send
it to the Policy service. This object also has logic to pull the endpoint for
the Policy service from the environment or constructor keyword arguments.
Another requirement for this object is to return the results from a query to
the calling object.

This object also contains the method to validate the completed `MetaData`
object against the ingest endpoint. Valid json is returned containing the
success or failure of the metadata to ingest.

#### MetaUpdate

This module has all the `MetaData` update code for determining parents and
children to update when values get updated.

##### MetaUpdate

The `MetaUpdate` class inherits from the `MetaData` class and provides methods
for querying the policy server to get results from the metadata and update
those results in the `MetaData` object.

### Bundler

This module defines a streaming bundler that allows one to stream the data and
metadata to a file descriptor. The file descriptor is open for write binary
and provides a single pass over the data files provided.

#### Bundler

The `Bundler` class provides a method called `stream()` to send the bundle to
a file descriptor. The class is created using an array of hashes that define
the arguments to `tarfile.TarFile.gettarinfo()`. However, the `arcname` argument
is required. The `stream()` method is blocking. However, it does have a callback
argument that sets up a thread to get percent complete from the stream thread
as it's processing.

### Uploader

This module provides the basic upload functionality to interface with the
ingest service.

#### Uploader

The `Uploader` class provides the interface for handling connections to the
ingest service. There are two methods `upload()` and `getstate()`. The
`upload()` method takes a file like object open for read binary and returns
a job_id for that upload. The `getstate()` method takes a job_id and returns
a json object as defined by the ingest API for getting job status.

## Uploader Expectations and Application Flows

There are general expectations that cover how an uploader is supposed to
interact with the services and objects above. The following section we will
discuss some program flows in general and how it might apply to different
uploader implementations.

### Uploader Program Flow

The uploader program should start by building a `MetaUpdate` object which may
contain some holes (`MetaObj` objects with no values). This object may not
contain any `FileObj` objects. This object can be validated at anytime to
determine completness, but must be valid prior to bundling.

The uploader program should use the `displayType` attribute of the `MetaObj`
to determine how the user should select the `value` attribute of that
`MetaObj`. The values of the `displayType` are arbitrary and should be defined
by the uploader.

The uploader program should populate the `query_results` for each hole in
`MetaData` by calling `MetaUpdate.query_results()`. The `query_results`
attribute is an array of objects that should be rendered by the
`displayFormat` attribute and displayed to the user. The uploader program may
call `query_results()` for `MetaObj` objects that already have values. In
Python, using string formatting is sufficient, but more complicated formatting
(i.e. Cheetah) can also be used. The specifics of how `displayFormat` is used
to render `query_results` are defined by the uploader.

If the uploader program has more than one hole and there exist dependencies
between those holes. The program must not fail if there isn't any
`query_results` to render. This is common in more complicated metadata query
models and the uploader must handle this.

When the uploader program is ready for a value to be selected. The uploader
program must set the `value` attribute in the respective `MetaObj` to the
`valueField` attribute of the object selected. The uploader must then call
`update_parents()` with the `MetaObj` selected. This will update the `value`
attribute for many `MetaObj` objects and the updated `MetaUpdate` object should
be rendered and presented to the user as previously discussed.

The uploader program must then verify `MetaUpdate.is_valid()` returns true.
If not the uploader program must repeat the previous paragraph until it does.
This is open ended and depends highly on properly formatting the `MetaData`
object with well organized metadata.

The uploader program should then call the `PolicyQuery.valid_metadata()` method
to validate the completed metadata prior to upload. This prevents the uploader
from uploading metadata not valid by the ingest policy. The uploader program
should then parse the result for success then proceed.

When the uploader program is ready to bundle the data. The uploader program
must build an array of objects that represent the attributes of a `tar.TarInfo`
object. Additionally, the object must have a `fileobj` attribute which is an
object the bundler will call the `read()` method like a standard open file
object.

The uploader program must then create a `Bundler` object with the `MetaUpdate`
and the array of `tar.TarInfo` objects as stated in the previous paragraph.
The uploader program must then setup a writable file object and call the
`stream()` method.

The uploader program must then create a `Uploader` object. The uploader program
must then setup a file-like object open for read and call the `upload()` method.

The two file-like objects are open for read and write for upload and bundle
respectively intentionally as this allows for setting up pipes between multiple
processes to stream the data without keeping a local copy.

The uploader must then verify the ingest has succeeded in ingest by calling
`getstate()` and parsing the ingest response. If there is an error the uploader
may perform the upload again.
