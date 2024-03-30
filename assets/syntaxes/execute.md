execute ...
... align <оси> -> execute
... anchored <anchor> -> execute
... as <селектор> -> execute
... at <селектор> -> execute
... facing (<позиция>|entity <селектор> <anchor>) -> execute
... in <измерение> -> execute
... on <отношение> -> execute
... positioned (<позиция>|as <селектор>|over <heightmap>) -> execute
... rotated (<rot>|as <targets>) -> execute
... store (result|success) ...
    ... block <targetPos> <path> <type> <scale> -> execute
    ... bossbar <id> (max|value) -> execute
    ... entity <target> <path> <type> <scale> -> execute
    ... score <targets> <objective> -> execute
    ... storage <target> <path> <type> <scale> -> execute
... summon <entity> -> execute
... (if|unless) ...
    ... biome <pos> <biome> -> [execute]
    ... block <pos> <block> -> [execute]
    ... blocks <start> <end> <destination> (all|masked) -> [execute]
    ... data ...
        ... block <sourcePos> <path> -> [execute]
        ... entity <source> <path> -> [execute]
        ... storage <source> <path> -> [execute]
    ... dimension <dimension> -> [execute]
    ... entity <entities> -> [execute]
    ... function <function> -> [execute]
    ... items ...
        ... block <sourcePos> <slots> <item_predicate> -> [execute]
        ... entity <source> <slots> <item_predicate> -> [execute]
    ... loaded <pos> -> [execute]
    ... predicate <predicate> -> [execute]
    ... score <target> <targetObjective> ...
        ... (<|<=|=|>|>=) <source> <sourceObjective> -> [execute]
        ... matches <range> -> [execute]
... run <command>
where -> execute represents the start of another subcommand that is required; -> [execute] represents the start of another subcommand that is optional.