import os
import re
from django.conf import settings
from django.http import HttpResponse
from django.template import loader, Context, Template
from django.utils import timezone
from .models import ConfigFile
from .models import Car
from .models import ConfigTemplate
from .models import CarClass
from .models import TrackList
from .models import Weather
from .models import Tyre
from .models import Download
from .models import Teams
from .models import EntryListUsers
from .models import EntryLists
from collections import defaultdict
from django.utils.timezone import activate, localtime, now


activate(settings.TIME_ZONE)
# Create your views here.
def start_server(request, config_id):
    do_nothing = 'true'
    html_template = loader.get_template('start_server.template')
    if request.user.is_staff is True:
        for x in ConfigFile.objects.all().filter(pk=config_id):
            started_by = request.user.username
            config_name_orig = x.config_name
            config_name = re.sub(r'[^\w]', '', x.config_name)
            creation_date = x.creation_date
            author = x.author
            udp_tcp_port = x.udp_tcp_port
            for check in ConfigFile.objects.all().filter(active_on_server=True):
                if x.udp_tcp_port != check.udp_tcp_port:
                    udp_tcp_port = x.udp_tcp_port
                else:
                    do_nothing = 'inuse'
            http_port = x.http_port
            for check in ConfigFile.objects.all().filter(active_on_server=True):
                if x.http_port != check.http_port:
                    http_port = x.http_port
                else:
                    do_nothing = 'inuse'
            server_name = x.server_name
            password = x.password
            admin_password = x.admin_password
            car_list = ''
            for y in CarClass.objects.all().filter(class_name=x.cars_classes):
                for car in y.cars.all().values_list('car'):
                    car_list += '%s;' % car
                cars = car_list[:-1]
            for z in TrackList.objects.all().filter(track_name=x.tracks):
                track = z.track
                config_track = z.track_config
            sun_angle = x.sun_angle
            max_clients = x.max_clients
            race_over_time = x.race_over_time
            allowed_tyres_out = x.allowed_tyres_out
            if x.loop_mode is True:
                loop_mode = 1
            else:
                loop_mode = 0
            if x.register_to_lobby is True:
                register_to_lobby = 1
            else:
                register_to_lobby = 0
            if x.pickup_mode_enabled is True:
                pickup_mode_enabled = 1
                gen_entry_list = True
            else:
                pickup_mode_enabled = 0
                gen_entry_list = False
            sleep_timer = x.sleep_timer
            voting_quorum = x.voting_quorum
            vote_duration = x.vote_duration
            blacklist_mode = x.blacklist_mode
            tc_allowed = x.tc_allowed
            abs_allowed = x.abs_allowed
            stability_allowed = x.stability_allowed
            autoclutch_allowed = x.autoclutch_allowed
            damage_multiplier = x.damage_multiplier
            fuel_rate = x.fuel_rate
            tyre_wear_rate = x.tyre_wear_rate
            client_send_interval_hz = x.client_send_interval_hz
            if x.tyre_blankets_allowed is True:
                tyre_blankets_allowed = 1
            else:
                tyre_blankets_allowed = 0
            qualify_max_wait_perc = x.qualify_max_wait_perc
            welcome_message = x.welcome_message
            start_rule = x.start_rule
            num_threads = x.num_threads
            if x.force_virtual_mirror is True:
                force_virtual_mirror = 1
            else:
                force_virtual_mirror = 0
            legal_tyres = ''
            for tyre in x.legal_tyre.all():
                legal_tyres += '%s;' % tyre.tyre
            legal_tyre = legal_tyres[:-1]
            max_ballast_kg = x.max_ballast_kg
            udp_plugin_local_port = x.udp_plugin_local_port
            udp_plugin_address = x.udp_plugin_address
            auth_plugin_address = x.auth_plugin_address
            race_gas_penalty_disabled = x.race_gas_penalty_disabled
            result_screen_time = x.result_screen_time
            race_extra_lap = x.race_extra_lap
            locked_entry_list = x.locked_entry_list
            race_pit_window_start = x.race_pit_window_start
            race_pit_window_end = x.race_pit_window_end
            reversed_grid_race_positions = x.reversed_grid_race_positions
            time_of_day_mult = x.time_of_day_mult
            max_contacts_per_km = x.max_contacts_per_km
            dyn_track = x.dyn_track
            dyn_track_session_start = x.dyn_track_session_start
            dyn_track_randomness = x.dyn_track_randomness
            dyn_track_lap_gain = x.dyn_track_lap_gain
            dyn_track_session_transfer = x.dyn_track_session_transfer
            booking = x.booking
            book_name = x.book_name
            book_time = x.book_time
            practice = x.practice
            practice_name = x.practice_name
            practice_time = x.practice_time
            practice_is_open = x.practice_is_open
            qualify = x.qualify
            qualify_name = x.qualify_name
            qualify_time = x.qualify_time
            qualify_is_open = x.qualify_is_open
            race_name = x.race_name
            race_laps = x.race_laps
            race_time = x.race_time
            race_wait_time = x.race_wait_time
            race_is_open = x.race_is_open
            for a in Weather.objects.all().filter(weather_name=x.weather_graphics):
                weather_graphics = a.weather
            weather_base_temperature_ambient = x.weather_base_temperature_ambient
            weather_variation_ambient = x.weather_variation_ambient
            weather_base_temperature_road = x.weather_base_temperature_road
            weather_variation_road = x.weather_variation_road
            wind_base_speed_min = x.wind_base_speed_min
            wind_base_speed_max = x.wind_base_speed_max
            wind_base_direction = x.wind_base_direction
            wind_variation_direction = x.wind_variation_direction
            entrylistusers_list = defaultdict(list)
            for d in EntryLists.objects.all().filter(entrylist=x.entrylist):
                count = 0
                for entrylistuser in d.entrylistusers.all():
                    if entrylistuser.spectator is True:
                        entryspectator = 1
                    else:
                        entryspectator = 0
                    for entrycars in Car.objects.all().filter(car_name=entrylistuser.entrycar):
                        entrycar = entrycars.car
                    entrydrivername = re.sub(r'[^\w]', '', str(entrylistuser.drivername))
                    entryteamname = re.sub(r'[^\w]', '', str(entrylistuser.teamname))
                    entrylistusers_list[count].append(
                        [
                            entrydrivername,
                            entryteamname,
                            entrycar,
                            entrylistuser.skin,
                            entrylistuser.guid,
                            entryspectator,
                            entrylistuser.ballast,
                            entrylistuser.restrictor
                        ]
                    )
                    count += 1
            # Set config active on server for the overview
            if x.active_on_server is False and do_nothing == 'true':
                x.active_on_server = True
                x.last_updated = timezone.now()
                x.save()
                do_nothing = 'false'
            elif do_nothing == 'inuse':
                do_nothing = 'inuse'
            else:
                do_nothing = 'true'
        user = request.user.username
        html_context = {
            'do_nothing': do_nothing,
            'username': user,
            'config_name': config_name_orig,
        }

