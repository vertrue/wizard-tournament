import sys

import modes

if __name__ == "__main__":
    mode = sys.argv[1]
    
    if mode == 'single':
        modes.single()
    
    elif mode == 'multi':
        # full random simulation

        try:
            num_of_game = int(sys.argv[2])
            if not num_of_game:
                raise ValueError

            modes.multi(num_of_game)
        except ValueError:
            print(f"use 'python simulation x' where x is number of the games")
            
        except IndexError:
            print(f"use 'python simulation x' where x is number of the games")
