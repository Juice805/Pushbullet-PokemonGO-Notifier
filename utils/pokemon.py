from datetime import datetime
import time


class Pokemon():
    _meta = None

    def __init__(self, meta):
        self._meta = meta
    
    def get_location(self):
        return {'latitude': self._meta['latitude'], 'longitude': self._meta['longitude']}
    
    def get_id(self):
        return self._meta['pokemon_id']
    
    def get_name(self):
        return self._meta['pokemon_name']
    
    def get_expires_timestamp(self):
        return self._meta['expires']
    
    def get_expires(self):
        return datetime.fromtimestamp(self.get_expires_timestamp())
        
    def sec_till_expire(self):
        return int(self.get_expires_timestamp()) - int(time.time())
    
    def __repr__(self):
        location = self.get_location()
        
        return '%s [%d]: %f, %f, %d seconds left' % (
                                                     self.get_name(),
                                                     self.get_id(),
                                                     location['latitude'],
                                                     location['longitude'],
                                                     int(self.get_expires_timestamp() - time.time())
                                                     )

def is_unique(pokemon, archive):
    for poke in archive:
        
        timestamp_diff = abs(poke.get_expires_timestamp() - pokemon.get_expires_timestamp())
        latitude_diff = abs(poke.get_location()['latitude'] - poke.get_location()['latitude'])
        longitude_diff = abs(poke.get_location()['longitude'] - poke.get_location()['longitude'])
        
        if timestamp_diff < 2:
            if longitude_diff < .00002:
                if latitude_diff < .00002:
                    if poke.get_id() == pokemon.get_id():
                        print('%s ignored' % pokemon.get_name())
                        return False
                    else:
                        print 'Unique Pokemon ID: %d - %d' % (poke.get_id(), pokemon.get_id())
                else:
                    print 'Unique longitude: Difference of %f' % (longitude_diff)
            else:
                print 'Unique latitude: Difference of %f' % (latitude_diff)
        else:
            print 'Unique timestamp: Difference of %f' % (timestamp_diff)
    return True