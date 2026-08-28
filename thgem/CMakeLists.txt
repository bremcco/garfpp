cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
project(goat)
if(NOT TARGET Garfield::Garfield)
  find_package(Garfield REQUIRED)
endif()

# ---Define executables----------------------------------------------------------
add_executable(gain gain.C)
target_link_libraries(gain Garfield::Garfield)






