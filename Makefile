list_cenarios:
	@echo ""
	@ls cenarios/* | awk 'gsub("cenarios/","")' | awk 'gsub(".json","")'
	@echo ""

save_cenario:
	cat config.json > cenarios/$(name).json

load_cenario:
	cat cenarios/$(name).json > config.json

run:
	python3 src/main.py
