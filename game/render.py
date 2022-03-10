def render_map(game_map, console):
    game_map.render(console)


def render_statusbar(player, console):
    console.print(
        x=1,
        y=47,
        string=f"HP: {player.hp.current_value}/{player.hp.maximum_value}",
    )
