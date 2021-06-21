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

        #if self.is_ncd():
            #self.type = 'NCD'
        #elif self.is_crc():
            #self.type = 'CRC'
        #elif self.is_mimic():
            #self.type = 'CD'
        #else:
            #self.type = None

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

    #def is_crc(self):



    #def is_mimic(self):


    #def is_ncd(self):
    #   return self.state_actions[self.start_state] == 'D'
