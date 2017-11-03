from django.contrib import admin
from .models import ConfigFile
from .models import Car
from .models import ConfigTemplate
from .models import CarClass
from .models import TrackList
from .models import Weather
from .models import Tyre
from .models import Teams
from .models import EntryListUsers
from .models import EntryLists
from import_export import resources
from import_export.admin import ImportExportModelAdmin
import copy


# Register your models here.


def duplicate_carclass(modeladmin, request, queryset):
    for object in queryset:
        object_copy = copy.copy(object)
        object_copy.id = None
        if object_copy.class_name == object_copy.class_name:
            object_copy.class_name = object_copy.class_name + "_copy"
        object_copy.save()
        for car in object.cars.all():
            object_copy.cars.add(car)
        object_copy.save()


duplicate_carclass.short_description = "Duplicate selected record"


def make_active(modeladmin, request, queryset):
    queryset.update(active_on_server=True)


make_active.short_description = "activate manuel started server"


def make_inactive(modeladmin, request, queryset):
    queryset.update(active_on_server=False)


make_inactive.short_description = "disable crashed server"


class ConfigFileResource(resources.ModelResource):
    class Meta:
        model = ConfigFile
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'config_name',
            'creation_date',
            'last_updated',
            'udp_tcp_port',
            'server_name',
            'password',
            'admin_password',
            'cars_classes',
            'tracks',
            'sun_angle',
            'max_clients',
            'race_over_time',
            'allowed_tyres_out',
            'loop_mode',
            'register_to_lobby',
            'pickup_mode_enabled',
            'sleep_timer',
            'voting_quorum',
            'vote_duration',
            'blacklist_mode',
            'tc_allowed',
            'abs_allowed',
            'stability_allowed',
            'autoclutch_allowed',
            'damage_multiplier',
            'fuel_rate',
            'tyre_wear_rate',
            'client_send_interval_hz',
            'tyre_blankets_allowed',
            'qualify_max_wait_perc',
            'welcome_message',
            'start_rule',
            'num_threads',
            'force_virtual_mirror',
            'legal_tyre',
            'max_ballast_kg',
            'udp_plugin_local_port',
            'udp_plugin_address',
            'auth_plugin_address',
            'race_gas_penalty_disabled',
            'result_screen_time',
            'race_extra_lap',
            'locked_entry_list',
            'race_pit_window_start',
            'race_pit_window_end',
            'reversed_grid_race_positions',
            'time_of_day_mult',
            'max_contacts_per_km',
            'dyn_track',
            'dyn_track_session_start',
            'dyn_track_randomness',
            'dyn_track_lap_gain',
            'dyn_track_session_transfer',
            'booking',
            'book_name',
            'book_time',
            'practice',
            'practice_name',
            'practice_time',
            'practice_is_open',
            'qualify',
            'qualify_name',
            'qualify_time',
            'qualify_is_open',
            'race_name',
            'race_laps',
            'race_time',
            'race_wait_time',
            'race_is_open',
            'weather_graphics',
            'weather_base_temperature_ambient',
            'weather_variation_ambient',
            'weather_base_temperature_road',
            'weather_variation_road',
            'wind_base_speed_min',
            'wind_base_speed_max',
            'wind_base_direction',
            'wind_variation_direction',
            'author',
        )


