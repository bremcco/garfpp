# Setup a minimal environment to build and run the examples

export GARFIELD_INSTALL=/cvmfs/sft.cern.ch/lcg/releases/Garfield++/961fb7bd-e90a3/x86_64-el9-gcc13-opt
export CMAKE_PREFIX_PATH=/cvmfs/sft.cern.ch/lcg/releases/Garfield++/961fb7bd-e90a3/x86_64-el9-gcc13-opt:$CMAKE_PREFIX_PATH
export HEED_DATABASE=$GARFIELD_INSTALL/share/Heed/database
export LD_LIBRARY_PATH=$GARFIELD_INSTALL/lib64:$LD_LIBRARY_PATH
export PYTHONPATH=$GARFIELD_INSTALL/lib64/python3.9/site-packages/:$PYTHONPATH
