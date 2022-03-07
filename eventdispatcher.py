import tcod
import action


class EventDispatcher(tcod.event.EventDispatch[action.Action]):
    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym

        if key == tcod.event.K_UP:
            return action.MovementAction(0, -1)
        elif key == tcod.event.K_DOWN:
            return action.MovementAction(0, 1)
        elif key == tcod.event.K_LEFT:
            return action.MovementAction(-1, -0)
        elif key == tcod.event.K_RIGHT:
            return action.MovementAction(1, -0)

        elif key == tcod.event.K_ESCAPE:
            return action.EscapeAction()

        return None