class ConfigFileAdmin(ImportExportModelAdmin):
    resource_class = ConfigFileResource

    def button(self, obj):
        return '<a class="button" href="/ac/start/%s/">Start Server</a>&nbsp; \
            <a class="button" href="/ac/stop/%s/">Stop Server</a>' % (obj.id, obj.id)

    button.short_description = 'Server Actions'
    button.allow_tags = True
    list_display = ('config_name', 'udp_tcp_port', 'active_on_server', 'button', 'author', 'creation_date')
    search_fields = ['config_name']
    list_filter = ('active_on_server', 'author')
    fieldsets = (
        (None, {
            'fields': (
                'config_name',
                'server_name',
                'max_clients',
                'password',
                'admin_password',
                'register_to_lobby',
                'loop_mode',
                'udp_tcp_port',
                'http_port',
            ),
        }),
        ('Tracks and Cars', {
            'classes': ('collapse',),
            'fields': (
                'entrylist',
                'cars_classes',
                'tracks',
                'dyn_track',
                'dyn_track_session_start',
                'dyn_track_randomness',
                'dyn_track_lap_gain',
                'dyn_track_session_transfer',
            ),
        }),
        ('Rules', {
            'classes': ('collapse',),
            'fields': (
                'race_over_time',
                'allowed_tyres_out',
                'tc_allowed',
                'abs_allowed',
                'stability_allowed',
                'autoclutch_allowed',
                'tyre_blankets_allowed',
                'start_rule',
                'force_virtual_mirror',
                'max_ballast_kg',
                'race_gas_penalty_disabled',
                'max_contacts_per_km',
            ),
        }),
        ('Sessions', {
            'classes': ('collapse',),
            'fields': (
                'pickup_mode_enabled',
                'booking',
                'book_name',
                'book_time',
                'practice',
                'practice_name',
                'practice_time',
                'practice_is_open',
                'qualify',
                'qualify_name',
                'qualify_time',
                'qualify_is_open',
                'race_name',
                'race_laps',
                'race_time',
                'race_wait_time',
                'race_is_open',
                'race_extra_lap',
                'qualify_max_wait_perc',
                'race_pit_window_start',
                'race_pit_window_end',
                'reversed_grid_race_positions',
            ),
        }),
        ('Damage, Tyres and Fuel', {
            'classes': ('collapse',),
            'fields': (
                'damage_multiplier',
                'fuel_rate',
                'tyre_wear_rate',
                'legal_tyre',
            ),
        }),
        ('Weather', {
            'classes': ('collapse',),
            'fields': (
                'sun_angle',
                'time_of_day_mult',
                'weather_graphics',
                'weather_base_temperature_ambient',
                'weather_variation_ambient',
                'weather_base_temperature_road',
                'weather_variation_road',
                'wind_base_speed_min',
                'wind_base_speed_max',
                'wind_base_direction',
                'wind_variation_direction',
            ),
        }),
        ('Server Basics (might not be touched)', {
            'classes': ('collapse',),
            'fields': (
                'sleep_timer',
                'client_send_interval_hz',
                'welcome_message',
                'num_threads',
                'udp_plugin_local_port',
                'udp_plugin_address',
                'auth_plugin_address',
                'result_screen_time',
                'voting_quorum',
                'vote_duration',
                'locked_entry_list',
                'blacklist_mode',
                'author',
            ),
        }),
    )
    exclude = ('active_on_server',)
    actions = [make_active, make_inactive, ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()


class TrackListResource(resources.ModelResource):
    class Meta:
        model = TrackList
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'track_name',
            'track',
            'track_config',
        )


class TrackListAdmin(ImportExportModelAdmin):
    resource_class = TrackListResource
    search_fields = ['track_name']


class CarResource(resources.ModelResource):
    class Meta:
        model = Car
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'car_name',
            'car',
        )


class CarAdmin(ImportExportModelAdmin):
    resource_class = CarResource
    search_fields = ['car_name']


class CarClassResource(resources.ModelResource):
    class Meta:
        model = CarClass
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'class_name',
            'cars',
        )


class CarClassAdmin(ImportExportModelAdmin):
    resource_class = CarClassResource
    actions = [duplicate_carclass]
    search_fields = ['class_name']
    filter_horizontal = ('cars',)


class ConfigTemplateResource(resources.ModelResource):
    class Meta:
        model = ConfigTemplate
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'template_name',
            'template_active',
            'entrylist',
            'template',
            'config_folder',
            'server_folder',
            'server_exec',
        )


class ConfigTemplateAdmin(ImportExportModelAdmin):
    resource_class = ConfigTemplateResource
    list_display = ('template_name', 'template_active', 'entrylist', 'creation_date')
    search_fields = ['template_name']


class WeatherResource(resources.ModelResource):
    class Meta:
        model = Weather
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'weather_name',
            'weather',
        )


class WeatherAdmin(ImportExportModelAdmin):
    resource_class = WeatherResource
    search_fields = ['weather_name']


class TyreResource(resources.ModelResource):
    class Meta:
        model = Tyre
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'tyre_name',
            'tyre',
        )


class TyreAdmin(ImportExportModelAdmin):
    resource_class = TyreResource
    search_fields = ['Tyre_name']


class TeamResource(resources.ModelResource):
    class Meta:
        model = Teams
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'team',
        )


class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource
    search_fields = ['team']


class EntryListUsersResource(resources.ModelResource):
    class Meta:
        model = EntryListUsers
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'name',
            'drivername',
            'teamname',
            'entrycar',
            'skin',
            'guid',
            'spectator',
            'ballast',
            'restrictor',
        )


class EntryListUsersAdmin(ImportExportModelAdmin):
    resource_class = EntryListUsersResource
    list_display = ('name', 'teamname', 'entrycar', 'skin',)
    search_fields = ['name']


class EntryListResource(resources.ModelResource):
    class Meta:
        model = EntryLists
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'entrylist',
            'entrylistusers',
        )


class EntryListAdmin(ImportExportModelAdmin):
    resource_class = EntryListResource
    search_fields = ['entrylist']


admin.site.register(ConfigFile, ConfigFileAdmin)
admin.site.register(ConfigTemplate, ConfigTemplateAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarClass, CarClassAdmin)
admin.site.register(TrackList, TrackListAdmin)
admin.site.register(Weather, WeatherAdmin)
admin.site.register(Tyre, TyreAdmin)
admin.site.register(Teams, TeamAdmin)
admin.site.register(EntryListUsers, EntryListUsersAdmin)
admin.site.register(EntryLists, EntryListAdmin)
