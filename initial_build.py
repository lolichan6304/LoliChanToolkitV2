import os

if not os.path.exists(database):
    os.mkdir(database)
if not os.path.exists(compiled):
    os.mkdir(compiled)