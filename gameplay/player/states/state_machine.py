from gameplay.player.states.basic_state import BasicState
from gameplay.player.states.idle import PlayerIdleState
from gameplay.player.states.run import PlayerRunState


class StateMachine:
    def __init__(self, context, first_state) -> None:
        self.state = first_state
        self.states = {
            'idle': PlayerIdleState(context, 'idle', {'run'}),
            'run': PlayerRunState(context, 'run', {'idle'})
        }
        self.current_state: BasicState = self.states.get(self.state)

    def change_state(self, state: str):
        if not state:
            return
        if state not in self.current_state.possible_next_states:
            return
        if not self.states[state].cooldown():
            return
        self.current_state._exsit()
        self.current_state = self.states[state]
        self.current_state._enter()
        self.state = state

    def update(self, dt, *args):
        self.current_state.update(dt, *args)
        for state in self.states.values():
            state.cooldown.timer()
        self.change_state(self.current_state.next_state())
        # if state := self.current_state.next_state(): self.change_state(state)
