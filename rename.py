#!/usr/bin/python

import os, sys, time, datetime

def get_files(path, extensions):
	def normalize_extension(ext):
		if not ext.startswith("."): ext = "." + ext
		return ext.lower()
	normalized = map(normalize_extension, extensions)
	def has_extension(path):
		name, ext = os.path.splitext(path)
		return ext.lower() in normalized
	paths = map(lambda f: os.path.join(path, f), os.listdir(path))
	files = filter(lambda x: os.path.isfile(x) and has_extension(x), paths)
	dirs = filter(os.path.isdir, paths)
	if len(dirs) > 0: return merge([files] + map(get_files, dirs))
	else: return files

def get_creation_time(path):
	ctime = os.path.getctime(path)
	return datetime.datetime.fromtimestamp(ctime)

def get_modification_time(path):
	mtime = os.path.getmtime(path)
	return datetime.datetime.fromtimestamp(mtime)

def get_new_name(path, time):
	base = os.path.dirname(path)
	name, ext = os.path.splitext(path)
	seq = 1
	while True:
		stamp = time.strftime("%Y%m%d")
		candidate = "%s-%d%s" % (stamp, seq, ext)
		full = os.path.join(base, candidate)
		if not os.path.exists(full): return full
		seq = seq + 1
	raise Exception("whoa")

def get_key(item):
	f =lambda x:x.strftime("%y%m%d%H%M%s")
	path, ctime, mtime = item
	return "%s-%s" % (f(ctime), f(mtime))

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: %s dir" % sys.argv[0]
		print " e.g.: %s dir" % sys.argv[0]
		sys.exit(1)
	else:
		paths = get_files(sys.argv[1], ["jpg", "mov", "avi", "png"])
		with_time = map(lambda p: (p, get_creation_time(p), get_modification_time(p)), paths)
		for (path, ctime, mtime) in sorted(with_time, key=get_key):
			new = get_new_name(path, mtime)
			os.rename(path, new)
			print "Renamed %s to %s" % (path, new)
