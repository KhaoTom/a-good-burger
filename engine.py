class Engine:
    def __init__(self, event_handler, game_map, player):
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def handle_enemy_turns(self):
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} ponders the meaning of life.')

    def handle_events(self, events):
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.handle_enemy_turns()

            self.update_fov()

    def update_fov(self):
        self.game_map.update_fov(self.player.x, self.player.y)

    def render(self, console, context):
        self.game_map.render(console)

        context.present(console)

        console.clear()
