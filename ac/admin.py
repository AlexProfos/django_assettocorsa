from django.contrib import admin
from .models import ConfigFile, Car, ConfigTemplate, CarClass, TrackList, Weather, Tyre
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

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
    exclude = ('active_on_server',)
    actions = [make_active, make_inactive]
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
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
            'car',
        )
class CarAdmin(ImportExportModelAdmin):
    resource_class = CarResource
    search_fields = ['car']

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
    search_fields = ['class_name']

class ConfigTemplateResource(resources.ModelResource):
    class Meta:
        model = ConfigTemplate
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'template_name',
            'template_active',
            'template',
            'config_folder',
            'server_folder',
            'server_exec',
        )
class ConfigTemplateAdmin(ImportExportModelAdmin):
    resource_class = ConfigTemplateResource
    list_display = ('template_name', 'template_active', 'creation_date')
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

admin.site.register(ConfigFile, ConfigFileAdmin)
admin.site.register(ConfigTemplate, ConfigTemplateAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarClass, CarClassAdmin)
admin.site.register(TrackList, TrackListAdmin)
admin.site.register(Weather, WeatherAdmin)
admin.site.register(Tyre, TyreAdmin)
