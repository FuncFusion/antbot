## {pack_mcmeta} Файл `pack.mcmeta`
`pack.mcmeta` нужен для того, чтобы майнкрафт смог увидеть рп/дп и понять, для какой версии он предназначен. Если не создавать этот файл, допустить в нём ошибку, или если у него формат не `mcmeta` — майнкрафт вероятно не покажет рп/дп в списке или они просто не заработают. Пример содержания файла `pack.mcmeta`:
```json
{
    "pack": {
        "pack_format": 57,
        "description": "Описание"
    }
}
```
### Числа `pack_format`
Каждой версии присваиваются свои числа, которые нужно указывать в `"pack_format"` файла `pack.mcmeta`, чтоб указать, для какой версии наш дп/рп. Если число будет отличаться от версии, на которой вы пробуете ваш дп/рп, это не означает, что он не будет работать. Наоборот, чаще всего он будет работать, но всегда будет предупреждать о возможных неисправностях, выделяя дп/рп красным цветом в окне их выбора. Тем не менее бывают редкие случаи, когда число влияет на ресурспак, поэтому рекомендуется всегда следить за этим.

Чтобы посмотреть, какие числа форматов относятся к каким версиям, используйте команду </packformat:1203447815305691206> либо зайдите на [вики](https://minecraft.wiki/w/Pack_format), где также есть таблица со всеми числами.
