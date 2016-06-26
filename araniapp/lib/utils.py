# -*- coding: utf-8 -*-

import os
import errno

flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY

def touch_file(filename):
	try:
	    file_handle = os.open(filename, flags)
	except OSError as e:
	    if e.errno == errno.EEXIST:  # Failed as the file already exists.
	        pass
	    else:  # Something unexpected went wrong so reraise the exception.
	        raise