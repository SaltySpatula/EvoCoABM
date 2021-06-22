import numpy as np
import random

learning_rate = 0.1
discount_factor = 1


class ReinforcementAgent:
    def __init__(self, moves, communication_tokens):
        self.tokens_received = []
        self.past_states = []
        self.moves = moves
        self.communication_tokens = communication_tokens
        self.actions = communication_tokens + moves
        self.q_table = []
        self.received_token = None
        self.send_token = None
        self.final_move = None
        self.payoff = 0
        self.state_index = 0
        self.epsilon = 0.8
        self.exploration_slow_down = 0.999
        self.action = random.choice(self.actions)
        if self.action in self.communication_tokens:
            self.send_token = self.action
        elif self.action in self.moves:
            self.final_move = self.action
            self.send_token = 0

    def step(self):
        if self.received_token is not None:
            self.tokens_received.append(self.received_token)

        if self.final_move is None:
            if self.tokens_received not in self.past_states:
                self.past_states.append(self.tokens_received)
                self.q_table.append([0 for i in self.actions])

            next_state_index = self.past_states.index(self.tokens_received)

            maximum_possible_payoff = max(self.q_table[next_state_index])
            self.q_table[self.state_index][self.actions.index(self.action)] = (1-learning_rate)*self.q_table[self.state_index][self.actions.index(self.action)] + learning_rate * (discount_factor * maximum_possible_payoff)

            self.state_index = next_state_index
            epsilon_seed = random.uniform(0, 1)
            if epsilon_seed < self.epsilon:
                self.action = self.actions[self.q_table[self.state_index].index(max(self.q_table[self.state_index]))]
            else:
                self.action = random.choice(self.actions)
                self.epsilon = self.epsilon * self.exploration_slow_down

            if self.action in self.communication_tokens:
                self.send_token = self.action
            else:
                self.final_move = self.action
                self.send_token = 0

    def reset(self):
        self.tokens_received = []
        self.received_token = None
        self.send_token = None
        self.final_move = None

    def final_payoff(self, payoff):
        action_index = self.actions.index(self.action)
        self.q_table[self.state_index][action_index] = (1-learning_rate) * self.q_table[self.state_index][action_index] + learning_rate * payoff