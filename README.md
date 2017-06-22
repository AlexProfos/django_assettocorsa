This is a simple Django app for managing Assetto Corsa Servers, without entry_list.cfg.

*Installation*
- put this code into your django folder
- add "'ac'," to you INSTALL_APPS in settings.py
- make migrations for ac
  - python manage.py makemigrations ac
- migrate migrations for ac
  - python manage.py migrate ac
- load default/sample data (default tracks, cars and sample car classes)
  - python manage.py loaddata ac.json

*Tested with:*
- python 3.5
- Django 1.11

*Sample Cron for starting and stopping the servers on linux*
# Start
#* *     * * * root cfg_folder='/opt/steam/assetto/cfg/' ; for x in $(find ${cfg_folder} -name "*.start" |tr "\n" " ") ; do su steam -c "cd ${cfg_folder}../ ; nohup ./acServer -c ${cfg_folder}server_cfg_$(< $x).ini -e ${cfg_folder}entry_list.ini > $(< $x).log 2>&1 &" ; ps axuwf |grep $(< ${x}) |grep -v grep |awk '{print $2}' > ${cfg_folder}/../$(< $x).pid ; rm -f ${x} ; done
# Stop
#* *     * * * root cfg_folder='/opt/steam/assetto/cfg/' ; for x in $(find ${cfg_folder} -name "*.stop" |tr "\n" " ") ; do kill -9 $(< ${cfg_folder}../$(< $x).pid) ; rm -f ${cfg_folder}server_cfg_$(< $x).ini ; rm -f ${cfg_folder}../$(< $x).log ; rm -f ${cfg_folder}../$(< $x).pid ; rm -f $x ; done
