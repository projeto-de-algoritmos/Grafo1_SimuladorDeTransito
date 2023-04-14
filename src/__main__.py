from .gui import GUI
from .sim import Simulation, eprint

def main():
    sim = Simulation(cenario_file="cenario.json")
    gui = GUI(max_fps=60)

    while sim.running:
        sim.jump_to_next_tick()
        sim.update()

        pistas, carros = sim.get_pistas_and_carros()
        gui.update(pistas, carros)
        
        try:
            gui.render()
        except Exception as e:
            if str(e) == "user closed program":
                break
            else:
                eprint("falha inesperada ao renderizar:", e, cexit=False)
                raise e

    gui.exit()

if __name__ == "__main__":
    main()