# IRNSS Receiver Software
---

## Folder structure
Note that combiner_utility is for both combiner_decoder and live. command_utility is for command_main. The purpose of each file is as follows:

1. combiner_decoder -- given a log file, it decodes it and gives the output in the same file structure as the default program.

2. live -- (requires the receiver) It establishes a connection with the receiver and decodes the data live and stores it in the same file structure as the default program.

3. combiner_utility -- contains the functions used in the above two. (It is imported in the above two so it must be in the same folder).

4. command_main -- (requires receiver) It establishes a connection with the receiver and sends commands based on input.

5. command_utility -- contains functions used in command_main. (It is imported in command_main so it must be in the same folder)


## Usage
To run the programs, go to the directory in which they are stored and run 

```
>> python3 live.py
(OR)
>> python3 combiner_decoder.py
(OR)
>> python3 command_main.py
```

[Drive link for demonstration of combiner_decoder.py](https://drive.google.com/file/d/1HR5mjOjeMZDl-ffOBGKy7dP6RKYKmemH/view)
