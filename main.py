import time
from datetime import timedelta
from datetime import datetime
from pytz import timezone
import re
from skiplagged import Skiplagged
from pushbullet import Pushbullet
from googlemaps import Client
from utils.pokemon import is_unique


        

if __name__ == '__main__':
    client = Skiplagged()
    pb = Pushbullet('key')
    gmaps = Client('api_key)

        # Log in with a Google or Pokemon Trainer Club account
    #print client.login_with_pokemon_trainer('username', 'password')
    print client.login_with_google('username', 'password')


    #bounds = client.get_bounds_for_address('Yosemite, CA')
    bounds = (
              (34.408359, -119.869816), # Lower left lat, lng
              (34.420923, -119.840293) # Upper right lat, lng
              )
    
    my_channel = pb.channels[0]
    print my_channel
    #print my_channel.push_note("Hello World!","Hello Team Valor!")
    
    notify = ['Venasaur','Blastoise', 'Charizard', 'Raichu', 'Nidoqueen', 'Nidoking', 'Clefable', 'Ninetales', 'Vileplume', 'Golduck', 'Arcanine', 'Poliwrath', 'Kadabra', 'Alakazam', 'Machamp', 'Victreebel', 'Golem', 'Slowbro', 'Rapidash', 'Farfetch\'d', 'Dewgong', 'Muk', 'Cloyster', 'Gengar', 'Hypno', 'Exeggutor', 'Hitmonchan', 'Hitmonlee', 'Lickitung', 'Weezing', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Starmie', 'Mr. Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Gyarados', 'Lapras', 'Snorlax', 'Ditto', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omastar', 'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew' ]
    
    archive = []
    

    while 1:
        try:
            
            # Get specific Pokemon Go API endpoint
            print client.get_specific_api_endpoint()
            
            # Get profile
            print client.get_profile()
            
            # Find pokemon
            for pokemon in client.find_pokemon(bounds):
                print pokemon
                id = pokemon.get_name()
                
                if id in notify:

                    PST = timezone('US/Pacific')
                    expires_time = pokemon.get_expires().replace(tzinfo=timezone('UTC')).astimezone(PST)

                    address = gmaps.reverse_geocode((pokemon.get_location()["latitude"], pokemon.get_location()["longitude"]))[0]['address_components']
                    formatted_address = address[0]['short_name'] + ' ' + address[1]['short_name'] + ', ' + address[2]['short_name']
                    
                    
                    message = "%s at %s.\nExpires at %s:%02d:%02d (in %d:%02d)" % (pokemon.get_name(), formatted_address, expires_time.strftime("%-I"), expires_time.minute, expires_time.second, int(pokemon.sec_till_expire()/60), pokemon.sec_till_expire()%60)
                    
                    #mapslink = 'http://maps.apple.com/?q=%s&ll=%f,%f&z=18' % (pokemon.get_name(), pokemon.get_location()["latitude"], pokemon.get_location()["longitude"])
                    mapslink = 'http://maps.apple.com/?q=%f,%f&ll=%f,%f&z=18' % (pokemon.get_location()["latitude"], pokemon.get_location()["longitude"], pokemon.get_location()["latitude"], pokemon.get_location()["longitude"])
                    print mapslink
                    

                    if is_unique(pokemon, archive):
                        archive.append(pokemon)
                        my_channel.push_note("Wild "+ pokemon.get_name().upper() + " appeared!", message + '\n' + mapslink)
                        print "\nWild "+ pokemon.get_name().upper() + " appeared!\n", message + '\n' + mapslink

                    
                    
                    print "%d in archive" % (len(archive))
                    
                    for found in archive:
                        
                        if int(found.get_expires_timestamp() - time.time()) <= 0:
                            print 'Removed: ' + found.get_name()
                            archive.remove(found)
                            
                    
        except Exception as e:
            print "exception:", e
            time.sleep(1)
            


