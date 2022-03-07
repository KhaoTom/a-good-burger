import tcod
from action import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown):
        action = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = MovementAction(delta_x=0, delta_y=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(delta_x=0, delta_y=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(delta_x=-1, delta_y=-0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(delta_x=1, delta_y=-0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        return action
