**Управляет скорбордами, а именно их задачами.**
Выводит список всех существующих скорбордов с их отображаемыми именами и критериями.
```ansi
[35mscoreboard [34mobjectives list
```
Добавляет новый скорборд с указанным именем, критерией и необязательным отображаемым названием. Используйте факьюшку `?скорборд критерии`, чтоб получить список всех критерий.
```ansi
[35mscoreboard [34mobjectives add [33m<[0mскорборд[33m> <[0mкритерия[33m> [[35m<[0mотображаемое название[35m>[33m]
```
Удаляет скорборд с указанным именем.
```ansi
[35mscoreboard [34mobjectives remove [33m<[0mскорборд[33m>
```
Отображает информацию о значениях указанного скорборда в определённом слоте. 
```ansi
[35mscoreboard [34mobjectives setdisplay [33m<[32mслот[33m> [35m<[0mскорборд[35m>[33m
```
Удаляет отображение какого-либо скорборда в указанном слоте.
```ansi
[35mscoreboard [34mobjectives setdisplay [33m<[32mслот[33m>
```
Изменяет, будут ли отображаемые имена автоматически обновляться на каждом обновлении их значения.
```ansi
[35mscoreboard [34mobjectives modify [33m<[0mскорборд[33m> [34mdisplayautoupdate [33m<[0mзначение[33m>
```
---separator---
Изменяет отображаемое имя скорборда в слотах отображения.
```ansi
[35mscoreboard [34mobjectives modify [33m<[0mскорборд[33m> [34mdisplayname [33m<[0mjson текст[33m>
```
Сбрасывает формат отображения чисел значений у скорборда в дисплей слотах до того, что по умолчанию.
```ansi
[35mscoreboard [34mobjectives modify [33m<[0mскорборд[33m> [34mnumberformat
```
Ставит формат отображения чисел значений у скорборда в дисплей слотах на пустой, то есть числа не будут отображаться вообще.
```ansi
[35mscoreboard [34mobjectives modify [33m<[0mскорборд[33m> [34mnumberformat blank
```
Ставит формат отображения чисел значений у скорборда в дисплей слотах на статичный текстовый json компонент.
```ansi
[35mscoreboard [34mobjectives modify [33m<[0mскорборд[33m> [34mnumberformat fixed [33m<[0mjson текст[33m>
```
Изменяет стиль формата отображения чисел значений у скорборда в дисплей слотах, например `{"color": "aqua", "bold": true}` сделает все числа светло-голубыми и жирными.
```ansi
[35mscoreboard [34mobjectives modify [33m<[0mскорборд[33m> [34mnumberformat style [33m<[0mстиль[33m>
```
Изменяет формат отображения чисел у скорбордов в tab листе игроков и над головами игроков, на числа либо сердца.
```ansi
[35mscoreboard [34mobjectives modify [33m<[0mскорборд[33m> [34mrendertype [33m([34mhearts[33m|[34minteger[33m)
```