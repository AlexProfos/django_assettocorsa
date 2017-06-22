from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ConfigTemplate(models.Model):
    class Meta:
        verbose_name = 'Config Template'
        verbose_name_plural = 'Config Templates'

    def __str__(self):
        return self.template_name

    template_name = models.CharField(
        max_length=32,
        default='temp'
    )
    template_active = models.BooleanField(
        default=False
    )
    template = models.TextField()
    config_folder = models.CharField(
        max_length=100,
        default='/path/to/assettocorsa/cfg',
        help_text='be sure to be case sensetive'
    )
    server_folder = models.CharField(
        max_length=100,
        default='/path/to/assettocorsa/',
        help_text='be sure to be case sensetive'
    )
    server_exec = models.CharField(
        max_length=20,
        default='acServer',
        help_text='be sure to be case sensetive'
    )
    creation_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        blank=True
    )

class Car(models.Model):
    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = "Cars"

    def __str__(self):
        return self.car

    car = models.CharField(
        max_length=32
    )

    class Meta:
        ordering = ['car']

class CarClass(models.Model):
    class Meta:
        verbose_name = 'Carclass'
        verbose_name_plural = "Carclasses"
        ordering = ['class_name']

    def __str__(self):
        return self.class_name

    class_name = models.CharField(
        max_length=32,
        null=True
    )
    cars = models.ManyToManyField(
        Car
    )

class TrackList(models.Model):
    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = "Tracks"
        ordering = ['track_name']

    def __str__(self):
        return self.track_name
    
    track_name = models.CharField(
        default='',
        max_length=64,
        blank=False,
        help_text='Track Displayname'
    )
    track = models.CharField(
        default='',
        max_length=64,
        blank=False,
        help_text='check acserver/content/tracks/*'
    )
    track_config = models.CharField(
        default='',
        max_length=64,
        blank=True,
        help_text='check acserver/content/tracks/"track"/*'
    )

class Tyre(models.Model):
    def __str__(self):
        return self.tyre_name

    class Meta:
        verbose_name = 'Tyre'
        verbose_name_plural = "Tyres"

    tyre_name = models.CharField(
        default='',
        max_length=32,
        blank=False
    )
    tyre = models.CharField(
        default='',
        max_length=3,
        blank=False,
        help_text='shortname of the Tyre, for the config'
    )


class Weather(models.Model):
    class Meta:
        verbose_name = 'Weather'
        verbose_name_plural = "Weather"

    def __str__(self):
        return self.weather_name

    weather_name = models.CharField(
        max_length=32,
        blank=False,
        help_text='Weather Displayname'
    )
    weather = models.CharField(
        max_length=32,
        blank=False
    )

