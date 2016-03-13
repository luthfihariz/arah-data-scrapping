import sys
from dbconfig import db

def main():
	'''Simple script to test db connection'''
	query_result = db.public_transport_lane.find()
	json_data = {'public_transport':query_result.count()}
	print(json_data)	

if __name__ == '__main__':
	sys.exit(main())