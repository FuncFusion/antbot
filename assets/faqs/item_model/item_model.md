## {item_modifier} Компонент `item_model`
В 1.21.2 был добавлен компонент `item_model`, который значительно упрощает изменение модели определённого предмета без использования кастом модел даты (смотрите `?cmd`).

Работает он очень просто - в него нужно вписать путь к модели предмета в ресурспаке, и путь начинается с папки `assets/minecraft/models/item`. Например, если нужно выдать палку с моделью стержня энда, это можно сделать так:
```ansi
[35mgive [36m@s [0mstick[33m[[37mitem_model[34m=[32m"end_rod"[33m]```
А если у нас есть кастомная модель в ресурспаке, и лежит она, например, по пути `assets/namespace/models/item/custom/fire_wand.json`, то команда выдачи будет выглядеть так:
```ansi
[35mgive [36m@s [0mstick[33m[[37mitem_model[34m=[32m"namespace:custom/fire_wand"[33m]```