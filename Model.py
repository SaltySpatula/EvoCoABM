import numpy as np
import random
from Agent import Agent


class Model:
    def __init__(self, agents, agent_computation_capacity, communication_tokens,
                 iterations, learning_method, timeout):
        self.number_of_agents = agents
        self.agent_computation_capacity = agent_computation_capacity
        self.number_of_communication_tokens = communication_tokens
        self.iterations = iterations
        self.time = 0
        self.learning_method = learning_method
        self.timeout = timeout
        self.allowed_communication_tokens = np.array([i for i in range(self.number_of_communication_tokens + 1)])
        self.moves = ['C', 'D']
        self.agents = [0 for i in range(self.number_of_agents)]

    def genetic_algorithm_setup(self):
        if self.time == 0:
            # first setup, completely random selection from solution population
            for i in range(self.number_of_agents):
                self.agents[i] = self.create_random_agent()
        else:
            old_population = np.array([i for i in range(self.number_of_agents)])
            no_games_played = self.number_of_agents - 1
            new_population = [0 for i in range(self.number_of_agents)]
            new_population_index = 0
            # populations size stays the same
            for agent in range(self.number_of_agents):
                agent_1 = self.agents[random.choice(old_population)]
                agent_2 = self.agents[random.choice(old_population)]

                average_payoff_agent_1 = agent_1.payoff / no_games_played
                average_payoff_agent_2 = agent_2.payoff / no_games_played
                # better agent chosen for reproduction
                better_agent = agent_1 if average_payoff_agent_1 >= average_payoff_agent_2 else agent_2

                mutation_coefficient = random.uniform(0, 1)
                if mutation_coefficient >= 0.5:
                    # mutate
                    self.mutate(better_agent)

                new_population[new_population_index] = better_agent
                new_population_index = new_population_index + 1
            # swap populations
            self.agents = new_population

#    def RL_setup(self):
#       #ToDo:
#       if self.time == 0:

    def run_model(self):
        print("Running model...")
        while self.time != self.iterations:
            print("Starting Iteration: " + str(self.time))
            if self.learning_method == 'GA':
                self.genetic_algorithm_setup()
            for agent_index in range(self.number_of_agents):
                for agent_jdex in range(agent_index + 1, self.number_of_agents):
                    one_shot_pd = Game(self.agents[agent_index], self.agents[agent_jdex], self.timeout)
                    one_shot_pd.play()
            self.time = self.time + 1
        print("Done")

    def create_random_agent(self):
        transition_matrix = self.create_random_transition_matrix()
        state_actions = self.create_random_state_actions()
        start_state = random.choice([i for i in range(self.agent_computation_capacity)])
        return Agent(state_actions, transition_matrix, self.allowed_communication_tokens, start_state)

    def create_random_transition_matrix(self):
        possible_states = [i for i in range(self.agent_computation_capacity)]
        transition_matrix = np.ndarray((self.agent_computation_capacity, self.number_of_communication_tokens + 1), dtype=int)
        for state_index in range(self.agent_computation_capacity):
            for received_token_index in range(len(transition_matrix[state_index])):
                transition_matrix[state_index][received_token_index] = random.choice(possible_states)
        return transition_matrix

    def create_random_state_actions(self):
        return [self.get_random_action() for i in range(self.agent_computation_capacity)]

    def get_random_action(self):
        move_or_communicate = random.uniform(0, 1)
        if move_or_communicate >= 0.5:
            # communicate
            return random.choice(self.allowed_communication_tokens[1:])
        else:
            # lock in move
            return random.choice(self.moves)

    def mutate(self, agent):
        action_or_transition = random.uniform(0, 1)
        # select random state to mutate
        state_to_mutate = random.randint(0, agent.computational_capacity-1)
        if action_or_transition >= 0.5:
            # Mutate action
            agent.state_actions[state_to_mutate] = self.get_random_action()
        else:
            # Mutate transition
            communication_token = random.randint(0, self.number_of_communication_tokens)
            agent.transition_matrix[state_to_mutate][communication_token] = random.randint(0, agent.computational_capacity-1)


class Game:
    def __init__(self, row_agent, column_agent, timeout):
        self.over = 0
        self.tokens_exchanged = np.array([[], []])
        self.row_agent = row_agent
        self.column_agent = column_agent
        self.timeout = timeout
        self.payoff_matrix = {
            'CC': [2, 2],
            'CD': [4, 1],
            'DD': [3, 3],
            'DC': [1, 4],
            'COL_UNDECIDED': [4, 0],
            'ROW_UNDECIDED': [0, 4],
            'BOTH_UNDECIDED': [0, 0]
        }
        self.game_outcome = None

    def play(self):
        self.column_agent.reset()
        self.row_agent.reset()
        playtime = 0
        while playtime != self.timeout:
            self.exchange_tokens()
            self.row_agent.step()
            self.column_agent.step()
            playtime = playtime + 1
            if self.column_agent.final_move is not None and self.row_agent.final_move is not None:
                self.game_outcome = self.row_agent.final_move + self.column_agent.final_move
                break
            if self.column_agent.final_move is None and self.row_agent.final_move is None:
                self.game_outcome = 'BOTH_UNDECIDED'
            elif self.column_agent.final_move is None:
                self.game_outcome = 'COL_UNDECIDED'
            else:
                self.game_outcome = 'ROW_UNDECIDED'

        row_agent_payoff = self.payoff_matrix.get(self.game_outcome)[0]
        column_agent_payoff = self.payoff_matrix.get(self.game_outcome)[1]
        self.column_agent.payoff += column_agent_payoff
        self.row_agent.payoff += row_agent_payoff

    def exchange_tokens(self):
        self.column_agent.received_token = self.row_agent.send_token
        self.row_agent.received_token = self.column_agent.send_token
