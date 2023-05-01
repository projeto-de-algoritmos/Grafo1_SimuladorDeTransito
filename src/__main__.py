from .gui import GUI
from .sim import Simulation, eprint


def main():
    cfg = read_config()

    sim = Simulation(
        cenario_file=cfg["cenario_file"],
        tick=cfg["tick"],
        limite_de_recursao=cfg["limite_de_recursao"],
        prever_jogada_cooldown=cfg["prever_jogada_cooldown"],
        skip_prever_jogada_for_ms=cfg["skip_prever_jogada_for_ms"],
    )

    gui = GUI(
        max_fps=cfg["max_fps"],
        resolution=cfg["resolution"],
        fullscreen=cfg["fullscreen"],
        render_scale=cfg["render_scale"],
    )

    while sim.running:
        sim.jump_to_next_tick()
        sim.update()

        pistas = sim.get_pistas_and_carros()
        gui.update(pistas)

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
