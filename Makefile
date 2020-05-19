test:
	pytest ./tests

pre-run:
	mkdir -p build
	python main.py program.php ./build/program.asm
	nasm -f elf32 -F dwarf -g ./build/program.asm -o ./build/program.o
	ld -m elf_i386 -o ./build/program ./build/program.o

run: pre-run
	./build/program