venv:
	python -m venv .venv
	@echo "Para ativar o ambiente virtual, execute:"
	@echo "source .venv/bin/activate"

deps:
	pip3 install -r requirements.txt

list_cenarios:
	@echo ""
	@ls cenarios/* | awk 'gsub("cenarios/","")' | awk 'gsub(".json","")'
	@echo ""

save_cenario:
	cat cenario.json > $(file)

load_cenario:
	cat $(file) > cenario.json

run:
	@echo "" > log.txt
	@python3 -m src
