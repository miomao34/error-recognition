all: run

run:
	. venv/bin/activate && \
		python images.py && \
		deactivate

generate: generate-text-images generate-alphabet

generate-text-images:
	rm generated_examples/*\-*.jpg || true 
	. venv/bin/activate && \
		python text_image_generator.py && \
		deactivate

generate-alphabet:
	rm alphabet.jpg || true 
	. venv/bin/activate && \
		python alphabet_generator.py && \
		deactivate

setup: venv dep

venv:
	python3 -m venv ./venv/

dep:
	. venv/bin/activate && \
		pip install -r requirements.txt && \
		deactivate
