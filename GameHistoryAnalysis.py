import numpy as np
import matplotlib.pyplot as plt
from Model import Model, Game


class GameHistoryAnalysis:
    def __init__(self, game_history, num_agents):
        self.game_history = game_history

        self.average_payoffs = []
        self.average_regular_game_payoffs = []
        self.tokens_exchanged_by_generation = []
        self.tokens_exchanged_by_generation_regular = []
        self.cooperative_play_percentages = []
        self.average_chat_length = []
        self.average_regular_chat_length = []
        self.ncd_agents_by_generation = []
        self.crc_agents_by_generation = []
        self.cd_agents_by_generation = []
        self.regular_unique_conversations_by_gen = []
        self.cooperative_epochs = 0

        self.outcome_frequency = [0, 0, 0]
        self.moves_frequency = [0, 0]

        for generation in self.game_history:

            games_in_generation = 0
            regular_games_in_generation = 0

            generation_average_payoff = 0
            generation_regular_average_payoff = 0
            generation_total_tokens_exchanged = 0
            generation_regular_total_tokens_exchanged = 0
            generation_cooperative_games = 0
            distinct_conversations = []

            first_iter = True
            crc_agents = 0
            ncd_agents = 0
            cd_agents = 0

            for game in generation:
                game_average_payoff = (game.row_agent_payoff + game.column_agent_payoff) / 2
                generation_average_payoff += game_average_payoff
                tokens_exchanged = len(game.tokens_exchanged)
                generation_total_tokens_exchanged += tokens_exchanged
                if game.game_outcome in ['CC', 'DD', 'CD', 'DC'] or game.game_outcome in ['SS', 'HH', 'SH', 'HS']:
                    if game.game_outcome in ['CC', 'SS']:
                        self.moves_frequency[0] += 2
                        self.outcome_frequency[0] += 1
                        generation_cooperative_games = generation_cooperative_games + 1
                    elif game.game_outcome in ['DD', 'HH']:
                        self.moves_frequency[1] += 2
                        self.outcome_frequency[1] += 1
                    else:
                        self.moves_frequency[0] += 1
                        self.moves_frequency[1] += 1
                        self.outcome_frequency[2] += 1

                    generation_regular_average_payoff += game_average_payoff
                    generation_regular_total_tokens_exchanged += tokens_exchanged
                    regular_games_in_generation = regular_games_in_generation + 1

                    if game.tokens_exchanged not in distinct_conversations and len(game.tokens_exchanged) != 100:
                        distinct_conversations.append(game.tokens_exchanged)
                games_in_generation = games_in_generation + 1

            for game in generation[:num_agents]:
                if first_iter:
                    if game.row_agent.type == 'NCD':
                        ncd_agents += 1
                    if game.row_agent.type == 'CD':
                        cd_agents += 1
                    if game.row_agent.type == 'CRC':
                        crc_agents += 1
                    first_iter = False
                if game.column_agent.type == 'NCD':
                    ncd_agents += 1
                if game.column_agent.type == 'CD':
                    cd_agents += 1
                if game.column_agent.type == 'CRC':
                    crc_agents += 1

            cooperative_percentage = generation_cooperative_games/games_in_generation * 100

            self.average_payoffs.append(generation_average_payoff / games_in_generation)
            self.average_regular_game_payoffs.append(generation_regular_average_payoff / regular_games_in_generation)
            self.tokens_exchanged_by_generation.append(generation_total_tokens_exchanged)
            self.tokens_exchanged_by_generation_regular.append(generation_regular_total_tokens_exchanged)
            self.cooperative_play_percentages.append(cooperative_percentage)
            self.average_chat_length.append(generation_total_tokens_exchanged / (2 * games_in_generation))
            self.average_regular_chat_length.append(
                generation_regular_total_tokens_exchanged / (2 * regular_games_in_generation))
            self.ncd_agents_by_generation.append(ncd_agents)
            self.crc_agents_by_generation.append(crc_agents)
            self.cd_agents_by_generation.append(cd_agents)
            self.regular_unique_conversations_by_gen.append(len(distinct_conversations))
            self.cooperative_epochs = self.cooperative_epochs + 1 if cooperative_percentage >= 10 else self.cooperative_epochs

    def plot_average_payoff(self):
        plt.plot(self.average_payoffs)
        plt.ylabel('Average Payoff')
        plt.xlabel('Generation')
        plt.show()

    def plot_total_communication(self):
        plt.plot(self.tokens_exchanged_by_generation)
        plt.ylabel('Tokens Exchanged')
        plt.xlabel('Generation')
        plt.show()

    def plot_total_regular_communication(self):
        plt.plot(self.tokens_exchanged_by_generation_regular)
        plt.ylabel('Tokens Exchanged in regular games')
        plt.xlabel('Generation')
        plt.show()

    def plot_cooperation_percentage(self):
        plt.plot(self.cooperative_play_percentages)
        plt.ylabel('Proportion [%] of Games with Mutual Cooperation')
        plt.xlabel('Generation')
        plt.show()

    def plot_average_chat_length(self):
        plt.plot(self.average_chat_length)
        plt.ylabel('Average Chat Length')
        plt.xlabel('Generation')
        plt.show()

    def plot_average_regular_chat_length(self):
        plt.plot(self.average_regular_chat_length)
        plt.ylabel('Average Chat Length in regular games')
        plt.xlabel('Generation')
        plt.show()

    def plot_number_of_unique_conversations(self):
        plt.plot(self.regular_unique_conversations_by_gen)
        plt.ylabel('Unique Conversations')
        plt.xlabel('Generation')
        plt.show()

    def plot_NCD_agents(self):
        plt.plot(self.ncd_agents_by_generation)
        plt.ylabel('NCD Agents')
        plt.xlabel('Generation')
        plt.show()

    def plot_CRC_agents(self):
        plt.plot(self.crc_agents_by_generation)
        plt.ylabel('CRC Agents')
        plt.xlabel('Generation')
        plt.show()

    def plot_CD_agents(self):
        plt.plot(self.cd_agents_by_generation)
        plt.ylabel('Mimics')
        plt.xlabel('Generation')
        plt.show()
