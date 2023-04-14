list_cenarios:
	@echo ""
	@ls cenarios/* | awk 'gsub("cenarios/","")' | awk 'gsub(".json","")'
	@echo ""

save_cenario:
	cat cenario.json > $(file)

load_cenario:
	cat $(file) > cenario.json

run:
	python3 -m src
