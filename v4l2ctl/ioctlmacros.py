###############################################################################
# Copyright 2020, Michael Israel
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by
# the European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
#   https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" basis, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence.
###############################################################################
"""
This is a plain semi-automated python port of asm-generic/ioctl.h.

*(Based on linux-libc-dev 5.6.14-1)*

.. note::
    **From asm-generic/ioctl.h:**

    ioctl command encoding: 32 bits total, command in lower 16 bits,
    size of the parameter structure in the lower 14 bits of the
    upper 16 bits.
    Encoding the size of the parameter structure in the ioctl request
    is useful for catching programs compiled with old versions
    and to avoid overwriting user space outside the user buffer area.
    The highest 2 bits are reserved for indicating the "access mode".
    NOTE: This limits the max parameter size to 16kB -1 !

    The following is for compatibility across the various Linux
    platforms.  The generic ioctl numbering scheme doesn't really enforce
    a type field.  De facto, however, the top 8 bits of the lower 16
    bits are indeed used as a type field, so we might just as well make
    this explicit here.  Please be sure to use the decoding macros
    below from now on.
"""
from ctypes import sizeof


_IOC_NRBITS = 8
_IOC_TYPEBITS = 8

"""
 * Let any architecture override either of the following before
 * including this file.
"""
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRMASK = ((1 << _IOC_NRBITS)-1)
_IOC_TYPEMASK = ((1 << _IOC_TYPEBITS)-1)
_IOC_SIZEMASK = ((1 << _IOC_SIZEBITS)-1)
_IOC_DIRMASK = ((1 << _IOC_DIRBITS)-1)

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = (_IOC_NRSHIFT+_IOC_NRBITS)
_IOC_SIZESHIFT = (_IOC_TYPESHIFT+_IOC_TYPEBITS)
_IOC_DIRSHIFT = (_IOC_SIZESHIFT+_IOC_SIZEBITS)

"""
 * Direction bits, which any architecture can choose to override
 * before including this file.
 *
 * NOTE: _IOC_WRITE means userland is writing and kernel is
 * reading. _IOC_READ means userland is reading and kernel is writing.
"""
_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2


def _IOC(dir_, type_, nr, size):
    return (((dir_) << _IOC_DIRSHIFT) |
            (ord(type_) << _IOC_TYPESHIFT) |
            ((nr) << _IOC_NRSHIFT) |
            ((size) << _IOC_SIZESHIFT)
            )


def _IOC_TYPECHECK(t):
    return (sizeof(t))


"""
 * Used to create numbers.
 *
 * NOTE: _IOW means userland is writing and kernel is reading. _IOR
 * means userland is reading and kernel is writing.
"""


def _IO(type_, nr):
    return _IOC(_IOC_NONE, (type_), (nr), 0)


def _IOR(type_, nr, size):
    return _IOC(_IOC_READ, (type_), (nr), (_IOC_TYPECHECK(size)))


def _IOW(type_, nr, size):
    return _IOC(_IOC_WRITE, (type_), (nr), (_IOC_TYPECHECK(size)))


def _IOWR(type_, nr, size):
    return _IOC(_IOC_READ | _IOC_WRITE, (type_), (nr), (_IOC_TYPECHECK(size)))


def _IOR_BAD(type_, nr, size):
    return _IOC(_IOC_READ, (type_), (nr), sizeof(size))


def _IOW_BAD(type_, nr, size):
    return _IOC(_IOC_WRITE, (type_), (nr), sizeof(size))


def _IOWR_BAD(type_, nr, size):
    return _IOC(_IOC_READ | _IOC_WRITE, (type_), (nr), sizeof(size))


""" used to decode ioctl numbers.. """


def _IOC_DIR(nr):
    return (((nr) >> _IOC_DIRSHIFT) & _IOC_DIRMASK)


def _IOC_TYPE(nr):
    return (((nr) >> _IOC_TYPESHIFT) & _IOC_TYPEMASK)


def _IOC_NR(nr):
    return (((nr) >> _IOC_NRSHIFT) & _IOC_NRMASK)


def _IOC_SIZE(nr):
    return (((nr) >> _IOC_SIZESHIFT) & _IOC_SIZEMASK)


""" ...and for the drivers/sound files... """
IOC_IN = (_IOC_WRITE << _IOC_DIRSHIFT)
IOC_OUT = (_IOC_READ << _IOC_DIRSHIFT)
IOC_INOUT = ((_IOC_WRITE | _IOC_READ) << _IOC_DIRSHIFT)
IOCSIZE_MASK = (_IOC_SIZEMASK << _IOC_SIZESHIFT)
IOCSIZE_SHIFT = (_IOC_SIZESHIFT)
