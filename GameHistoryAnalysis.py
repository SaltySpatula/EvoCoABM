import numpy as np
import matplotlib.pyplot as plt
from Model import Model, Game


class GameHistoryAnalysis:
    def __init__(self, game_history):
        self.game_history = game_history

    def plot_average_payoff(self):
        average_payoffs = []
        for generation in self.game_history:
            generation_average_total_payoff = 0
            games_in_generation = 0
            for game in generation:
                game_average_payoff = (game.row_agent_payoff + game.column_agent_payoff)/2
                generation_average_total_payoff += game_average_payoff
                games_in_generation = games_in_generation + 1
            average_payoffs.append(generation_average_total_payoff/games_in_generation)
        plt.plot(average_payoffs)
        plt.ylabel('Average Payoff')
        plt.xlabel('Generation')
        plt.show()

    def plot_total_communication(self):
        tokens_exchanged_per_generation = []
        for generation in self.game_history:
            generation_total_tokens_exchanged = 0
            for game in generation:
                generation_total_tokens_exchanged += len(game.tokens_exchanged)
            tokens_exchanged_per_generation.append(generation_total_tokens_exchanged)

        plt.plot(tokens_exchanged_per_generation)
        plt.ylabel('Tokens Exchanged')
        plt.xlabel('Generation')
        plt.show()

    def plot_cooperation_percentage(self):
        cooperative_play_percentages = []
        for generation in self.game_history:
            cooperative_games = 0
            game_index = 0
            for game in generation:
                if game.game_outcome == 'CC' or game.game_outcome == 'SS':
                    cooperative_games = cooperative_games + 1
                game_index = game_index + 1
            cooperative_play_percentages.append((cooperative_games/game_index) * 100)
        plt.plot(cooperative_play_percentages)
        plt.ylabel('Proportion [%] of Games with Mutual Cooperation')
        plt.xlabel('Generation')
        plt.show()

    def plot_average_chat_length(self):
        average_chat_length = []
        for generation in self.game_history:
            generation_total_tokens_exchanged = 0
            games_in_generation = 0
            for game in generation:
                tokens_exchanged = len(game.tokens_exchanged)
                generation_total_tokens_exchanged += tokens_exchanged if tokens_exchanged != 100 else 0
                if tokens_exchanged != 100:
                    games_in_generation += 1
            average_chat_length.append(generation_total_tokens_exchanged/games_in_generation)

        plt.plot(average_chat_length)
        plt.ylabel('Tokens Exchanged')
        plt.xlabel('Generation')
        plt.show()

    def plot_number_of_unique_conversations(self):
        unique_conversations_by_gen = []
        for generation in self.game_history:
            distinct_conversations = []
            for game in generation:
                if game.tokens_exchanged not in distinct_conversations and len(game.tokens_exchanged) != 100:
                    distinct_conversations.append(game.tokens_exchanged)
            unique_conversations_by_gen.append(len(distinct_conversations))
        plt.plot(unique_conversations_by_gen)
        plt.ylabel('Unique Conversations')
        plt.xlabel('Generation')
        plt.show()

    def plot_NCD_agents(self, number_of_agents):
        ncd_agents_by_generation = []
        for generation in self.game_history:
            ncd_agent = 0
            first_iter = True
            for game in generation[:number_of_agents]:
                if game.row_agent.type == 'NCD' and first_iter:
                    ncd_agent += 1
                    first_iter = False
                if game.column_agent.type == 'NCD':
                    ncd_agent += 1
            ncd_agents_by_generation.append(ncd_agent)
        plt.plot(ncd_agents_by_generation)
        plt.ylabel('NCD Agents')
        plt.xlabel('Generation')
        plt.show()

    def plot_CRC_agents(self, number_of_agents):
        crc_agents_by_generation = []
        for generation in self.game_history:
            crc_agent = 0
            first_iter = True
            for game in generation[:number_of_agents]:
                if game.row_agent.type == 'CRC' and first_iter:
                    crc_agent += 1
                    first_iter = False
                if game.column_agent.type == 'CRC':
                    crc_agent += 1
            crc_agents_by_generation.append(crc_agent)
        plt.plot(crc_agents_by_generation)
        plt.ylabel('CRC Agents')
        plt.xlabel('Generation')
        plt.show()

    def plot_CD_agents(self, number_of_agents):
        cd_agents_by_generation = []
        for generation in self.game_history:
            cd_agent = 0
            first_iter = True
            for game in generation[:number_of_agents]:
                if game.row_agent.type == 'CD' and first_iter:
                    cd_agent += 1
                    first_iter = False
                if game.column_agent.type == 'CD':
                    cd_agent += 1
            cd_agents_by_generation.append(cd_agent)
        plt.plot(cd_agents_by_generation)
        plt.ylabel('Mimics')
        plt.xlabel('Generation')
        plt.show()
