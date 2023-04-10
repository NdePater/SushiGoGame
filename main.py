import os
import neat
from SushiGoGame import SushiGoGame

def eval_genomes(genomes, config):
    
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = SushiGoGame()
            game.train_ai(genome1, genome2, config)

# run neat
def run_neat(config):
    num_generations = 50
    checkpoint_after = 1
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1')
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(checkpoint_after))
    
    winner = population.run(eval_genomes, num_generations)


# if name is main, then run the main function
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    #set config
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)
    
    run_neat(config)