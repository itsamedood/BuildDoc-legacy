# Files.
MAIN 	:= src/main.py
BINARY	:= builddoc-bin

# OS-Dependant.
OS			 := $(shell uname -s | tr A-Z a-z)
SYS 		 :=
OUTPUT_PATH  :=
RELEASE_PATH :=

# Checking the OS.
ifeq ($(OS), "linux")
	SYS := linux
else ifeq ($(OS), darwin)
	SYS := macos
else
	SYS := windows
endif

# Updating paths.
OUTPUT_PATH  := bin/$(SYS)
RELEASE_PATH := release/$(SYS)

# Compiles all the python files to an executable, using cxfreeze.
# https://pypi.org/project/cx-Freeze/
compile:
	@echo 🛠 Compiling... 🛠
	@echo -----------------
	cxfreeze -c ./$(MAIN) --target-dir ./$(OUTPUT_PATH) --target-name $(BINARY)
# Empty echo to create gap between compilation output and run-time output.
	@echo
	./$(OUTPUT_PATH)/$(BINARY)

# Just runs the program.
run:
	@echo 🔨 Running... 🔨
	@echo ---------------
	python3 -B ./$(MAIN)

# Zips together the binary & it's libraries (according to your OS) and puts it in `./release`.
release:
	@echo 📁 Releasing... 📁
	@echo -----------------
	@echo Error: Cannot release yet.
