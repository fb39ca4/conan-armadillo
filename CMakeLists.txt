
# Copyright 2008-2016 Conrad Sanderson (http://conradsanderson.id.au)
# Copyright 2008-2016 National ICT Australia (NICTA)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------



cmake_minimum_required(VERSION 2.8.12 FATAL_ERROR)
project(armadillo CXX C)

include(${CMAKE_CURRENT_SOURCE_DIR}/../conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

include(CheckIncludeFileCXX)
include(CheckLibraryExists)

## Set ARMA_USE_WRAPPER to false if you're getting linking errors when compiling your programs,
## or if you prefer to directly link with BLAS and/or LAPACK.
## You will then need to link your programs with -lblas -llapack instead of -larmadillo
## If you're using OpenBLAS, link your programs with -lopenblas -llapack instead of -larmadillo

set(ARMA_USE_WRAPPER true)


# the settings below will be automatically configured by the rest of this script

set(ARMA_USE_LAPACK           false)
set(ARMA_USE_BLAS             false)
set(ARMA_USE_ATLAS            false)
set(ARMA_USE_HDF5_ALT         false)
set(ARMA_USE_ARPACK           false)
set(ARMA_USE_EXTERN_CXX11_RNG false)
set(ARMA_USE_SUPERLU          false)  # Caveat: only SuperLU version 5.x can be used!

## NOTE: OpenBLAS appears to have its own LAPACK functions,
## NOTE: but on some systems the installed version of OpenBLAS
## NOTE: has been modified not to include LAPACK functions.
## NOTE: As the presence of LAPACK functions in OpenBLAS can't be guaranteed,
## NOTE: this installer script requires LAPACK to be present on the system
## NOTE: in order to enable the use of LAPACK functions by Armadillo.
## NOTE: This installer will link with OpenBLAS first,
## NOTE: so if a full version of OpenBLAS is actually present on the system,
## NOTE: the linker should make use of LAPACK functions from OpenBLAS
## NOTE: instead of standard LAPACK.


## extract version from sources

set(ARMA_VERSION_FILE_NAME "${PROJECT_SOURCE_DIR}/include/armadillo_bits/arma_version.hpp")

if(NOT EXISTS ${ARMA_VERSION_FILE_NAME})
  message(FATAL_ERROR "Can't read ${ARMA_VERSION_FILE_NAME}")
endif()

file(READ ${ARMA_VERSION_FILE_NAME} ARMA_VERSION_FILE_CONTENTS)
string(REGEX REPLACE ".*#define ARMA_VERSION_MAJOR ([0-9]+).*" "\\1" ARMA_VERSION_MAJOR "${ARMA_VERSION_FILE_CONTENTS}")
string(REGEX REPLACE ".*#define ARMA_VERSION_MINOR ([0-9]+).*" "\\1" ARMA_VERSION_MINOR "${ARMA_VERSION_FILE_CONTENTS}")
string(REGEX REPLACE ".*#define ARMA_VERSION_PATCH ([0-9]+).*" "\\1" ARMA_VERSION_PATCH "${ARMA_VERSION_FILE_CONTENTS}")

message(STATUS "Configuring Armadillo ${ARMA_VERSION_MAJOR}.${ARMA_VERSION_MINOR}.${ARMA_VERSION_PATCH}")

# deprecated options
set(INSTALL_LIB_DIR     "" CACHE STRING "deprecated; use CMAKE_INSTALL_LIBDIR instead")
set(INSTALL_INCLUDE_DIR "" CACHE STRING "deprecated; use CMAKE_INSTALL_INCLUDEDIR instead")
set(INSTALL_DATA_DIR    "" CACHE STRING "deprecated; use CMAKE_INSTALL_DATADIR instead")
set(INSTALL_BIN_DIR     "" CACHE STRING "deprecated; use CMAKE_INSTALL_BINDIR instead")

if(INSTALL_LIB_DIR)
  message(STATUS "*** INSTALL_LIB_DIR is deprecated; use CMAKE_INSTALL_LIBDIR instead")
  set(CMAKE_INSTALL_LIBDIR "${INSTALL_LIB_DIR}")
  GNUInstallDirs_get_absolute_install_dir(CMAKE_INSTALL_FULL_LIBDIR CMAKE_INSTALL_LIBDIR)
endif()

if(INSTALL_INCLUDE_DIR)
  message(STATUS "*** INSTALL_INCLUDE_DIR is deprecated; use CMAKE_INSTALL_INCLUDEDIR instead")
  set(CMAKE_INSTALL_INCLUDEDIR "${INSTALL_INCLUDE_DIR}")
  GNUInstallDirs_get_absolute_install_dir(CMAKE_INSTALL_FULL_INCLUDEDIR CMAKE_INSTALL_INCLUDEDIR)
endif()

if(INSTALL_DATA_DIR)
  message(STATUS "*** INSTALL_DATA_DIR is deprecated; use CMAKE_INSTALL_DATADIR instead")
  set(CMAKE_INSTALL_DATADIR "${INSTALL_DATA_DIR}")
endif()

if(INSTALL_BIN_DIR)
  message(STATUS "*** INSTALL_BIN_DIR is deprecated; use CMAKE_INSTALL_BINDIR instead")
  set(CMAKE_INSTALL_BINDIR "${INSTALL_BIN_DIR}")
endif()


if(MSVC)
  option(BUILD_SHARED_LIBS "build shared library" OFF)
else()
  option(BUILD_SHARED_LIBS "build shared library" ON)
endif()

message(STATUS "CMAKE_SYSTEM_NAME          = ${CMAKE_SYSTEM_NAME}"         )
message(STATUS "CMAKE_CXX_COMPILER_ID      = ${CMAKE_CXX_COMPILER_ID}"     )
message(STATUS "CMAKE_CXX_COMPILER_VERSION = ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "CMAKE_COMPILER_IS_GNUCXX   = ${CMAKE_COMPILER_IS_GNUCXX}"  )
message(STATUS "BUILD_SHARED_LIBS          = ${BUILD_SHARED_LIBS}"         )


message(STATUS "")
message(STATUS "*** Armadillo wrapper library will use the following libraries:")
message(STATUS "*** ARMA_LIBS = ${CONAN_LIBS}")
message(STATUS "")


if(DEFINED CMAKE_CXX_COMPILER_ID AND DEFINED CMAKE_CXX_COMPILER_VERSION)
  if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND NOT ${CMAKE_CXX_COMPILER_VERSION} VERSION_LESS 4.8.3)
    set(ARMA_USE_EXTERN_CXX11_RNG true)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
    message(STATUS "Detected gcc 4.8.3 or later. Added '-std=c++11' to compiler flags")
  endif()
endif()


message(STATUS "Copying ${PROJECT_SOURCE_DIR}/include/ to ${PROJECT_BINARY_DIR}/tmp/include/")
file(COPY ${PROJECT_SOURCE_DIR}/include/ DESTINATION ${PROJECT_BINARY_DIR}/tmp/include/)

message(STATUS "Generating ${PROJECT_BINARY_DIR}/tmp/include/config.hpp")
configure_file(${PROJECT_BINARY_DIR}/tmp/include/armadillo_bits/config.hpp.cmake ${PROJECT_BINARY_DIR}/tmp/include/armadillo_bits/config.hpp)

message(STATUS "Generating ${PROJECT_SOURCE_DIR}/examples/Makefile")
configure_file(${PROJECT_SOURCE_DIR}/examples/Makefile.cmake ${PROJECT_SOURCE_DIR}/examples/Makefile)


include_directories(${PROJECT_BINARY_DIR}/tmp/include/ ${CMAKE_REQUIRED_INCLUDES})


## work around a silly limitation in Mac OS X
if(APPLE)
  if(${ARMA_VERSION_MINOR} GREATER 99)
    math(EXPR ARMA_VERSION_MINOR_ALT "${ARMA_VERSION_MINOR} / 10")
  else()
    set(ARMA_VERSION_MINOR_ALT ${ARMA_VERSION_MINOR})
  endif()
else()
  set(ARMA_VERSION_MINOR_ALT ${ARMA_VERSION_MINOR})
endif()


## necessary when linking with Intel MKL on Linux systems
if(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
  set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,--no-as-needed")
endif()


if(CMAKE_COMPILER_IS_GNUCXX)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2")
endif()

message(STATUS "CMAKE_CXX_FLAGS           = ${CMAKE_CXX_FLAGS}"          )
message(STATUS "CMAKE_SHARED_LINKER_FLAGS = ${CMAKE_SHARED_LINKER_FLAGS}")
message(STATUS "CMAKE_REQUIRED_INCLUDES   = ${CMAKE_REQUIRED_INCLUDES}"  )


add_library( armadillo STATIC ${PROJECT_SOURCE_DIR}/src/wrapper.cpp )
target_link_libraries( armadillo ${CONAN_LIBS} )
target_include_directories(armadillo INTERFACE $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include> $<INSTALL_INTERFACE:include>)
set_target_properties(armadillo PROPERTIES VERSION ${ARMA_VERSION_MAJOR}.${ARMA_VERSION_MINOR_ALT}.${ARMA_VERSION_PATCH} SOVERSION ${ARMA_VERSION_MAJOR})

