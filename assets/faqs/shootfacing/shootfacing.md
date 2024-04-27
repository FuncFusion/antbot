### {predicate} Что такое шутфейсинг?
Shootfacing - это метод, позволяющий запускать сущность в ту сторону, куда она смотрит, за исключением игрока. Это может быть полезно, чтоб искусственно запускать снаряды от игрока в ту сторону, куда он смотрит, или же делать рывок для самих сущностей.

{mcf} `shootface.mcfunction`:
```ansi
[30m# Эта функция запускается от лица и расположения выбранного моба.
[30m# Число 3 в этой команде является силой запуска. Чем больше это число, тем дальше полетит моб.
[35mexecute [34mpositioned [32m0.0 0 0.0 [34mrun [35mtp [36m@s [32m^ ^ ^3
[35mdata [34mmodify storage [33mnamespace:shootfacing [0mMotion [34mset from entity [36m@s [0mPos
[35mtp [36m@s [32m~ ~ ~
[35mdata [34mmodify entity [36m@s [0mMotion [34mset from storage [33mnamespace:shootfacing [0mMotion
```
Теперь, если мы хотим сделать рывок какому то существующему мобу, то используем такую команду:
```ansi
[35mexecute [34mas [33m<[36mселектор[33m> [34mat [36m@s [34mrun [35mfunction [33mnamespace:shootface
```
А если надо заспавнить снаряд и сразу же отправить запустить его в сторону, куда смотрит игрок, то от лица и расположения игрока (с `anchored eyes`) запускаем такую команду:
```ansi
[35mexecute [34mpositioned [32m^ ^ ^1 [34msummon [33m<[36mсущность[33m> [34mpositioned as [36m@s [34mrun [35mfunction [33mnamespace:shootface
```