class ConfigFile(models.Model):
    class Meta:
        verbose_name = 'Configfile'
        verbose_name_plural = "Configfiles"

    def __str__(self):
        return self.config_name

    config_name = models.CharField(
        'Config Name',
        unique=True,
        max_length=32,
        help_text='unique config name'
    )
    active_on_server = models.BooleanField(
        default=False
    )
    creation_date = models.DateTimeField(
        'date published',
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        'date updated',
        auto_now_add=True
    )
    udp_tcp_port = models.IntegerField(
        unique=False, default=9600
    )
    http_port = models.IntegerField(
        default=8081
    )
    server_name = models.CharField(
        default='AC Server',
        max_length=32,
        help_text='Servername in AC Server List.'
    )
    password = models.CharField(
        max_length=32,
        blank=True,
        default='',
        help_text='Server Password'
    )
    admin_password = models.CharField(
        max_length=32,
        blank=False,
        help_text='Server Admin Password'
    )
    cars_classes = models.ForeignKey(
        CarClass,
        null=True,
        blank=False
    )
    tracks = models.ForeignKey(
        TrackList,
        null=True,
        blank=False
    )
    sun_angle = models.IntegerField(
        default=48
    )
    max_clients = models.IntegerField(
        default=16,
        help_text='Depends on the servers network performance and the Tracks Pit Slots.'
    )
    race_over_time = models.IntegerField(
        default=30,
        help_text='Time left after the leader finishes the race (in seconds)'
    )
    allowed_tyres_out = models.IntegerField(
        default=-1,
        help_text='penalty (-1 disabled)'
    )
    loop_mode = models.BooleanField(
        default=True,
        help_text='the server restarts from the first track, if active'
    )
    register_to_lobby = models.BooleanField(
        default=False,
        help_text='this must not be touched'
    )
    pickup_mode_enabled = models.BooleanField(
        default=False,
        help_text='if disabled the server start in booking mode (do not use it)'
    )
    sleep_timer = models.IntegerField(
        default=1,
        help_text='this must not be touched'
    )
    voting_quorum = models.IntegerField(
        default=75,
        help_text='percentage of vote that is required for the SESSION vote to pass'
    )
    vote_duration = models.IntegerField(
        default=20,
        help_text='time in seconds'
    )
    blacklist_mode = models.IntegerField(
        default=0,
        help_text='this must not be touched'
    )
    tc_allowed = models.IntegerField(
        default=1,
        help_text='0 -> no car can use TC, 1 -> only car provided with TC can use it; 2-> any car can use TC'
    )
    abs_allowed = models.IntegerField(
        default=1,
        help_text='0 -> no car can use ABS, 1 -> only car provided with ABS can use it; 2-> any car can use ABS'
    )
    stability_allowed = models.IntegerField(
        default=0,
        help_text='Stability assist 0 -> OFF; 1 -> ON'
    )
    autoclutch_allowed = models.IntegerField(
        default=1,
        help_text='Autoclutch assist 0 -> OFF; 1 -> ON'
    )
    damage_multiplier = models.IntegerField(
        default=100,
        help_text='Damage from 0 (no damage) to 100 (full damage)'
    )
    fuel_rate = models.IntegerField(
        default=100,
        help_text='Fuel usage from 0 (no fuel usage) to XXX (100 is the realistic one)'
    )
    tyre_wear_rate = models.IntegerField(
        default=100,
        help_text='Tyre wear from 0 (no tyre wear) to XXX (100 is the realistic one)'
    )
    client_send_interval_hz = models.IntegerField(
        default=15,
        help_text='refresh rate of packet sending by the server. 10Hz = ~100ms. Higher number = higher MP quality = higher bandwidth resources needed. Really high values can create connection issues'
    )
    tyre_blankets_allowed = models.BooleanField(
        default=True,
        help_text='at the start of the session or after the pitstop the tyre will have the optimal temperature'
    )
    qualify_max_wait_perc = models.IntegerField(
        default=120,
        help_text='120 means that 120% of the session fastest lap remains to end the current lap.'
    )
    welcome_message = models.CharField(
        max_length=2048,
        blank=True,
        default='',
        help_text='path of a file who contains the server welcome message'
    )
    start_rule = models.IntegerField(
        default=1,
        help_text='0 is car locked until start; 1 is teleport; 2 is drivethru (if race has 3 or less laps then the Teleport penalty is enabled)'
    )
    num_threads = models.IntegerField(
        default=4,
        help_text='number of server cpu threads used'
    )
    force_virtual_mirror = models.BooleanField(
        default=True,
        help_text='active = virtual mirror will be enabled for every client, disabled = mirror as optional'
    )
    legal_tyre = models.ManyToManyField(
        Tyre,
        help_text='list of the tyres shortnames that will be allowed in the server.'
    )
    max_ballast_kg = models.IntegerField(
        default=0,
        help_text='the max total of ballast that can be added through the admin command'
    )
    udp_plugin_local_port = models.CharField(
        max_length=5,
        blank=True,
        help_text='this must not be touched'
    )
    udp_plugin_address = models.CharField(
        max_length=15,
        blank=True,
        help_text='this must not be touched'
    )
    auth_plugin_address = models.CharField(
        max_length=15,
        blank=True,
        help_text='this must not be touched'
    )
    race_gas_penalty_disabled = models.IntegerField(
        default=0,
        help_text='0 any cut will be penalized with the gas cut message; 1 no penalization will be forced, but cuts will be saved in the race result json.'
    )
    result_screen_time = models.IntegerField(
        default=20,
        help_text='seconds of result screen between racing sessions.'
    )
    race_extra_lap = models.IntegerField(
        default=0,
        help_text='if it is a timed race, with 1 the race will not end when the time is over and the leader crosses the line, but the latter will be forced to drive another extra lap.'
    )
    locked_entry_list = models.IntegerField(
        default=0,
        help_text='same as in booking mode, only players already included in the entry list can join the server (password not needed).'
    )
    race_pit_window_start = models.IntegerField(
        default=0,
        blank=True,
        help_text='Pit window open at lap/minute (depends on the race mode)'
    )
    race_pit_window_end = models.IntegerField(
        default=0,
        blank=True,
        help_text='Pit window closes at lap/minute (depends on the race mode)'
    )
    reversed_grid_race_positions = models.IntegerField(
        default=0,
        help_text='0 = no additional race, 1toX = only those position will be reversed for the next race, -1 = all the position will be reversed (Retired players will be on the last positions)'
    )
    time_of_day_mult = models.IntegerField(
        default=1,
        help_text='multiplier for the time of day'
    )
    max_contacts_per_km = models.IntegerField(
        default=5,
        help_text='max allowed contacts per KM'
    )
