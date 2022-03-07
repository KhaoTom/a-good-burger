class Engine:
    def __init__(self, entities, event_handler, game_map, player):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map

    def handle_events(self, events):
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

    def render(self, console, context):
        self.game_map.render(console)

        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

        context.present(console)

        console.clear()
