## {md} Что такое сущность взаимодействия (interaction entity) и как ей пользоваться?
Сущность `interaction` (далее — `интеракция`) — техническая сущность, добавленая в версии 1.19.4. Она полностью невидима, неуязвима и её хитбоксу можно менять размер (её хитбокс можно увидеть с помощью `f3+b`). Она позволяет считывать нажатие ЛКМ и ПКМ по ней, но имеет минус того, что не даёт взаимодействовать с чем либо за этой сущностью.

### Как работать с интеракцией
С помощью ачивок можно считывать нажатие ЛКМ/ПКМ по сущности — триггер `player_interacted_with_entity` считывает ПКМ, а `player_hurt_entity` — ЛКМ.

С помощью `execute on` можно переводить исполнителя команды с интеракции на последнего игрока, кто кликнул по ней:
```ansi
[30m# От лица последнего игрока, кто ПКМнул по определённой интеракции, написать в чат "hi"
[35mexecute [34mas [36m@e[33m[[37mtype[34m=[32minteraction[34m,[37mtag[34m=[32msome_tag[33m] [34mon target run [35msay [0mhi
[30m# Тоже самое, но для ЛКМ
[35mexecute [34mas [36m@e[33m[[37mtype[34m=[32minteraction[34m,[37mtag[34m=[32msome_tag[33m] [34mon attacker run [35msay [0mhi```
---separator---
Информация о последнем игроке, ЛКМнувшим по интеракции, записывается в нбт тег `attack`, внутри которого находится тег с UUID кликнувшего игрока и время, когда оно было кликнуто, например — `{attack:{player:[I;-1195679934,1522158402,-1755134412,-1621914861],timestamp:348608L}`, а информация о ПКМнувшем игроке, в свою очередь, записывается в нбт тег `interaction` в таком же формате.
`execute on attacker|target` работает как раз засчёт наличия этих нбт тегов, поэтому если вы хотите, чтоб после клика по интеракции `execute on` срабатывал 1 раз, то вам также следует сразу же убрать эти теги у сущности с помощью `data remove`.

Высота и ширина хитбокса сущности записана в нбт тегах `height` и `width` (по умолчанию — `{width:1.0f,height:1.0f}`, что делает её размер хитбокса 1х1 блок).

Интеракция также имеет нбт тег `response` (по умолчанию — `{response:0b}`), который при значении `1b` включает анимацию руки и звук удара по сущности при ЛКМ и также анимацию взмаха руки при ПКМ.