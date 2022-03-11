import numpy
from game.tiletypes import unexplored


def render_map(game_map, console):
    console.rgb[0:game_map.width, 0:game_map.height] = numpy.select(
        condlist=[game_map.visible, game_map.explored],
        choicelist=[game_map.tiles["light"], game_map.tiles["dark"]],
        default=unexplored
    )

    entities_sorted_for_rendering = sorted(
        game_map.entities, key=lambda e: e.z
    )

    for entity in entities_sorted_for_rendering:
        if game_map.visible[entity.x, entity.y]:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)


def render_statusbar(player, turn_count, console):
    x = 1
    console.print(
        x=x,
        y=47,
        string=f"HP: {player.hp}",
    )
    x += 9
    console.print(
        x=x,
        y=47,
        string=f"Atk: {player.attack}",
    )
    x += 9
    console.print(
        x=x,
        y=47,
        string=f"Def: {player.defense}",
    )
    x += 9
    console.print(
        x=x,
        y=47,
        string=f"Turn: {turn_count}",
    )


def render_messagebar(messages, index, console):
    msg = messages[index]
    console.print(
        x=1,
        y=48,
        string=f"{msg}"
    )
