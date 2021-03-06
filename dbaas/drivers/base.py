# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
from django.utils.translation import ugettext_lazy as _
from django_services.service.exceptions import InternalException

LOG = logging.getLogger(__name__)

__all__ = ['GenericDriverError', 'ConnectionError',
           'AuthenticationError', 'DatabaseAlreadyExists', 'CredentialAlreadyExists', 'InvalidCredential',
           'BaseDriver', 'DatabaseStatus', 'DatabaseInfraStatus', 'DatabaseDoesNotExist']


class GenericDriverError(InternalException):
    """ Exception raises when any kind of problem happens when executing operations on databaseinfra """

    def __init__(self, message=None):
        self.message = message

    def __unicode__(self):
        return "%s: %s" % (type(self).__name__, self.message)

    def __str__(self):
        return b"%s: %s" % (type(self).__name__, self.message)

    def __repr__(self):
        return b"%s: %s" % (type(self).__name__, self.message)


class ConnectionError(GenericDriverError):
    """ Raised when there is any problem to connect on databaseinfra """
    pass


class AuthenticationError(ConnectionError):
    """ Raised when there is any problem authenticating on databaseinfra """
    pass


class DatabaseAlreadyExists(InternalException):
    """ Raised when database already exists in datainfra """
    pass


class DatabaseDoesNotExist(InternalException):
    """ Raised when there is no requested database """
    pass


class CredentialAlreadyExists(InternalException):
    """ Raised when credential already exists in database """
    pass


class InvalidCredential(InternalException):
    """ Raised when credential no more exists in database """
    pass


class BaseDriver(object):
    """
    BaseDriver interface
    """
    ENV_CONNECTION = 'DATABASEINFRA_CONNECTION'

    # List of reserved database names for this driver that cannot be used
    RESERVED_DATABASES_NAME = []

    # must be overwritten by subclasses
    default_port = 0

    def __init__(self, *args, **kwargs):

        if 'databaseinfra' in kwargs:
            self.databaseinfra = kwargs.get('databaseinfra')
        else:
            raise TypeError(_("DatabaseInfra is not defined"))

    def test_connection(self, credential=None):
        """ Tests the connection to the database """
        raise NotImplementedError()

    def get_connection(self, database=None):
        """ Connection string for this databaseinfra """
        raise NotImplementedError()

    def get_user(self):
        return self.databaseinfra.user

    def get_password(self):
        return self.databaseinfra.password

    def check_status(self):
        """ Check if databaseinfra is working. If not working, raises subclass of GenericDriverError """
        raise NotImplementedError()

    def info(self):
        """ Returns a mapping with same attributes of databaseinfra """
        raise NotImplementedError()

    def create_user(self, credential, roles=None):
        raise NotImplementedError()

    def update_user(self, credential):
        raise NotImplementedError()

    def remove_user(self, credential):
        raise NotImplementedError()

    def list_users(self, instance=None):
        """
        this method should return a list of the users in the instance
        Ex.: ["mary", "john", "michael"]
        """
        raise NotImplementedError()

    def create_database(self, database):
        raise NotImplementedError()

    def remove_database(self, database):
        raise NotImplementedError()

    def list_databases(self):
        """
        list databases in a databaseinfra
        this method should return a list of the databases names in the instance
        Ex.: ["mary", "john", "michael"]
        """
        raise NotImplementedError()

    def import_databases(self, databaseinfra):
        """import databases already created in a databaseinfra"""
        raise NotImplementedError()




class DatabaseStatus(object):

    def __init__(self, database_model):
        self.database_model = database_model
        self.used_size_in_bytes = -1
        self.total_size_in_bytes = -1
        self.is_alive = False

    @property
    def name(self):
        return self.database_model.name


class DatabaseInfraStatus(object):

    def __init__(self, databaseinfra_model):
        self.databaseinfra_model = databaseinfra_model
        self.version = None
        self.used_size_in_bytes = -1
        self.databases_status = {}

    def get_database_status(self, database_name):
        """ Return DatabaseStatus of one specific database """
        return self.databases_status.get(database_name, None)
