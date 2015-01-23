del srbb /S/F/Q
..\Scripts\pcreate -t srbb_stack --overwrite .
..\Scripts\pip install -e .
..\Scripts\initialize_core_db dev.ini
..\Scripts\pserve.exe --reload dev.ini