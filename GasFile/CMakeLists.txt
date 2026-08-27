cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
project(GasFile)
if(NOT TARGET Garfield::Garfield)
  find_package(Garfield REQUIRED)
endif()

# ---Define executables----------------------------------------------------------
add_executable(generate generate.C)
target_link_libraries(generate Garfield::Garfield)

add_executable(penning penning.C)
target_link_libraries(penning Garfield::Garfield)




