#from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler

#spark

import argparse
from measure import baseExpect
from measure import directCompare


class Users:
    """
    This is a facade class. The object is used to access all other objects.
    """
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
            return None

    def load(self, path: str):
        users_id = load_users_id(path)
        users_table = load_users_id(path)
        self.users_id = users_id
        self.users_table = users_table

    def run(self, sn_list=None):
        if sn_list is None:
            sn_list = list(self.users_id)
        for i in range(len(sn_list)):
            client = self.users_table[sn_list[i]]
            if not client.method:
                client.recommend_method()
            client.run_measure()
            self.users_table[sn_list[i]] = client

    def run_predict_base(self):
        for client in self.users_table:
            energy_base = baseExpect(client)
            client.energy.append(energy_base)

    def run_direct_compare(self):
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
        self.has_power_meter = False

    def read_data(self):
        # TODO: adapt to platform data format
        # TODO: define time resolution
        # TODO: recognize building using status
        data = read_data(sn)
        self.city = data.city
        self.district = data.district
        self.project_type = data.project_type
        self.stats = data.stats
        self.has_power_meter = data.has_power_meter
        self.historical_data_length = calculate_historical_data_length()

    def recommend_method(self):
        if self.historical_data_length < 365:
            # more than one year
            self.method = "DirectCompare"
        else:
            self.method = self.check_data_quality()

    def check_data_quality(self) -> str:
        if not self.has_power_meter:
            return "DirectCompare"
        else:
            return "BaseExpect"

    def run_measure(self):
        if not self.method:
            self.recommend_method()
        if self.method == "DirectCompare":
            # TODO: determine date_list, k
            results = directCompare.direct_compare(self._sn, date_list=None, k=None)
            comparing_dates = results.comparing_dates
            similar_dates = results.similar_dates
            energy_savings = results.energy_savings

        if self.method == "BaseExpect":
            pass # TODO: run BaseExpect

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


def main():
    """
    initiate
    service
    """

    # take behavior params
    parser = argparse.ArgumentParser(description="energy savings measurement and visualization")
    parser.add_argument("-m", "--model_path", type=str, help="path to ML model for base expecting method", default=None)
    parser.add_argument("-d", "--data_path", type=str, help="path to saved data", default=None)
    parser.add_argument("-c", "--command", type=str, default="init")
    # parser.add_argument("-v", "--verbose", action="store_true")
    # parser.add_argument("-q", "--quiet", action="store_true")
    # parser.add_argument("x", type=int, help="the base")
    # parser.add_argument("y", type=int, help="the exponent")
    args = parser.parse_args()
    print("energy savings manager is launched.")
    print("""command guide:""")
    if args.command == "init":
        users = Users()
        if not args.data_path:
            return users
        else:
            users.load(args.d)
            return users
    if args.command == "run":
        if not args.data_path:
            print("no saved historical data")
        else:
            users = Users()
            users.load(args.d)
            users.run(list(users.users_id))
            return users


def execute():
    output = main()
    print(output)
    return output
"""
    if in_sudo_mode:
        command = Command(always_authenticated, always_authorized)
    else:
        command = Command(config.authenticate, config.authorize)
    command.execute(current_user, delete_user_action)

    pass
"""

if __name__ == '__main__':
    execute()
