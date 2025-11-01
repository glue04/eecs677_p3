SCRIPT = dataflow.py
EXECUTABLE = dataflow

all: $(EXECUTABLE)

$(EXECUTABLE): $(SCRIPT)
	@echo "#!/usr/bin/env bash" > $(EXECUTABLE)
	@echo "python3 $(SCRIPT) \$$@" >> $(EXECUTABLE)
	@chmod +x $(EXECUTABLE)


clean:
	@rm -f $(EXECUTABLE)
	@rm -r __pycache__
