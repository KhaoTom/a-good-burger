class Engine:
    def __init__(self, event_dispatcher, game_map, player):
        self.event_handler = event_dispatcher
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def handle_ai_turns(self):
        ai_entities = [e for e in self.game_map.entities - {self.player} if e.ai]
        for entity in ai_entities:
            entity.ai.perform(self, entity)

    def handle_events(self, events):
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

        self.custom_render(console)

        context.present(console)

        console.clear()

    def custom_render(self, console):
        pass
