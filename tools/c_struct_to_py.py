#!/usr/bin/env python3.9
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
from pycparser import parse_file
from pycparser.c_ast import NodeVisitor, Struct, Union, TypeDecl, ArrayDecl
from pycparser.c_ast import IdentifierType
import sys
import argparse
from pathlib import Path
from warnings import warn
from enum import Enum


c_types_mapping = {"__u8": "ctypes.c_uint8",
                   "__s8": "ctypes.c_int8",
                   "__u16": "ctypes.c_uint16",
                   "__s16": "ctypes.c_int16",
                   "__u32": "ctypes.c_uint32",
                   "__s32": "ctypes.c_int32",
                   "__u64": "ctypes.c_uint64",
                   "__s64": "ctypes.c_int64",
                   }


class StructVisitor(NodeVisitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._structs = []

    def visit_Union(self, node):
        self._structs.append(node)

        for c in node:
            self.visit(c)

    def visit_Struct(self, node):
        self._structs.append(node)

        for c in node:
            self.visit(c)

    def _process_member(self, member):
        if type(member.type) is TypeDecl or type(member.type) is ArrayDecl:
            return self._process_member(member.type)
        elif type(member.type) is Struct or type(member.type) is Union:
            if member.type.name:
                return self.get_nodes(member.type.name)
            else:
                return self._search_struct_members(member.type)
        return []

    def _search_struct_members(self, node):
        code = []
        for decl in node.decls:
            code = self._process_member(decl) + code
        return code

    def get_nodes(self, struct):
        code = []
        for s in self._structs:
            if s.name == struct:
                if not s.decls:
                    # Just a reference to the structure so skip it.
                    continue
                code.insert(0, s)
                code = self._search_struct_members(s) + code
                break
        else:
            warn("'%s' was not found!" % struct)
        return code


class PyCStructure(object):
    class CType(Enum):
        Union = "Union"
        Struct = "Structure"

    def __init__(self, file, name, type, anonymous, parent_struct=None):
        self._file = file
        self._name = name
        self._type = type
        self._anonymous = anonymous
        self._parent_struct = parent_struct
        self._entered = False
        self._fields = {}
        self._anonymous_fields = []
        self._doc_fields = []
        self._anonymous_count = 0

    @property
    def name(self):
        return PyCStructure.c_name_to_py(self._name)

    @staticmethod
    def c_name_to_py(c_name):
        c_name = c_name.replace("v4l2", "V4l2Ioctl")
        pre_ = 0
        while (idx := c_name.find("_")) > -1:
            if idx == 0:
                pre_ += 1
                c_name = c_name[1:]
                continue
            new_name = c_name[0:idx]
            if len(c_name) > idx:
                new_name += c_name[idx+1].upper()
            if len(c_name) > idx+1:
                new_name += c_name[idx+2:]
            c_name = new_name
        c_name = "_" * pre_ + c_name
        return c_name

    def add_field(self, name, type):
        if not self._entered:
            raise Exception("To be used in a with context only!")
        self._fields[name] = type
        self._doc_fields.append(name)

    def add_anonymous_field(self, type_name, fields):
        if not self._entered:
            raise Exception("To be used in a with context only!")
        self._anonymous_count += 1
        name = "_" * self._anonymous_count
        self._anonymous_fields.append(name)
        self._fields[name] = type_name
        self._doc_fields.extend(fields)

    def __enter__(self):
        self._entered = True
        return self

    def __exit__(self, *exc):
        self._entered = False
        if self._parent_struct:
            struct_name = "the {} inside the struct {}".format(
                self._type.name.lower(),
                self._parent_struct,
                )
        else:
            struct_name = f"struct {self._name}"
        header = '''\n\n\nclass {py_name}(ctypes.{c_type}):
    """Implementation of {struct_name} from
    uapi/linux/videodev2.h
    """
'''
        self._file.write(header.format(py_name=self.c_name_to_py(self._name),
                                       c_type=self._type.value,
                                       struct_name=struct_name,
                                       ))

        if self._anonymous_fields:
            self._file.write("    _anonymous_ = (")
            for field in self._anonymous_fields:
                self._file.write(f"'{field}', ")
            self._file.write(")\n")

        self._file.write("    _fields_ = [\n")
        for name, type in self._fields.items():
            self._file.write(f"        ('{name}', {type}),\n")
        self._file.write("        ]")
        if not self._anonymous:
            self._file.write("""
    ###########################################################################
    # These are the fields/attributes that will be automatically
    # created/overwritten in this class. Provided here for documentation
    # purposes only.
    ###########################################################################""")  # noqa E501
            for field in self._doc_fields:
                self._file.write("\n    #: TODO")
                self._file.write(f"\n    {field} = None")


def process_array(array):
    count = int(array.dim.value)
    type_ = array.type
    if type(type_) is ArrayDecl:
        type_, count2 = process_array(type_)
        count *= count2
    elif type(type_) is TypeDecl:
        if type(type_.type) is IdentifierType:
            type_ = c_types_mapping[type_.type.names[0]]
        else:
            if not type_.type.name:
                # TODO Anonymous
                pass
            else:
                type_ = PyCStructure.c_name_to_py(type_.type.name)
    return type_, count


def write_structure(file_, struct, anonymous=False, parent_struct=None):
    fields = []
    with PyCStructure(file_,
                      struct.name,
                      PyCStructure.CType[type(struct).__name__],
                      anonymous,
                      parent_struct) as py:
        for d in struct.decls:
            try:
                d_type = type(d.type)
                if d_type is TypeDecl:
                    name = d.type.declname
                    if type(d.type.type) is IdentifierType:
                        type_ = c_types_mapping[d.type.type.names[0]]
                    else:
                        if not d.type.type.name:
                            if type(d.type.type) is Union:
                                type_suffix = "Union"
                            elif type(d.type.type) is Struct:
                                type_suffix = "Struct"
                            else:
                                raise Exception("Unexpected type!")
                            d.type.type.name = py.name + type_suffix
                            write_structure(file_,
                                            d.type.type,
                                            parent_struct=struct.name)
                            type_ = d.type.type.name
                        else:
                            type_ = PyCStructure.c_name_to_py(d.type.type.name)
                    py.add_field(name, type_)
                    fields.append(name)
                elif d_type is ArrayDecl:
                    name = d.name
                    type_, count = process_array(d.type)
                    type_ = f"{type_} * {count}"
                    if type_ is None:
                        print(2, d)
                    py.add_field(name, type_)
                    fields.append(name)
                elif d_type is Struct or d_type is Union:
                    if d.name is not None:
                        raise Exception("Expected anonymous complex member")
                    if d_type is Union:
                        type_suffix = "Union"
                    elif d_type is Struct:
                        type_suffix = "Struct"
                    else:
                        raise Exception("Unexpected type!")
                    d.type.name = "_" + py.name.removeprefix("V4l2Ioctl") + \
                        type_suffix
                    anonymous_fields = write_structure(
                        file_,
                        d.type,
                        anonymous=True,
                        parent_struct=struct.name)
                    fields.extend(anonymous_fields)
                    py.add_anonymous_field(d.type.name, anonymous_fields)
            except Exception:
                # For debugging purposes.
                print(d)
                raise
    return fields


def dump_python_structures(file_, structs):
    file_.write("import ctypes")
    for struct in structs:
        write_structure(file_, struct)


def main():
    headers_dir = Path(r"/usr/include")
    videodev2 = headers_dir.joinpath("linux", "videodev2.h")
    if not videodev2.exists():
        videodev2 = None

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-f",
                           "--file",
                           help="the header file to parse. [Default: %s]"
                                % videodev2,
                           action="store",
                           metavar="DEVICE",
                           type=Path,
                           default=videodev2,
                           )
    argparser.add_argument("struct",
                           help="the structure to convert.",
                           action="store",
                           metavar="STRUCT",
                           )

    args = argparser.parse_args()

    if not args.file:
        raise FileNotFoundError("Failed to find the linux headers directory")

    if not args.file.exists():
        raise FileNotFoundError("File '" + str(args.file) +
                                "' does not exist.")

    code = parse_file(args.file, use_cpp=True, cpp_path='gcc',
                      cpp_args=[r'-E',
                                # Workaround gcc extensions.
                                r'-D__restrict=restrict',
                                r'-D__attribute__(X)=',
                                r'-D__extension__=',
                                r'-D__inline__=inline',
                                r'-D__signed__=signed',
                                ])
    visitor = StructVisitor()
    visitor.visit(code)

    with open("generated_structures.py", "w") as f:
        dump_python_structures(f, visitor.get_nodes(args.struct))

    return 0


if __name__ == "__main__":
    sys.exit(main())
