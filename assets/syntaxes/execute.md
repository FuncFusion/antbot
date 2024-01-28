`/execute . . .`

*   `... align <axes> -> execute`
*   `... anchored <anchor> -> execute`
*   `... as <[36mселекторs> -> execute`
*   `... at <[36mселекторs> -> execute`
*   `... facing (<pos>|entity <[36mселекторs> <anchor>) -> execute`
*   `... in <dimension> -> execute`
*   `... on <relation> -> execute`
*   `... positioned (<pos>|as <[36mселекторs>|over <heightmap>) -> execute`
*   `... rotated (<rot>|as <[36mселекторs>) -> execute`
*   `... store (result|success) . . .`
    *   `... block <[36mселекторPos> <path> <type> <scale> -> execute`
    *   `... bossbar <id> (max|value) -> execute`
    *   `... entity <[36mселектор> <path> <type> <scale> -> execute`
    *   `... score <[36mселекторs> <objective> -> execute`
    *   `... storage <[36mселектор> <path> <type> <scale> -> execute`
*   `... summon <entity> -> execute`
*   `... (if|unless) . . .`
    *   `... biome <pos> <biome> -> execute`
    *   `... block <pos> <block> -> execute`
    *   `... blocks <start> <end> <destination> (all|masked) -> execute`
    *   `... data . . .`
        *   `... block <sourcePos> <path> -> execute`
        *   `... entity <source> <path> -> execute`
        *   `... storage <source> <path> -> execute`
    *   `... dimension <dimension> -> execute`
    *   `... function <function> -> execute`
    *   `... entity <entities> -> execute`
    *   `... loaded <pos> -> execute`
    *   `... predicate <predicate> -> execute`
    *   `... score <[36mселектор> <[36mселекторObjective> . . .`
        *   `... (<|<=|=|>|>=) <source> <sourceObjective> -> execute`
        *   `... matches <range> -> execute`
*   `... run <command>`

where `-> execute` represents the start of another subcommand.