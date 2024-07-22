import sys

import modes

if __name__ == "__main__":
    mode = sys.argv[1]
    
    if mode == 'single':
        modes.single()
    
    elif mode == 'multi':
        try:
            num_of_game = int(sys.argv[2])
            if not num_of_game:
                raise ValueError
            modes.multi(num_of_game)

        except (ValueError, IndexError) as e:
            print(f"use 'python simulation x' where x is number of the games")
           
