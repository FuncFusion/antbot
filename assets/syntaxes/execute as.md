Ставит лицо воспроизведения команды на указанных сущностей, не изменяя позицию, поворот, измерение и якорь воспроизведения команды.
В результате изменяет сущность, которая хранится в селекторе `@s`, т. к. этот селектор отвечает за лицо воспроизведения команды. Из-за того, что этот селектор может хранить в себе только одну сущность, то при указании множества сущностей в `execute as` команда разветвляется, то есть воспроизведётся по команде на каждую из выбранных сущностей.
```ansi
[35mexecute [34mas [33m<[36mселектор[33m>
```