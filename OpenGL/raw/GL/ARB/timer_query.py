'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_timer_query'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_timer_query',error_checker=_errors._error_checker)
GL_TIMESTAMP=_C('GL_TIMESTAMP',0x8E28)
GL_TIME_ELAPSED=_C('GL_TIME_ELAPSED',0x88BF)
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,arrays.GLint64Array)
def glGetQueryObjecti64v(id,pname,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum,arrays.GLuint64Array)
def glGetQueryObjectui64v(id,pname,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLenum)
def glQueryCounter(id,target):pass
