## {cameras_file} В РФ не работает Spyglass
Расширение Datapack Helper Plus перестало работать в рф. Вот как это исправить:
- Скачать `zapret-discord-youtube` от Flowseal с гитхаба. Распаковать и поместить в папку программ;
- Заходим в папку скрипта, открываем файл по пути `lists/list-general.txt` и добавляем в самом конце строку `api.spyglassmc.com`;
- Теперь запускаем скрипт `general.bat` или *ALT* для своего региона.
После того, как ваш скрипт активен:
- VS Code должен быть закрыт;
- Удаляем папку по пути `C:\Users\<USER>\AppData\Local\spyglassmc-nodejs\Cache\http`;
- Открываем VS Code и ждём инициализации Spyglass (надпись слева снизу);
- Если всё ещё ошибки, то очищаем кэш: Нажимаем F1, пишем `spyglass`, и из списка выбираем `Spyglass: Reset Project Cache`
-# (Гайд от <@887093938685616138>)