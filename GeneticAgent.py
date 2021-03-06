class GeneticAgent:
    def __init__(self, state_actions, transition_matrix, communication_tokens, start_state):
        self.payoff = 0
        self.state_actions = state_actions
        self.transition_matrix = transition_matrix
        self.communication_tokens = communication_tokens
        self.start_state = start_state
        self.state = start_state
        self.received_token = None
        self.send_token = None
        self.final_move = None
        self.computational_capacity = len(self.transition_matrix)

        action = self.state_actions[self.state]
        if action in self.communication_tokens:
            self.send_token = action
        else:
            self.final_move = action
            self.send_token = 0

        if self.is_ncd():
            self.type = 'NCD'
        elif self.is_crc():
            self.type = 'CRC'
        elif self.is_mimic():
            self.type = 'CD'
        else:
            self.type = None

    def step(self):
        self.state = self.transition_matrix[self.state][self.received_token]
        if self.final_move is None:
            action = self.state_actions[self.state]
            if action in self.communication_tokens:
                self.send_token = action
            else:
                self.final_move = action
                self.send_token = 0

    def reset(self):
        self.state = self.start_state
        self.received_token = None
        self.send_token = None
        self.final_move = None
        action = self.state_actions[self.state]
        if action in self.communication_tokens:
            self.send_token = action
        else:
            self.final_move = action
            self.send_token = 0

    def is_reacheable(self, start_state, allowed_tokens, final_actions):
        possible_actions = []
        states_visited = []
        self.get_possible_actions(possible_actions, start_state, allowed_tokens, states_visited)
        return any(final_actions[i] in possible_actions for i in range(len(final_actions)))

    def get_possible_actions(self, possible_actions, start_state, allowed_tokens, states_visited):
        possible_actions.append(self.state_actions[start_state])
        states_visited.append(start_state)
        for token in allowed_tokens:
            next_state = self.transition_matrix[start_state][token]
            if next_state not in states_visited:
                possible_actions.append(self.get_possible_actions(possible_actions, next_state, allowed_tokens, states_visited))

    def is_crc(self):
        return self.is_reacheable(self.start_state, self.communication_tokens, ['C', 'S'])

    def is_mimic(self):
        return self.is_reacheable(self.start_state, self.communication_tokens, ['D', 'H'])

    def is_ncd(self):
        return self.state_actions[self.start_state] == 'D' or self.state_actions[self.start_state] == 'H'

    def update_type(self):
        if self.is_ncd():
            self.type = 'NCD'
        elif self.is_crc():
            self.type = 'CRC'
        elif self.is_mimic():
            self.type = 'CD'
        else:
            self.type = None