# If update is True overwrite config on server
        config_template = ConfigTemplate.objects.get(template_active=True, entrylist=False)
        template = Template(config_template.template)
        data = {
            'config_name': config_name_orig,
            'creation_date': creation_date,
            'udp_tcp_port': udp_tcp_port,
            'http_port': http_port,
            'server_name': server_name,
            'password': password,
            'admin_password': admin_password,
            'cars': cars,
            'track': track,
            'config_track': config_track,
            'sun_angle': sun_angle,
            'max_clients': max_clients,
            'race_over_time': race_over_time,
            'allowed_tyres_out': allowed_tyres_out,
            'loop_mode': loop_mode,
            'register_to_lobby': register_to_lobby,
            'pickup_mode_enabled': pickup_mode_enabled,
            'sleep_timer': sleep_timer,
            'voting_quorum': voting_quorum,
            'vote_duration': vote_duration,
            'blacklist_mode': blacklist_mode,
            'tc_allowed': tc_allowed,
            'abs_allowed': abs_allowed,
            'stability_allowed': stability_allowed,
            'autoclutch_allowed': autoclutch_allowed,
            'damage_multiplier': damage_multiplier,
            'fuel_rate': fuel_rate,
            'tyre_wear_rate': tyre_wear_rate,
            'client_send_interval_hz': client_send_interval_hz,
            'tyre_blankets_allowed': tyre_blankets_allowed,
            'qualify_max_wait_perc': qualify_max_wait_perc,
            'welcome_message': welcome_message,
            'start_rule': start_rule,
            'num_threads': num_threads,
            'force_virtual_mirror': force_virtual_mirror,
            'legal_tyre': legal_tyre,
            'max_ballast_kg': max_ballast_kg,
            'udp_plugin_local_port': udp_plugin_local_port,
            'udp_plugin_address': udp_plugin_address,
            'auth_plugin_address': auth_plugin_address,
            'race_gas_penalty_disabled': race_gas_penalty_disabled,
            'result_screen_time': result_screen_time,
            'race_extra_lap': race_extra_lap,
            'locked_entry_list': locked_entry_list,
            'race_pit_window_start': race_pit_window_start,
            'race_pit_window_end': race_pit_window_end,
            'reversed_grid_race_positions': reversed_grid_race_positions,
            'time_of_day_mult': time_of_day_mult,
            'max_contacts_per_km': max_contacts_per_km,
            'dyn_track': dyn_track,
            'dyn_track_session_start': dyn_track_session_start,
            'dyn_track_randomness': dyn_track_randomness,
            'dyn_track_lap_gain': dyn_track_lap_gain,
            'dyn_track_session_transfer': dyn_track_session_transfer,
            'booking': booking,
            'book_name': book_name,
            'book_time': book_time,
            'practice': practice,
            'practice_name': practice_name,
            'practice_time': practice_time,
            'practice_is_open': practice_is_open,
            'qualify': qualify,
            'qualify_name': qualify_name,
            'qualify_time': qualify_time,
            'qualify_is_open': qualify_is_open,
            'race_name': race_name,
            'race_laps': race_laps,
            'race_time': race_time,
            'race_wait_time': race_wait_time,
            'race_is_open': race_is_open,
            'weather_graphics': weather_graphics,
            'weather_base_temperature_ambient': weather_base_temperature_ambient,
            'weather_variation_ambient': weather_variation_ambient,
            'weather_base_temperature_road': weather_base_temperature_road,
            'weather_variation_road': weather_variation_road,
            'wind_base_speed_min': wind_base_speed_min,
            'wind_base_speed_max': wind_base_speed_max,
            'wind_base_direction': wind_base_direction,
            'wind_variation_direction': wind_variation_direction,
            'author': author,
            'started_by': started_by,
            'started_at': localtime(now()),
        }
        context = Context(data)

        if do_nothing == 'false':
            if not os.path.isdir(config_template.config_folder):
                os.mkdir(config_template.config_folder)
            config_filename = 'server_cfg_' + config_name + '.ini'
            config_fullpath = config_template.config_folder + config_filename
            with open(config_fullpath, 'w') as config:
                config.write(re.sub("\r?\n", "\n", template.render(context)))
            start_file = config_template.config_folder + config_name + '.start'
            with open(start_file, 'w') as start:
                print(config_name, file=start)
            if gen_entry_list is True:
                count = 0
                for dic in entrylistusers_list.items():
                    for entry in dic[1]:
                        entry_list_number = count
                        drivername = entry[0]
                        teamname = entry[1]
                        entrylist_car = entry[2]
                        skin = entry[3]
                        guid = entry[4]
                        spectator = entry[5]
                        ballast = entry[6]
                        restrictor = entry[7]
                        entrylist_data = {
                            'entry_list_number': entry_list_number,
                            'drivername': drivername,
                            'teamname': teamname,
                            'car': entrylist_car,
                            'skin': skin,
                            'guid': guid,
                            'spectator': spectator,
                            'ballast': ballast,
                            'restrictor': restrictor,
                        }
                        count += 1
                        entrylist_context = Context(entrylist_data)
                        config_template = ConfigTemplate.objects.get(template_active=True, entrylist=True)
                        entrylist_template = Template(config_template.template)
                        entry_filename = 'entry_list_' + config_name + '.ini'
                        entry_fullpath = config_template.config_folder + entry_filename
                        with open(entry_fullpath, 'a') as entry:
                            entry.write(re.sub("\r?\n", "\n", entrylist_template.render(entrylist_context)))
                            entry.write('\n\n')

    else:
        html_context = {
            'do_nothing': do_nothing,
            'username': '',
            'config_name': '',
        }
    return HttpResponse(html_template.render(html_context, request))

