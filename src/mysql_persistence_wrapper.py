"""Implements a MySQL Persistence Wrapper"""

from persistence_wrapper_interface import PersistenceWrapperInterface
from mysql import connector

class MySQLPersistenceWrapper(PersistenceWrapperInterface):
	"""Implements MySQL Persistance Wrapper"""

	def __init__(self):
		"""Initializes """
		# Constants
		self.SELECT_ALL_INVENTORIES = 'SELECT id, name, description FROM inventories'
		self.INSERT = 'INSERT INTO items (inventory_id, item, count) VALUES(%s, %s, %s)'
		self.SELECT_ALL_ITEMS_FOR_INVENTORY_ID = 'SELECT id, inventory_id, item, count FROM items WHERE inventory_id = %s'

		# Database Configuration Constants
		self.DB_CONFIG = {}
		self.DB_CONFIG['database'] = 'home_inventory'
		self.DB_CONFIG['user'] = 'home_inventory_user'
		self.DB_CONFIG['host'] = '127.0.0.1'
		self.DB_CONFIG['port'] = 3306

		# Database Connection
		self._db_connection = self._initialize_database_connection(self.DB_CONFIG)


	def get_all_inventories(self):
		"""Returns a list of all rows in the inventories table"""
		cursor = None
		try:
			cursor = self._db_connection.cursor()
			cursor.execute(self.SELECT_ALL_INVENTORIES)
			results = cursor.fetchall()
		except Exception as e:
			print(f'Exception in persistance wrapper: {e}')
		return results


	def get_items_for_inventory(self, inventory_id):
		"""Returns a list of all items for given inventory id"""
		cursor = None
		try:
			cursor = self._db_connection.cursor()
			cursor.execute(self.SELECT_ALL_ITEMS_FOR_INVENTORY_ID, ([inventory_id]))
			results = cursor.fetchall()
		except Exception as e:
			print(f'Exception in persistance wrapper: {e}')
		return results


	def create_inventory(self, name: str, description: str, date: str):
		"""Insert new row into inventories table."""
		try:
			cursor = self._db_connection.cursor()
			cursor.execute(
				"INSERT INTO inventories (name, description, date) VALUES (%s, %s, %s)",
                (name, description, date),
			)
			self._db_connection.commit()
			return cursor.lastrowid
		except Exception as e:
			print(f"Exception in create inevntory: {e}")
			return None


	def create_item(self, inventory_id: int, item: str, count: int):
		"""Insert new row into items table for given inventory id"""
		try:
			cursor = self._db_connection.cursor()
			cursor.execute(
                "INSERT INTO items (inventory_id, item, count) VALUES (%s, %s, %s)",
                (inventory_id, item, count),
            )
			self._db_connection.commit()
			return cursor.lastrowid
		except Exception as e:
			print(f"Exception in create_item: {e}")
			return None
		
	def _initialize_database_connection(self, config):
		"""Initializes and returns database connection pool."""
		cnx = None
		try:
			cnx = connector.connect(pool_name = 'dbpool', pool_size=10, **config)
		except Exception as e:
			print(e)
		return cnx



