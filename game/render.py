def render_map(game_map, console):
    game_map.render(console)


def render_statusbar(player, console):
    player_hp = player.stats["hp"]
    console.print(
        x=1,
        y=47,
        string=f"HP: {player_hp.current_value}/{player_hp.maximum_value}",
    )
