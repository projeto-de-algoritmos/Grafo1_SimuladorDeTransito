save_cenario:
	cat config.json > cenarios/$(name).json

load_cenario:
	cat cenarios/$(name).json > config.json

run:
	python3 src/main.py