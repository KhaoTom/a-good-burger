from framework import GameState


class MainState(GameState):
    """
    Main game state, player character is alive and kicking.
    """
    event_handler = None
    player = None
    game_map = None

    def enter_state(self, data):
        self.event_handler = data["event_dispatcher"]
        self.player = data["player"]
        self.game_map = data["game_map"]
        self.update_fov()

    def handle_ai_turns(self):
        ai_entities = [e for e in self.game_map.entities - {self.player} if e.ai]
        for entity in ai_entities:
            entity.ai.perform(self, entity)

    def update(self, events):
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.handle_ai_turns()

            self.update_fov()

    def update_fov(self):
        self.game_map.update_fov(self.player.x, self.player.y)

    def render(self, console, context):
        self.game_map.render(console)

        self.render_statusbar(console)

        context.present(console)

        console.clear()

    def render_statusbar(self, console):
        player_hp = self.player.stats["hp"]
        console.print(
            x=1,
            y=47,
            string=f"HP: {player_hp.current_value}/{player_hp.maximum_value}",
        )
