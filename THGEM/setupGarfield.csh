# Setup a minimal environment to build and run the examples

setenv GARFIELD_INSTALL /cvmfs/sft.cern.ch/lcg/releases/Garfield++/961fb7bd-e90a3/x86_64-el9-gcc13-opt
setenv CMAKE_PREFIX_PATH /cvmfs/sft.cern.ch/lcg/releases/Garfield++/961fb7bd-e90a3/x86_64-el9-gcc13-opt:${CMAKE_PREFIX_PATH}
setenv HEED_DATABASE ${GARFIELD_INSTALL}/share/Heed/database
setenv LD_LIBRARY_PATH ${GARFIELD_INSTALL}/lib64:${LD_LIBRARY_PATH}
setenv PYTHONPATH ${GARFIELD_INSTALL}/lib64/python3.9/site-packages/:${PYTHONPATH}
