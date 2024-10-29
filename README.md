# chess_evaluator
evaluating chess games via DNNs?

### Step 0: took data from [Lichess Database](https://database.lichess.org/#standard_games)

### Step 1: read a pgn file, learn about fen notation: mostly done

### Step 2: how to serialize the board as np array, it is 8x8xc but how many channels == states of the board are there?

At first, I imagined I would just do a (17, 8, 8) but its just perfect 4+1 bit fit so why not?

<img src="assets/board_to_bits.svg">


### Step 3: Okay how do we structure the model? now that we have serialized it, assuming I've saved a processed subset to train.


* [ ] should it generate a new board state? -- probably not, too many illegal states.
* [] 
* [ ] c.