#!/usr/bin/python

'''
Define Reviewer information in the spdx object.
'''
import MySQLdb
import datetime

class reviewerInfo:
	
	def __init__( self):
		self.reviewer 		= ""
		self.reviewDate 	= datetime.datetime.now()
		self.reviewComment 	= ""

	def getReviewerInfo(self, reviewer_id, dbHost, dbUserName, dbUserPass, dbName):
		'''
		gets reviewerInfo from database
		'''
		with MySQLdb.connect(host = dbHost, user = dbUserName, passwd = dbUserPass, db = dbName) as dbCursor:
			sqlCommand = """SELECT * FROM reviewers WHERE id = ?"""
			dbCursor.execute(sqlCommand, (reviewer_id))
			
			queryReturn = dbCursor.fetchone()

			self.reviewer		= queryReturn.reviewer
			self.reviewDate		= queryReturn.reviewer_date
			self.reviewComment	= queryReturn.reviewer_comment
	
	def insertReviewerInfo(self, spdx_doc_id, dbHost, dbUserName, dbUserPass, dbName):
		'''
		inserts reviewerInfo into database
		'''
		with MySQLdb.connect(host = dbHost, user = dbUserName, passwd = dbUserPass, db = dbName) as dbCursor:
			'''Get id of reviewer'''
			sqlCommand = "SHOW TABLE STATUS LIKE 'reviewers'"
			dbCursor.execute(sqlCommand)
			reviewerId = dbCursor.fetchone()[10]

			sqlCommand   = """INSERT INTO reviewers (reviewer, reviewer_date, reviewer_comment, spdx_doc_id, created_at, updated_at)
 					  VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"""
			dbCursor.execute(sqlCommand, (self.reviewer, self.reviewDate, self.reviewComment, spdx_doc_id))
		
		return reviewerId
			
	def outputReviewerInfo_TAG(self):
		'''
		outputs reviewerInfo to stdout
		'''
		if self.reviewer != "":
			print "Reviewer: " + self.reviewer
		if self.reviewer != "" and self.reviewDate != "":
			print "ReviewDate: " + self.reviewDate
		if self.reviewComment != "":
			print "ReviewComment: <text>" + self.reviewComment + "</text>"
