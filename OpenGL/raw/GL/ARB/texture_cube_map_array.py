'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_texture_cube_map_array'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_texture_cube_map_array',error_checker=_errors._error_checker)
GL_INT_SAMPLER_CUBE_MAP_ARRAY_ARB=_C('GL_INT_SAMPLER_CUBE_MAP_ARRAY_ARB',0x900E)
GL_PROXY_TEXTURE_CUBE_MAP_ARRAY_ARB=_C('GL_PROXY_TEXTURE_CUBE_MAP_ARRAY_ARB',0x900B)
GL_SAMPLER_CUBE_MAP_ARRAY_ARB=_C('GL_SAMPLER_CUBE_MAP_ARRAY_ARB',0x900C)
GL_SAMPLER_CUBE_MAP_ARRAY_SHADOW_ARB=_C('GL_SAMPLER_CUBE_MAP_ARRAY_SHADOW_ARB',0x900D)
GL_TEXTURE_BINDING_CUBE_MAP_ARRAY_ARB=_C('GL_TEXTURE_BINDING_CUBE_MAP_ARRAY_ARB',0x900A)
GL_TEXTURE_CUBE_MAP_ARRAY_ARB=_C('GL_TEXTURE_CUBE_MAP_ARRAY_ARB',0x9009)
GL_UNSIGNED_INT_SAMPLER_CUBE_MAP_ARRAY_ARB=_C('GL_UNSIGNED_INT_SAMPLER_CUBE_MAP_ARRAY_ARB',0x900F)

