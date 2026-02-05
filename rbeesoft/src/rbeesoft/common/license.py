import time


class License:
    def __init__(self, payload):
        self._payload = payload

    def customer(self):
        return self._payload['customer']
    
    def product(self):
        return self._payload['product']
    
    def feature_list(self):
        return self._payload['features']
    
    def expiry_days(self):
        return int(self._payload['exp'])
    
    def major_version(self):
        return float(self._payload['major_version'])
    
    def id(self):
        return self._payload['license_id']
    
    # CHECKS

    def is_expired(self):
        now = int(time.time())
        if now > self.expiry_days():
            return True
        return False
    
    def has_all_features(self):
        return 'all' in self.feature_list()
    
    def has_feature(self, name):
        return name in self.feature_list()