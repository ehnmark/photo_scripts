#!/usr/bin/python

import os, sys, hashlib, shutil

def merge(lists):
	import operator
	return reduce(operator.add, lists)

def get_hash(path):
	m = hashlib.md5(open(path).read(1024))
	return m.hexdigest()

def get_files(path):
	paths = map(lambda f: os.path.join(path, f), os.listdir(path))
	files = filter(os.path.isfile, paths)
	dirs = filter(os.path.isdir, paths)
	if len(dirs) > 0: return merge([files] + map(get_files, dirs))
	else: return files

def move_duplicates(paths):
	for path in paths[1:]:
		dup_dir = os.path.join(os.path.dirname(path), "duplicates")
		if not os.path.exists(dup_dir): os.mkdir(dup_dir)
		print "Moving %s to %s" % (path, dup_dir)
		shutil.move(path, dup_dir)

def get_by_hash_lookup(paths):
	def agg(hashes, path):
		key = get_hash(path)
		if not key in hashes: hashes[key] = list()
		hashes[key].append(path)
		return hashes
	return reduce(agg, paths, dict())

def find_duplicates(hashes):
	for key, values in hashes.iteritems():
		if len(values) > 1:
			print "\nPotential duplicates:"
			for path in values: print "\t%s" % path
#			move_duplicates(values)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: %s folder" % sys.argv[0]
		sys.exit(1)
	else:
		paths = get_files(sys.argv[1])
		hashes = get_by_hash_lookup(paths)
		find_duplicates(hashes)
