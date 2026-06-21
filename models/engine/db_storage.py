class DBStorage:

    def close(self):
        """Close current session"""
        self.__session.remove()
