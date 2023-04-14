from gui import GUI
from sim import Simulation


def main():
    sim = Simulation(config_file="config.json")
    gui = GUI(max_fps=60)

    while sim.running:
        sim.jump_to_next_tick()
        sim.update()

        pistas, carros = sim.get_pistas_and_carros()
        gui.update(pistas, carros)
        gui.render()

    gui.exit()


if __name__ == '__main__':
    main()
