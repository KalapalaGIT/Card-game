import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from main import Deck, Player, Table, GameMenu

class GameEnv:
    def __init__(self):
        # Initialize deck, table, and players
        self.deck = Deck()
        self.deck.shuffle()
        self.table = Table()
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

        # Players start by drawing 5 cards each
        self.player1.draw(self.deck, 5)
        self.player2.draw(self.deck, 5)

        # Initialize the game menu
        self.menu = GameMenu(self.player1, self.player2, self.table)

    def reset(self):
        # Reset the game environment
        self.deck = Deck()
        self.deck.shuffle()
        self.table = Table()
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.player1.draw(self.deck, 5)
        self.player2.draw(self.deck, 5)
        self.menu = GameMenu(self.player1, self.player2, self.table)
        return self.get_state()

    def step(self, action):
        # Execute an action within the game environment
        current_player = self.player1 if self.menu.turn == 1 else self.player2
        self.menu.handle_action(action, current_player)

        # Check game-ending condition (e.g., one player runs out of cards)
        done = len(self.player1.hand) == 0 or len(self.player2.hand) == 0
        reward = 1 if done and len(current_player.hand) == 0 else 0

        return self.get_state(), reward, done

    def get_state(self):
        # Return a simplified state representation
        current_player = self.player1 if self.menu.turn == 1 else self.player2
        return {
            "player_hand": [card.get_value() for card in current_player.hand],
            "table_top_card": self.table.cards[-1].get_value() if self.table.cards else None,
            "deck_size": len(self.deck.cards),
        }

    def render(self):
        # Display the current state of the game
        self.player1.Show_hand()
        self.player2.Show_hand()
        self.table.Print_table()

    def play(self):
        # Start the game loop
        self.menu.start_game()


class QNetwork(nn.Module):
    def __init__(self, input_size, output_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)  # Hidden layer with 128 neurons
        self.fc2 = nn.Linear(128, output_size)  # Output layer with as many neurons as actions

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # ReLU activation for the hidden layer
        x = self.fc2(x)  # Linear output layer
        return x


class DQNAgent:
    def __init__(self, input_size, n_actions, alpha=0.001, gamma=0.9, epsilon=0.1):
        self.input_size = input_size  # Size of state space
        self.n_actions = n_actions  # Number of possible actions
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration-exploitation tradeoff

        # Initialize the Q-network and the optimizer
        self.q_network = QNetwork(input_size, n_actions)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.alpha)

    def choose_action(self, state):
        """Choose an action using epsilon-greedy policy."""
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(range(self.n_actions))  # Explore: choose random action
        else:
            with torch.no_grad():
                state_tensor = torch.tensor(state, dtype=torch.float32)
                q_values = self.q_network(state_tensor)
                return torch.argmax(q_values).item()  # Exploit: choose action with max Q-value

    def update_q_values(self, state, action, reward, next_state, done):
        """Update Q-values using the Bellman equation and backpropagation."""
        state_tensor = torch.tensor(state, dtype=torch.float32)
        next_state_tensor = torch.tensor(next_state, dtype=torch.float32)

        # Get Q-values for the current and next state
        q_values = self.q_network(state_tensor)
        next_q_values = self.q_network(next_state_tensor)

        # Compute the target Q-value
        target = reward + self.gamma * torch.max(next_q_values) * (1 - done)
        current_q_value = q_values[action]

        # Compute the loss (Mean Squared Error)
        loss = nn.MSELoss()(current_q_value, target)

        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def train(self, episodes=1000):
        env = GameEnv()  # Create the game environment
        for episode in range(episodes):
            state = env.reset()  # Reset the environment at the start of each episode
            done = False
            total_reward = 0

            while not done:
                action = self.choose_action(state)  # Choose an action based on the current state
                next_state, reward, done = env.step([action])  # Take the action and get the new state, reward, and done flag

                self.update_q_values(state, action, reward, next_state, done)  # Update the Q-values based on the result

                state = next_state  # Move to the next state
                total_reward += reward

            if episode % 100 == 0:
                print(f"Episode {episode}, Total Reward: {total_reward}")

# Example usage
input_size = 5  # Number of cards in hand (simplified for this example)
n_actions = 12  # Number of possible actions (cards in hand)
agent = DQNAgent(input_size, n_actions)

# Train the agent
agent.train(episodes=1000)