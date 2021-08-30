#from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler

#spark

import argparse
from measure import baseExpect
from measure import directCompare


class Users:
    def __init__(self):
        self.users_id = set()
        self.users_table = {}

    def add_user(self, sn: str):
        self.users_id.add(sn)
        self.users_table[sn] = Client(sn)

    def delete_user(self, sn: str):
        self.users_id.remove(sn)

    def edit_user(self, sn, command):
        pass

    def query(self, sn: str):
        if sn in self.users_id:
            return self.users_table[sn]
        else:
            print("the machine is not on the service list")

    def load(self, path: str):
        users_id = load_users_id(path)
        users_table = load_users_id(path)
        self.users_id = users_id
        self.users_table = users_table

    def predict_base(self):
        for client in self.users_table:
            energy_base = baseExpect(client)
            client.energy.append(energy_base)

    def direct_compare(self):
        for client in self.users_table:
            energy_base = directCompare(client)
            client.energy.append(energy_base)


class Client:
    def __init__(self, sn):
        self._sn = sn
        self.method = None
        self.historical_data_length = None
        self.city = None
        self.district = None
        self.project_type = None
        self.stats = None

    def read_data(self):
        # TODO: adapt to platform data format
        data = read_sql_data(sn)
        self.city = data.city
        self.district = data.district
        self.project_type = data.project_type
        self.stats = data.stats

    def execute(self, command):
        pass


class User:
    _persist_methods = ['get', 'save', 'delete']

    def __init__(self, persister):
        self._persister = persister

    def __getattr__(self, attribute):
        if attribute in self._persist_methods:
            return getattr(self._persister, attribute)


class Logger(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_logger'):
            cls._logger = super(Logger, cls
                    ).__new__(cls, *args, **kwargs)
        return cls._logger


class Command:

    def __init__(self, authenticate=None, authorize=None):
        self.authenticate = authenticate or self._not_authenticated
        self.authorize = authorize or self._not_autorized

    def execute(self, user, action):
        self.authenticate(user)
        self.authorize(user, action)
        return action()


def load_users_id(path):
    pass


def load_users_id(path):
    pass


def main():

    # take behavior params
    parser = argparse.ArgumentParser(description="energy savings measurement and visualization")
    parser.add_argument("", "--command", type=str)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")
    #parser.add_argument("x", type=int, help="the base")
    #parser.add_argument("y", type=int, help="the exponent")
    args = parser.parse_args()
    print("energy savings manager is launched.")
    if args.command == "init":
        users = Users()
    if args.command == "pred":
        users = Users()
        saved_users_data = data_path  # TODO: update
        users.load(saved_users_data)
        users.predict_base()
    if args.command == "compare":
        users = Users()
        saved_users_data = data_path  # TODO: update
        users.load(saved_users_data)
        users.compare()

    if in_sudo_mode:
        command = Command(always_authenticated, always_authorized)
    else:
        command = Command(config.authenticate, config.authorize)
    command.execute(current_user, delete_user_action)

    pass


if __name__ == '__main__':
    main()
