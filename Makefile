MAKEENV_MODULES=*
include .makeenv/makeenv.mak

# this is used in setup.py to indicate that the nose entry point should not be
# installed - if it is installed for test it screws up coverage because the
# yanc module gets imported too early
export YANC_NO_NOSE = 1
