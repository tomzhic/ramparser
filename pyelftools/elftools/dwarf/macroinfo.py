'''
Created on May 30, 2012

@author: pawelp
'''

from ..common.utils import struct_parse
from elftools.dwarf.enums import ENUM_DW_MACINFO
from collections import OrderedDict


class MacroInfo(object):
    '''
    Macro Information parser

    Parses through a macro section and generates
    ordered dictionaries with Macro definitions and undefinitions

    Included macros are also parsed but they are currently
    treated in the same way as local macros - inclusion data is dumped
    '''

    def __init__(self, stream, offset, structs):
        '''
        Initializes the data parser and parses the stream

        stream - .debug_macinfo section stream
        offset - offset within the macro stream (value of DW_AT_macro_info
                                                                attribute)
        structs - DWARFStructs of the current compilation unit
        '''
        self.defines = OrderedDict()
        self.undefines = OrderedDict()
        self.structs = structs
        stream.seek(offset)
        value = struct_parse(structs.Dwarf_dw_form["DW_FORM_udata"], stream)
        if value == ENUM_DW_MACINFO['DW_MACINFO_start_file']:
            self.__parse_file(stream)

    def __parse_file(self, stream):
        '''
        Parses through a macro file block
        '''
        self.__parse_start_file(stream)
        while True:
            value = struct_parse(self.structs.Dwarf_dw_form["DW_FORM_udata"],
                                 stream)
            if value == ENUM_DW_MACINFO['DW_MACINFO_start_file']:
                self.__parse_file(stream)
            elif value == ENUM_DW_MACINFO['DW_MACINFO_define']:
                self.__parse_define(stream)
            elif value == ENUM_DW_MACINFO['DW_MACINFO_undef']:
                self.__parse_undef(stream)
            elif value == ENUM_DW_MACINFO['DW_MACINFO_end_file']:
                break

    def __parse_start_file(self, stream):
        '''
        Parses through a macro file start block
        File data is currently dumped - all macros are treated as local
        '''
        # Dump inclusion data
        struct_parse(self.structs.Dwarf_dw_form["DW_FORM_udata"],
                    stream)
        struct_parse(self.structs.Dwarf_dw_form["DW_FORM_udata"],
                    stream)

    def __parse_define(self, stream):
        '''
        Parses through a define block
        A new macro name,value pair is added to the defines dictionary
        '''
        struct_parse(self.structs.Dwarf_dw_form["DW_FORM_udata"],
                    stream)
        value = struct_parse(self.structs.Dwarf_dw_form["DW_FORM_string"],
                             stream)
        kv = value.split(" ", 1)
        k = kv[0]
        if len(kv) < 2:
            v = ''
        else:
            v = kv[1]
        self.defines[k] = v

    def __parse_undef(self, stream):
        '''
        Parses through a define block
        A new macro name,value pair is added to the undefines dictionary
        '''
        value = struct_parse(self.structs.Dwarf_dw_form["DW_FORM_udata"],
                             stream)
        value = struct_parse(self.structs.Dwarf_dw_form["DW_FORM_string"],
                             stream)
        kv = value.split(" ", 1)
        k = kv[0]
        if len(kv) < 2:
            v = ''
        else:
            v = kv[1]
        self.undefines[k] = v