def stop_server(request, config_id):
    do_nothing = True
    html_template = loader.get_template('stop_server.template')
    if request.user.is_staff is True:
        config_template = ConfigTemplate.objects.get(template_active=True, entrylist=False)
        for x in ConfigFile.objects.all().filter(pk=config_id):
            config_name_orig = x.config_name
            config_name = re.sub(r'[^\w]', '', x.config_name)
            if x.active_on_server is True:
                x.active_on_server = False
                x.last_updated = timezone.now()
                x.save()
                do_nothing = False
            else:
                do_nothing = True
        if do_nothing is False:
            stop_file = config_template.config_folder + config_name + '.stop'
            with open(stop_file, 'w') as stop:
                print(config_name, file=stop)
            if os.path.exists(config_template.config_folder + config_name + '.start'):
                os.remove(config_template.config_folder + config_name + '.start')
        user = request.user.username
        html_context = {
            'do_nothing': do_nothing,
            'username': user,
            'config_name': config_name_orig,
        }
    else:
        html_context = {
            'do_nothing': do_nothing,
            'username': '',
            'config_name': '',
        }
    return HttpResponse(html_template.render(html_context, request))


def download(request):
    html_template = loader.get_template('downloads.template')
    downloads = Download.objects.all()
    html_context = {
        'downloads': downloads,
    }
    return HttpResponse(html_template.render(html_context, request))