# Dynamic Track
    dyn_track = models.BooleanField(
        default=True,
        help_text='Enable/Disable Dynamic Track'
    )
    dyn_track_session_start = models.IntegerField(
        default=90,
        help_text='% level of grip at session start'
    )
    dyn_track_randomness = models.IntegerField(
        default=1,
        help_text='level of randomness added to the start grip'
    )
    dyn_track_lap_gain = models.IntegerField(
        default=1,
        help_text='how many laps are needed to add 1% grip'
    )
    dyn_track_session_transfer = models.IntegerField(
        default=50,
        help_text='how much of the gained grip is to be added to the next session 100 -> all the gained grip. Example: difference between starting (90) and ending (96) grip in the session = 6%, with session_transfer = 50 then the next session is going to start with 93.'
    )
# Book
    booking = models.BooleanField(
        default=True,
        help_text='Enable/Disable Booking mode'
    )
    book_name = models.CharField(
        max_length=16,
        default='Booking',
        blank=True
    )
    book_time = models.IntegerField(
        default=5,
        help_text='session length in minutes'
    )
# Practice
    practice = models.BooleanField(
        default=True,
        help_text='Enable/Disable Practice Session'
    )
    practice_name = models.CharField(
        max_length=16,
        default='Free Practice',
        blank=True
    )
    practice_time = models.IntegerField(
        default=15,
        help_text='session length in minutes'
    )
    practice_is_open = models.IntegerField(
        default=1,
        help_text='0 = no join, 1 = free join,'
    )
# Qualify
    qualify = models.BooleanField(
        default=True,
        help_text='Enable/Disable Qualify Session'
    )
    qualify_name = models.CharField(
        max_length=16,
        default='Qualify',
        blank=True
    )
    qualify_time = models.IntegerField(
        default=15,
        help_text='session length in minutes'
    )
    qualify_is_open = models.IntegerField(
        default=1,
        help_text='0 = no join, 1 = free join,'
    )
# Race
    race_name = models.CharField(
        max_length=16,
        default='Race'
    )
    race_laps = models.IntegerField(
        default=10,
        help_text='length of the lap races'
    )
    race_time = models.IntegerField(
        default=0,
        help_text='length of the timed races, only if laps = 0'
    )
    race_wait_time = models.IntegerField(
        default=60,
        help_text='seconds before the start of the session'
    )
    race_is_open = models.IntegerField(
        default=2,
        help_text='0 = no join, 1 = free join, 2 = free join until 20 seconds to the green light'
    )
# Weather
    weather_graphics = models.ForeignKey(
        Weather,
        null=True,
        blank=False
    )
    weather_base_temperature_ambient = models.IntegerField(
        default=20,
        help_text='temperature of the Ambient'
    )
    weather_variation_ambient = models.IntegerField(
        default=2,
        help_text='variation of the ambients temperature. In this example final ambients temperature can be 16 or 20'
    )
    weather_base_temperature_road = models.IntegerField(
        default=6,
        help_text='Relative road temperature: this value will be added to the final ambient temp. In this example the road temperature will be between 22 (16 + 6) and 26 (20 + 6). It can be negative.'
    )
    weather_variation_road = models.IntegerField(
        default=1,
        help_text='variation of the roads temperature. Like the ambient one.'
    )
# Wind
    wind_base_speed_min = models.IntegerField(
        default=3,
        help_text='Min speed of the session possible'
    )
    wind_base_speed_max = models.IntegerField(
        default=15,
        help_text='Max speed of session possible (max 40)'
    )
    wind_base_direction = models.IntegerField(
        default=50,
        help_text='base direction of the wind (wind is pointing at); 0 = North, 90 = East etc'
    )
    wind_variation_direction = models.IntegerField(
        default=15,
        help_text='variation (+ or -) of the base direction'
    )
# Author
    author = models.ForeignKey(
        User,
        blank=True,
        help_text='Config creator'
    )
