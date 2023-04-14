from .gui import GUI
from .sim import Simulation, eprint

def main():
    cfg = read_config()

    sim = Simulation(
        cenario_file=cfg["cenario_file"],
        tick_rate=cfg["tick_rate"]
    )
    
    gui = GUI(
        max_fps=cfg["max_fps"],
        resolution=cfg["resolution"],
        fullscreen=cfg["fullscreen"],
        render_scale=cfg["render_scale"]
    )

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

def read_config(file="config.json"):
    import json
    with open("config.json", "r") as f:
        return json.load(f)


if __name__ == "__main__":
    main()
