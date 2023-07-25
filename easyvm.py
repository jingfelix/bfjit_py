import os

from rich import print
from typer import Typer

app = Typer()


@app.command()
def help():
    print("Usage: easyvm [options] <file>")
    print("Options:")
    print("  help    Show this message and exit")
    print("  vm      Run the brainfuck VM")


@app.command()
def vm(src: str):
    if src is None:
        print("No input file")
        return

    # check if str exists
    if not os.path.exists(src):
        print("File not exists!")
        return

    pc = 0

    max_length = 30000

    data = [0] * max_length
    stack = []
    ptr = 0

    with open(src, encoding="utf-8", mode="r") as file:
        code = file.read()

    while pc < len(code):

        ch = code[pc]

        if ptr > max_length:
            print("[red]Stack Overwrite![/red]")
            return

        if ch == ">":
            ptr += 1

        elif ch == "<":
            ptr -= 1

        elif ch == "+":
            data[ptr] += 1

        elif ch == "-":
            data[ptr] -= 1

        elif ch == ",":
            buffer = input()
            data[ptr] = ord(buffer[0])

        elif ch == ".":
            print(chr(data[ptr]), end="")

        elif ch == "[":

            current_length = len(stack)

            stack.append(pc)

            if data[ptr] == 0:

                while True:
                    pc += 1

                    if code[pc] == "[":
                        stack.append(pc)
                        continue

                    elif code[pc] == "]":
                        stack.pop()

                        if len(stack) == current_length:
                            break

        elif ch == "]":
            if data[ptr] != 0:
                pc = stack[-1]
            else:
                stack.pop()

        pc += 1

    if len(stack) != 0:
        print("[red]Unmatched '['[/red]")
        return

if __name__ == "__main__":
    app()