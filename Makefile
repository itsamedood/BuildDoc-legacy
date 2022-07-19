# Yes, I used the very thing I'm trying to make an alternative to, shut up.

# Files.
MAIN 	:= src/main.py
BINARY	:= builddoc-bin
ZIP					:=

# OS-Dependant.
OS			 		:= $(shell uname -s | tr A-Z a-z)
SYS 		 		:=
OUTPUT_PATH  		:=

# Other.
BUILDDOC_VERSION	:= 0.0.1
RELEASE_STAGE 		:= ALPHA

# Checking the OS.
ifeq ($(OS), linux)
	SYS := linux
else ifeq ($(OS), darwin)
	SYS := macos
else
	SYS := windows
endif

# Updating paths.
OUTPUT_PATH  := bin/$(SYS)
ZIP			 := release/$(BUILDDOC_VERSION)/$(RELEASE_STAGE)/builddoc-$(SYS).zip

.PHONY: release

# Compiles all the python files to an executable, using cxfreeze.
# https://pypi.org/project/cx-Freeze/
compile:
	@echo 🛠 Compiling... 🛠
	@echo -----------------
ifeq ($(SYS), macos)
	cxfreeze -c ./$(MAIN) --target-dir ./$(OUTPUT_PATH) --target-name $(BINARY) | lolcat -f

else ifeq ($(SYS), linux)
# cxfreeze didn't wanna work on Linux for some reason, so I'm using PyInstaller instead.
# https://pypi.org/project/pyinstaller/
	pyinstaller --onefile ./$(MAIN) --distpath ./$(OUTPUT_PATH) --name $(BINARY) && rm -r ./build | lolcat -f

else
	@echo MichealSoft BinBows.
endif
# Empty echo to create gap between compilation output and run-time output.
	@echo
	./$(OUTPUT_PATH)/$(BINARY)

# Just runs the program.
run:
	@echo 🔨 Running... 🔨
	@echo ---------------
	./$(OUTPUT_PATH)/$(BINARY)

test:
	@echo 🧪 Testing... 🧪
	@echo ---------------
	./$(OUTPUT_PATH)/$(BINARY) -v

# Zips together the binary, it's libraries, the shell scripts, and the README, then puts it in `./release`.
release:
	@echo 📁 Releasing... 📁
	@echo -----------------
ifeq ("$(wildcard ./release/)", "")
	mkdir release
endif

ifeq ("$(wildcard ./release/$(BUILDDOC_VERSION)/)", "")
	mkdir release/$(BUILDDOC_VERSION)
endif

ifeq ("$(wildcard ./release/$(BUILDDOC_VERSION)/$(RELEASE_STAGE)/)", "")
	mkdir ./release/$(BUILDDOC_VERSION)/$(RELEASE_STAGE)/
endif
# 						./scripts/*  👇
	zip -X -r ./$(ZIP) ./bin/$(SYS)/* ./README.txt | lolcat -f

	@echo 📂 Released v$(BUILDDOC_VERSION) [$(RELEASE_STAGE)]! 📂
	@echo -----------------------------------
