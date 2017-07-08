#!/usr/bin/python
__author__ = 'mmcdowell'

import argparse
import os
import sys
import shutil
import crypt
from distutils.dir_util import copy_tree
from itertools import count, ifilterfalse



usage = "usage: {add | delete} -u USERNAME -p PASSWORD(OPTIONAL)"
parser = argparse.ArgumentParser(usage)

subparsers = parser.add_subparsers(help='Use add or delete')

parser_add = subparsers.add_parser('add', help='Add a user')
parser_add.set_defaults(which='add')
parser_add.add_argument("-u", "--user", required=True, dest="user")
parser_add.add_argument("-p", "--password", dest="password", help="Set a password")

parser_delete = subparsers.add_parser('delete', help='Delete a user')
parser_delete.set_defaults(which='delete')
parser_delete.add_argument("-u", "--user", required=True, dest="user")
args = vars(parser.parse_args())

def main():

	if args['which'] == 'add':
		adduser(args['user'],args['password'])

	if args['which'] == 'delete':
		deleteuser(args['user'])

def adduser(user, password):
	data = getdata('/etc/passwd')
	for line in data:
		if line.startswith(user + ':'):
			print "Error: User already exists"
			sys.exit()
		else:
			continue
	guid = getnextid('/etc/group', 2, 1000)
	uid = getnextid('/etc/passwd', 2, 1000)
	homedir = '/home/' + user
	with open('/etc/passwd', 'a') as f:
		f.write(user + ':x:' + str(uid) + ':' + str(guid) + '::' + homedir + ':\n')
	with open('/etc/group', 'a') as f:
		f.write(user + ':x:' + str(guid) + ':\n')
	if password:
		with open('/etc/shadow', 'a') as f:
			f.write(user +':' + crypt.crypt(password,"$6$") + ':17354:0:99999:7:::\n')
	copy_tree('/etc/skel', homedir)
	os.chown(homedir,uid,guid)


def deleteuser(user):
	data = getdata('/etc/passwd')
	for line in data:
		if line.startswith(user + ':'):
			if (os.path.isdir(line.split(':')[5])):
				shutil.rmtree(line.split(':')[5])
	dellines('/etc/passwd', user)
	dellines('/etc/shadow', user)
	dellines('/etc/group', user)


def getdata(file):
	file = open(file, mode="r")
	lines = file.readlines()
	file.close
	return [x.strip() for x in lines]


def dellines(file, user):
	f = open(file,'r')
	lines = f.readlines()
	f.close()
	f = open(file,'w')
	for line in lines:
		if not line.startswith(user + ':'):
			f.write(line)
	f.close()


def getnextid(file, field,start):
	file = getdata(file)
	ids = [i.split(':')[field] for i in file]
	ids = map(int, ids)
	return(next(ifilterfalse(set(ids).__contains__, count(start))))


if __name__=="__main__":
        main()
