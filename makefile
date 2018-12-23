# The following make file build for GTK+3, Glade and Multiple Source Directories.

# VARIABLES for make file.
MAIN_FILE_NAME = runserver.py

# Run the make file.
$(MAIN_FILE_NAME): clear run

run:
	@echo Running Python file.
	python3 "$(MAIN_FILE_NAME)"
	@echo

clean:
	@echo Removes only existing runtime and object files.
	@echo

clear:
	clear
