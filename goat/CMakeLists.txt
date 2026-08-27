cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
project(goat)
if(NOT TARGET Garfield::Garfield)
  find_package(Garfield REQUIRED)
endif()

# ---Define executables----------------------------------------------------------
add_executable(gain gain.C)
target_link_libraries(gain Garfield::Garfield)

add_executable(gasplot gasplot.C)
target_link_libraries(gasplot Garfield::Garfield)

add_executable(eplot eplot.C)
target_link_libraries(eplot Garfield::Garfield)

add_executable(avalancheplot avalancheplot.C)
target_link_libraries(avalancheplot Garfield::Garfield)





