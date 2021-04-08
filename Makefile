

DB_REC_PATH ?= "./database_recordings"
FP_PATH     ?= "./data"
QUERY_PATH  ?= "./query_recordings"
OUTPUT      ?= "output.txt"

fingerprinter:
	python3 -c "from fingerprint import fingerprintBuilder;fingerprintBuilder($(DB_REC_PATH), $(FP_PATH))"

shazam:
	python3 -c "from audioid import audioIdentification;audioIdentification($(QUERY_PATH), $(FP_PATH), $(OUTPUT))"

print-and-id:
	python3 main.py

evaluate:
	python3 evaluate.py

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf \
	rm -rf ./data
