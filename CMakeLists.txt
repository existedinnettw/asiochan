cmake_minimum_required(VERSION 3.17)
set(ASIOCHAN_VERSION 0.4.3)
project(AsioChan VERSION "${ASIOCHAN_VERSION}")

include(CheckCXXCompilerFlag)

option(ASIOCHAN_USE_STANDALONE_ASIO "Use standalone ASIO instead of Boost.ASIO" OFF)

add_library(asiochan INTERFACE)
add_library(asiochan::asiochan ALIAS asiochan)
target_compile_features(asiochan INTERFACE cxx_std_20)
target_include_directories(asiochan INTERFACE include)

set(COROUTINES_FLAG -fcoroutines)
check_cxx_compiler_flag("${COROUTINES_FLAG}" COMPILER_HAS_COROUTINES_FLAG)
if (COMPILER_HAS_COROUTINES_FLAG)
  target_compile_options(asiochan INTERFACE "${COROUTINES_FLAG}")
endif()

if (ASIOCHAN_USE_STANDALONE_ASIO)
  target_compile_definitions(asiochan INTERFACE ASIOCHAN_USE_STANDALONE_ASIO)
endif()

if (ASIOCHAN_USE_STANDALONE_ASIO)
  find_package(asio REQUIRED CONFIG)
  target_link_libraries(asiochan INTERFACE asio::asio)
else()
  find_package(Boost REQUIRED)
  target_link_libraries(asiochan INTERFACE Boost::headers)
endif()

if (NOT BUILD_TESTING STREQUAL OFF)
  find_package(Threads REQUIRED)
  enable_testing()

  add_subdirectory(examples EXCLUDE_FROM_ALL)
  add_subdirectory(tests)
endif()
