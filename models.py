# -*- coding: utf-8 -*-

import time
from webapp2_extras.appengine.auth.models import User
from webapp2_extras.security import generate_password_hash 

from google.appengine.ext import ndb


class User(User):
	
	avatar = ndb.StringProperty(required=False, default="new.png")
	
	def set_password(self, raw_password):
		"""Sets the password for the current user
		:param raw_password:
		The raw password which will be hashed and stored
		"""
		self.password = generate_password_hash(raw_password, length=16)

	@classmethod
	def get_by_auth_token(cls, user_id, token, subject='auth'):
		"""Returns a user object based on a user ID and token.
		:param user_id:
				The user_id of the requesting user.
		:param token:
				The token string to be verified.
		:returns:
				A tuple ``(User, timestamp)``, with a user object and
				the token timestamp, or ``(None, None)`` if both were not found.
		"""
		token_key = cls.token_model.get_key(user_id, subject, token)
		user_key = ndb.Key(cls, user_id)
		valid_token, user = ndb.get_multi([token_key, user_key])
		if valid_token and user:
				timestamp = int(time.mktime(valid_token.created.timetuple()))
				return user, timestamp

		return None, None

