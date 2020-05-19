test:
	pytest ./tests

compile:
	python main.py program.php program.asm
	nasm -f elf32 -F dwarf -g program.asm
	ld -m elf_i386 -o program program.o

run:
	./program