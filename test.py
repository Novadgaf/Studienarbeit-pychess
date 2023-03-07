def square_name_to_index(square_name: str) -> int:
        print(ord(square_name[0])-97 + 64-8*int(square_name[1]))

square_name_to_index("a4")
square_name_to_index("c6")
square_name_to_index("h5")
square_name_to_index("a8")