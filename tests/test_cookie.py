#!/usr/bin/python3
"""
Testing the supposedly beautiful command line parsing 
@author chairs
"""
import unittest
from cookie.cookie import Cookie


app = Cookie(__name__, notes=('simple', 'test'))

class TestCookie (unittest.TestCase):

	def test_notes (self):
		"""
		Ensure that the notes feature of
		the Cookie class is in working order
		"""
		self.assertEqual(('simple', 'test'), app.notes)

	def test_decorator (self):
		"""
		Ensure that the decorator is working as expected
		"""
		@app.get_args
		def test_function (name=str()): 
			return 'Hello %s!' % name

		app.run(test_function)
		assert 'Usage: ' in app.outline

if __name__ == '__main__':
	unittest.main()

