### {bbmodel} {id} CustomModelData
CustomModelData - ванильный метод, добавленный в 1.14, который позволяет менять модель предмету в зависимости от значения компонента `custom_model_data` (до 1.20.5 - нбт тега `CustomModelData`), то есть не задевая обычный предмет.

### Как же пользоваться этим методом?
1. Выберите предмет, модель которого вы будете менять. Для этого примера возьмём палку.
2. Найдите модель этого предмета в дефолт ресурспаке. В нашем случае это `assets/minecraft/models/item/stick.json`.
3. Скопируйте этот файл модели и вставьте в ваш ресурспак в те же самые папки, что и в дефолт рп, то есть в `assets/minecraft/models/item/`.
4. Откройте файл текстовым редактором. У палки содержимое файла выглядит так:
```json
{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "minecraft:item/stick"
  }
}
```
5. После объекта `textures` добавьте массив `overrides`, а в него столько объектов, сколько разных моделей нам надо добавить для нашего предмета. В параметр `custom_model_data` пишем число, которое должно стоять в компоненте предмета, чтоб изменить модель именно на эту. В параметр `model` пишем путь к файлу модели, на который будет меняться модель предмета. Путь модели по умолчанию начинается с папки `assets/minecraft/models`, поэтому если написать туда например `item/custom_stick`, то это обозначает файл `assets/minecraft/models/item/custom_stick.json`. Если перед путём поставить название неймспейса и двоеточие, то путь по умолчанию изменится на `assets/namespace/models`, где `namespace` - то, что вы написали в название неймспейса. В итоге файл `stick.json` будет выглядеть примерно так:
---separator---
```json
{
    "parent": "item/generated",
    "textures": {
        "layer0": "item/stick"
    },
    "overrides": [
        { "predicate": {"custom_model_data": 1}, "model": "item/custom_stick"},
        { "predicate": {"custom_model_data": 2}, "model": "custom/branch"},
        { "predicate": {"custom_model_data": 3}, "model": "block/stone"},
        { "predicate": {"custom_model_data": 880}, "model": "magica:item/magic_staff"}
    ]
}
```
Данный файл говорит майнкрафту, что:
Если игрок выдаст себе палку с компонентом `[custom_model_data=1]` (до 1.20.5 - нбт тегом`{CustomModelData:1}`), то модель палки заменится на модель `assets/minecraft/models/item/custom_stick.json`.
Если игрок выдаст себе палку с компонентом `[custom_model_data=2]`, то модель палки заменится на модель `assets/minecraft/models/custom/branch.json`.
Если игрок выдаст себе палку с компонентом `[custom_model_data=3]`, то модель палки заменится на модель `assets/minecraft/models/block/stone.json`, что в дефолт рп является моделью блока камня, поэтому палка заменится на блок камня.
Если игрок выдаст себе палку с компонентом `[custom_model_data=880]`, то модель палки заменится на модель `assets/magica/models/item/magic_staff.json`.

### Важно
Учтите, что если числа кастом модел даты, выбранные вами, совпадут с числами другого ресурспака, который игрок может носить одновременно, то всё может сломаться. Поэтому тщательно выбирайте числа для вашей кастом модел даты, не берите слишком большие числа, так как они также могут всё поломать, и не используйте одинаковые числа даже для разных предметов. Эта система далеко неидеальна и поэтому может быть так много проблем.