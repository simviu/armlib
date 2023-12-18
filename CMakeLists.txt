project(armlib)
cmake_minimum_required(VERSION 3.4)

SET(CMAKE_CXX_STANDARD 14)

find_package (jsoncpp REQUIRED)
find_package (Eigen3 3.3 REQUIRED NO_MODULE)

set(ENV{armLib_DIR} ${CMAKE_CURRENT_SOURCE_DIR})

include_directories(inc)

add_subdirectory(armCpp)

