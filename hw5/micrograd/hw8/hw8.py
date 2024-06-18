import gymnasium as gym
env = gym.make("CartPole-v1", render_mode="human") 


observation, info = env.reset(seed=42)
score = 0

def action(observation):
    if observation[3]>0:
        action = 1
    else:
        action = 0
    return action
for _ in range(1000):
   env.render()
   observation, reward, terminated, truncated, info = env.step(action(observation))

   
   score += reward
   if terminated or truncated:
      observation, info = env.reset()
      print('done, score=', score)
      score = 0
env.close()