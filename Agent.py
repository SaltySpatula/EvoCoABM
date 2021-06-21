import numpy as np
import random

class Agent:
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

        if self.is_ncd():
            self.type = 'NCD'
        elif self.is_crc():
            self.type = 'CRC'
        elif self.is_mimic():
            self.type = 'CD'
        else:
            self.type = None

    def step(self):
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

    def is_reacheable(self, start_state, allowed_tokens, final_action):
        possible_actions = []
        states_visited = []
        self.get_possible_actions(possible_actions, start_state, allowed_tokens, states_visited)
        return final_action in possible_actions

    def get_possible_actions(self, possible_actions, start_state, allowed_tokens, states_visited):
        possible_actions.append(self.state_actions[start_state])
        states_visited.append(start_state)
        for token in allowed_tokens:
            next_state = self.transition_matrix[start_state][token]
            if next_state not in states_visited:
                possible_actions.append(self.get_possible_actions(possible_actions, next_state, allowed_tokens, states_visited))

    def is_crc(self):
        return self.is_reacheable(self.start_state, self.communication_tokens, 'C')

    def is_mimic(self):
        return self.is_reacheable(self.start_state, self.communication_tokens, 'D')

    def is_ncd(self):
        return self.state_actions[self.start_state] == 'D'
