import pygame
import numpy as np
import torch
import torch.nn as nn
from Controller import Controller
from dataclasses import dataclass
import matplotlib.pyplot as plt

# Data class for holding all of the training data in one place
@dataclass
class TrainingData:
    state: list
    action: pygame.math.Vector2
    reward: int
    new_state: list
    done: bool

class NN(nn.Module):
    def __init__(self, input_dimensions, output_dimensions):
        super(NN, self).__init__()
        self.input_layer = nn.Linear(input_dimensions, 256)
        self.layer_2 = nn.Linear(256, 256)
        self.output_layer = nn.Linear(256, output_dimensions)

    # Feed forward to get network prediction
    def forward(self, x):
        x = torch.relu(self.input_layer(x))
        x = torch.relu(self.layer_2(x))
        return (self.output_layer(x))

# List of actions as directions:  LEFT, RIGHT, UP, DOWN
ACTIONS = [pygame.math.Vector2(-1, 0), pygame.math.Vector2(1, 0), pygame.math.Vector2(0, -1), pygame.math.Vector2(0, 1)]

class RLController(Controller):
    world = None
    # Main net used for training and updating weights
    main_net = NN(14, 4)
    # Target net used to compare main net output with
    target_net = NN(14, 4)

    target_net.load_state_dict(main_net.state_dict())
    target_net.eval()
    # Experience replay is used to train the networks
    experience = []
    # Number of inputs for the neural network
    num_inputs = 14
    # Hyperparameters for training
    # Epsilon used in epsilon greedy algorithm; see get_action()
    epsilon = 1.0
    epsilon_min = 0.1
    epsilon_decay = 0.8
    gamma = 0.99
    learning_rate = 0.9

    optimizer = torch.optim.Adam(main_net.parameters(), lr=learning_rate)
    
    epochs = 1000
    
    batch_size = 10

    epoch_reward = 0
    current_epoch = 0

    cost = []
    reward_per_epoch = []

    is_dead = False
    apple_eaten = False

    def __init__(self, s):
        self.snake = s

    def dead(self, value):
        self.is_dead = value

    def apple(self, value):
        self.apple_eaten = value
                
    def move(self):
        action = self.train()
        self.snake.change_direction(action)
        self.snake.move()

    def processInput(self, event):
        pass

    # Returns the current state of the world
    def load_state(self, action=None):
        applePos = self.world.getApplePos()
        snakePos = self.world.getSnakePos()

        # If loading state for current state action is None; else direction and position is updated according to action
        if (action is None):
            direction = self.snake.get_direction()
        else:
            direction = action
            snakePos += self.snake.get_size() * action

        # Define feature data
        appleLeft = 0
        appleRight = 0
        appleUp = 0
        appleDown = 0

        appleEaten = 0

        directionLeft = 0
        directionRight = 0
        directionUp = 0
        directionDown = 0

        dangerLeft = 0
        dangerRight = 0
        dangerUp = 0
        dangerDown = 0

        collision = 0

        if (applePos.x < snakePos.x):
            appleLeft = 1
        elif (applePos.x > snakePos.x):
            appleRight = 1
        
        if (applePos.y < snakePos.y):
            appleUp = 1
        elif (applePos.y > snakePos.y):
            appleDown = 1
        
        if (applePos == snakePos):
            appleEaten = 1

        if (direction == ACTIONS[0]):
            directionLeft = 1
        elif (direction == ACTIONS[1]):
            directionRight = 1
        elif (direction == ACTIONS[2]):
            directionUp = 1
        else:
            directionDown = 1

        # Check danger in surrounding directions
        size = self.snake.get_size()
        dangerLeft = int(self.snake.check_danger(snakePos + size * ACTIONS[0]))
        dangerRight = int(self.snake.check_danger(snakePos + size * ACTIONS[1]))
        dangerUp = int(self.snake.check_danger(snakePos + size * ACTIONS[2]))
        dangerDown = int(self.snake.check_danger(snakePos + size * ACTIONS[3]))

        collision = int(self.snake.check_wall(snakePos))
        if (collision == 0):
            collision = int(self.snake.colliding_self())

        # Return state as list of integers
        return [appleLeft, appleRight, appleUp, appleDown, appleEaten, directionLeft, directionRight, directionUp, directionDown, dangerLeft, dangerRight, dangerUp, dangerDown, collision]
        

    def giveWorldView(self, w):
        self.world = w

    def get_random_action(self):
        notDone = True
        while (notDone):
            random_action = np.random.randint(0, 4)
            action = ACTIONS[random_action]
            if (len(self.experience) > 0):
                # Ensure action can be taken and is not opposite direction
                if (action + self.experience[len(self.experience)-1].action != pygame.math.Vector2(0,0)):
                    notDone = False
            else:
                notDone = False
        
        return action

    ###
    # Uses the epsilon greedy algorithm to determine if the agent should select a random action
    # or an action based on the target network
    ###
    def get_action(self, state):
        if (np.random.random() < self.epsilon):
            action = self.get_random_action()
            return action
        else:
            predicted_q_values = self.main_net.forward(torch.FloatTensor([state]))
            
            index = torch.argmax(predicted_q_values)
            
            action = ACTIONS[index]

            return action
        
    def get_reward(self, state):
        reward = 0

        # Check if the apple has been eaten
        if (state[4] == 1 or self.apple_eaten == True):
            reward = 20
            self.apple(False)
            print("Eaten")

        # Check for collision
        if (state[13] == 1 or self.is_dead == True):
            reward = -10
            self.dead(False)
            print("Collision")

        return reward
    
    def load_default_state(self):
        applePos = self.world.getApplePos()
        snakePos = pygame.math.Vector2(300,300)

        direction = self.snake.get_direction()

        # Define feature data
        appleLeft = 0
        appleRight = 0
        appleUp = 0
        appleDown = 0

        appleEaten = 0

        directionLeft = 0
        directionRight = 0
        directionUp = 0
        directionDown = 0

        dangerLeft = 0
        dangerRight = 0
        dangerUp = 0
        dangerDown = 0

        collision = 0

        if (applePos.x < snakePos.x):
            appleLeft = 1
        elif (applePos.x > snakePos.x):
            appleRight = 1
        
        if (applePos.y > snakePos.y):
            appleUp = 1
        elif (applePos.y < snakePos.y):
            appleDown = 1
        
        if (applePos == snakePos):
            appleEaten = 1

        if (direction == ACTIONS[0]):
            directionLeft = 1
        elif (direction == ACTIONS[1]):
            directionRight = 1
        elif (direction == ACTIONS[2]):
            directionUp = 1
        else:
            directionDown = 1

        # Return state as list of integers
        return [appleLeft, appleRight, appleUp, appleDown, appleEaten, directionLeft, directionRight, directionUp, directionDown, dangerLeft, dangerRight, dangerUp, dangerDown, collision]
        

    ###
    # Trains the agent in the training world.
    ###
    def train(self):

        if (len(self.experience) < self.batch_size):
            action = self.get_random_action()
            state = self.load_state()
            reward = self.get_reward(state)
            
            # If there is a collision, load the default state
            if (state[13] == True):
                done = True
                new_state = self.load_default_state()
            else:
                done = False
                new_state = self.load_state(action=action)

            data = TrainingData(state, action, reward, new_state, done)
            self.experience.append(data)

            return action
        
        state = self.load_state()

        action = self.get_action(state)

        reward = self.get_reward(state)
        self.epoch_reward += reward

        new_state = self.load_state(action=action)

        if (state[13] == 0):
            done = False
        else:
            done = True
            print(state[13])

        data = TrainingData(state, action, reward, new_state, done)
        self.experience.append(data)

        self.optimize()

        #Update target network
        if (self.world.getDeaths() % 5 == 0):
            self.target_net.load_state_dict(self.main_net.state_dict())

        if (self.world.getDeaths() != self.current_epoch):
            self.epsilon = max(self.epsilon_min, self.epsilon_decay * self.epsilon)
            self.current_epoch += 1
            self.reward_per_epoch.append(self.epoch_reward)
            self.epoch_reward = 0

        return action

        
    def optimize(self):
        state_batch = []
        #action_batch = np.zeros(shape=(self.batch_size, 1))
        reward_batch = []
        new_state_batch = []
        for i in range(0, self.batch_size):
            rand = np.random.randint(0, len(self.experience))
            state_batch.append(self.experience[rand].state)
            #action_batch.append(self.experience[rand].action)
            reward_batch.append(self.experience[rand].reward)
            new_state_batch.append(self.experience[rand].new_state)

        state_batch = torch.FloatTensor(state_batch)
        reward_batch = torch.FloatTensor(reward_batch)
        new_state_batch = torch.FloatTensor(new_state_batch)

        q_values = torch.t(self.main_net.forward(state_batch))

        with torch.no_grad():
            max_values = self.target_net.forward(new_state_batch).max(1)[0]
            target_values = reward_batch + self.gamma * max_values * (1 - q_values)

        loss = nn.MSELoss()(q_values, target_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
    def plot_rewards(self, rewards_per_epoch):
        plt.plot(rewards_per_epoch)
        plt.xlabel('Epoch')
        plt.ylabel('Reward')
        plt.title('Snake')
        plt.show()
    
    def plot_costs(self, costs):
        plt.plot(costs)
        plt.xlabel('Epoch')
        plt.ylabel('Cost')
        plt.title('Snake')
        plt.show()