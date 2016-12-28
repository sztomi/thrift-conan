cmake_minimum_required(VERSION 3.0.0)
project(thrift_test)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(hello_server
    src/Hello.cpp
    src/hello_constants.cpp
    src/Hello_server.skeleton.cpp
    src/hello_types.cpp)

target_link_libraries(hello_server ${CONAN_LIBS})
set_target_properties(
        hello_server
        PROPERTIES
        CXX_STANDARD 11)
