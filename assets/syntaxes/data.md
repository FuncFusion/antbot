**Позволяет получать, мерджить, изменять и удалять НБТ теги у блоков-сущностей, сущностей и НБТ хранилищ.**
Получает весь НБТ или отдельные теги, также можно умножать выведенное число множителем.
```ansi
[35mdata [34mget block [33m<[32mпозиция[33m> [<[0mнбт путь[33m>] [<[0mмножитель[33m>]
[35mdata [34mget entity [33m<[36mселектор[33m> [<[0mнбт путь[33m>] [<[0mмножитель[33m>]
[35mdata [34mget storage [33m<[0mпуть к нбт хранилищу[33m> [<[0mнбт путь[33m>] [<[0mмножитель[33m>]
```
Мерджит НБТ указанного блока/сущности/хранилища с указанным нбт.
```ansi
[35mdata [34mmerge block [33m<[32mпозиция[33m> <[0mнбт[33m>
[35mdata [34mmerge entity [33m<[36mселектор[33m> <[0mнбт[33m>
[35mdata [34mmerge storage [33m<[0mпуть к нбт хранилищу[33m> <[0mнбт[33m>
```
Удаляет НБТ по указанному нбт пути.
```ansi
[35mdata [34mremove block [33m<[32mпозиция[33m> <[0mнбт путь[33m>
[35mdata [34mremove entity [33m<[36mселектор[33m> <[0mнбт путь[33m>
[35mdata [34mremove storage [33m<[0mпуть к нбт хранилищу[33m> <[0mнбт путь[33m>
```
Изменяет определённые нбт теги по указанному нбт пути с помощью разных способов изменения.
```ansi
[35mdata [34mmodify block [33m<[32mпозиция[33m> <[0mнбт путь[33m> <[0mспособ изменения[33m>
[35mdata [34mmodify entity [33m<[36mселектор[33m> <[0mнбт путь[33m> <[0mспособ изменения[33m>
[35mdata [34mmodify storage [33m<[0mпуть к нбт хранилищу[33m> <[0mнбт путь[33m> <[0mспособ изменения[33m>
```
---separator---
У каждого из способов изменения есть три параметра с одинаковыми аргументами:
```ansi
... [33m<[0mспособ изменения[33m> from [33m<[32mпозиция[33m> [<[0mнбт путь[33m>] [<[0mначало[33m>] [<[0mконец[33m>]
[0m... [33m<[0mспособ изменения[33m> from [33m<[36mселектор[33m> [<[0mнбт путь[33m>] [<[0mначало[33m>] [<[0mконец[33m>]
[0m... [33m<[0mспособ изменения[33m> from [33m<[0mпуть к нбт хранилищу[33m> [<[0mнбт путь[33m>] [<[0mначало[33m>] [<[0mконец[33m>]
[0m... [33m<[0mспособ изменения[33m> string [33m<[32mпозиция[33m> [<[0mнбт путь[33m>] [<[0mначало[33m>] [<[0mконец[33m>]
[0m... [33m<[0mспособ изменения[33m> string [33m<[36mселектор[33m> [<[0mнбт путь[33m>] [<[0mначало[33m>] [<[0mконец[33m>]
[0m... [33m<[0mспособ изменения[33m> string [33m<[0mпуть к нбт хранилищу[33m> [<[0mнбт путь[33m>] [<[0mначало[33m>] [<[0mконец[33m>]
[0m... [33m<[0mспособ изменения[33m> value <[0mзначение[33m>
```
**Способы изменения:**
`append` — добавить нбт в конец указанного списка или массива.
`insert <индекс>` — вставить нбт в указанное место списка или массива.
`merge` — мерджить нбт с указанным объектом.
`prepend` — добавить нбт в начало указанного списка или массива.
`set` — просто изменить нбт указанного объекта.