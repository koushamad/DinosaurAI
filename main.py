from game import Game
import neat
import os


def start(genomes, config):
    point = Game().start(genomes, config, pop.generation + 1)
    print(f'generation: {str(pop.generation + 1)} => point: {str(point)}')


def run(config_path):
    global pop

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(start, 1000000000000)


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)


if __name__ == '__main__':
    main()
