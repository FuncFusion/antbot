Возвращает общее значение указанного атрибута.
```ansi
[35mattribute [33m<[36mселектор[33m> <[0mатрибут[33m> [34mget [33m[[34m<[0mмножитель[34m>[33m]
```
Возвращает базовое значение указанного атрибута.
```ansi
[35mattribute [33m<[36mселектор[33m> <[0mатрибут[33m> [34mbase get [33m[[34m<[0mмножитель[34m>[33m]
```
Изменяет базовое значение указанного атрибута.
```ansi
[35mattribute [33m<[36mселектор[33m> <[0mатрибут[33m> [34mbase set [33m<[0mзначение[33m>
```
Сбрасывает базовое значение указанного атрибута.
```ansi
[35mattribute [33m<[36mселектор[33m> <[0mатрибут[33m> [34mbase reset
```
Добавляет модификатор атрибута с заданными свойствами, если не существует модификатора с таким же айди.
Операции атрибутов:
- `add_value` — добавляет значение к базовому значению атрибута.
- `add_multiplied_base` — Умножает базововое значение атрибута на (1 + сумму значений модификаторов).
`Итоговое значение = Базовое значение × (1 + Модификатор1 + Модификатор2 + … + МодификаторN)`
- `add_multiplied_total` — Умножает базововое значение атрибута на (1 + значения модификаторов) для каждого модификатора.
`Итоговое значение = Базовое значение × (1 + Модификатор1) × (1 + Модификатор2) × … × (1 + МодификаторN)`
```ansi
[35mattribute [33m<[36mселектор[33m> <[0mатрибут[33m> [34mmodifier add [33m<[0mайди[33m> <[0mимя[33m> <[0mзначение[33m> ([34madd_value[33m|[34madd_multiplied_base[33m|[34madd_multiplied_total[33m)
``` 
Убирает модификатор атрибута с указанным айди.
```ansi
[35mattribute [33m<[36mселектор[33m> <[0mатрибут[33m> [34mmodifier remove [33m<[0mайди[33m>
```
Возвращает значение атрибута с указанным айди.
```ansi
[35mattribute [33m<[36mселектор[33m> <[0mатрибут[33m> [34mmodifier value get [33m<[0mайди[33m> [[34m<[0mscale[34m>[33m]
```