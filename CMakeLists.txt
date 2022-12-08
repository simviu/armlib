project(armlib)
cmake_minimum_required(VERSION 3.4)

SET(CMAKE_CXX_STANDARD 14)

find_package (jsoncpp REQUIRED)
find_package (Eigen3 3.3 REQUIRED NO_MODULE)

#--- Hack for Mac brew
link_directories(/opt/dep/local/lib)

#---- 
message(STATUS "vsnLb_DIR=$ENV{vsnLib_DIR}")

include_directories(
    inc 
    ${EIGEN3_INCLUDE_DIR}
    $ENV{vsnLib_DIR}/inc
    ${JsonCpp_INCLUDE_DIR}
    /opt/dep/local/include
    /usr/include/jsoncpp
    )

#----------- Arm Z1 -------------
if(WITH_ARM_Z1)
    add_subdirectory(dep/z1_sdk)
    include_directories(
        inc 
        dep/z1_sdk/include/unitree_arm_sdk
        ${EIGEN3_INCLUDE_DIR}
        $ENV{vsnLib_DIR}/inc
        ${JsonCpp_INCLUDE_DIR}
        /opt/dep/local/include
        /usr/include/jsoncpp
        )
    link_directories(dep/z1_sdk/lib)
    set(Z1_LINK_LIB Z1_SDK_Linux64)
    add_definitions(-DWITH_ARM_Z1)
endif()

FILE(GLOB  SRC_CORE src/*.cpp)
add_library(armLib ${SRC_CORE} )
target_link_libraries(armLib   
    vsnLib 
    ${Z1_LINK_LIB}
    -fPIC
    pthread
    ${OpenCV_LIBRARIES}
    ${Eigen3_LIBRARY}    
    )

FILE(GLOB  SRC_TEST test/*.cpp)
add_executable(armTest ${SRC_TEST})
target_link_libraries(armTest armLib)

FILE(GLOB  SRC_ARMCMD app/armCmd/*.cpp)
add_executable(armcmd ${SRC_ARMCMD})
target_link_libraries(armcmd armLib)

