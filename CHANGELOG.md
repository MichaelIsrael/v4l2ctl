# v4l2ctl change log

## 0.1a5
* Fix issue #1 (importing from utils)

## 0.1a4
* Support cropping rectangles (querying, getting and setting).
* Support setting and getting formats.
* Add tool to auto generate Python implementations of C structures.
* V4l2Device now implements the io.IOBase interface (no I/O features are supported yet).

## 0.1a3
* Reading supported frame sizes.
* Reading supported frame intervals.

## 0.1a2
* First (internal) support for write ioctls.
* Getting a list of available v4l2 devices.
* Reading the supported formats.

## 0.1a1
* First release.
* Basic functionalities of create a v4l2 device.
* Reading card and driver names.
* Reading device capabilities.
