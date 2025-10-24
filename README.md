# memory-management
 Pablo Torres Arroyo  
 801-19-7744  
 23/10/2025  

### Libraries used:
---
1. **Sys**: Capture program parameters
2. **Random**: Randomization for test file generation
3. **Classes**: Custom created classes for this project. It contains the Node, PageFrame, and CircularLinkedList classes.

### How to run
---

The project consists of four separate programs:

The three algorithm programs second.py, optimal.py, and wsclock.py share the initial setup. 

Using the function parseInstructionFile, the sequence files are parsed into an array where each element is a single instruction from the file. 

They all also use an array of PageFrames in order to keep track of the amount of times each page is accessed via page fault or page hit.

The unique algorithm for each is denoted with a comment that reads:

#Start of <algorithm> page replacement algorithm

At the end of every program, the page faults, page hits and access amounts for each page are displayed

- second.py:

Use: python3 second.py <number_of_physical_memory_pages> <access_sequence_file>

The program takes a page sequence file and a max of physical memory pages to simulate the Second Chance page replacement algorithm. 

Firstly the program fills the entirety of the alloted memory space with PageFrame objects using a circularly linked list. Once the list is filled, it begins to check each page frame.

On a page hit, the page frame's bit is turned on if it isn't already.

Before a page fault once memory is full, the program checks the pages in FIFO order. If it checks a page with its bit turned on, it resets it to 0 and checks the next page. If it checks a page with its bit turned off, it replaces it on the spot. The replacement function of the linked list removes a page in its position and appends the new page at the end, retaining FIFO

- optimal.py:

Use: python3 second.py <number_of_physical_memory_pages> <access_sequence_file>

The program takes a page sequence file and a max of physical memory pages to simulate the Optimal page replacement algorithm.

In order to simulate the theoretical efficiency of the optimal algorithm, the program first preprocesses the instructions and generates a dictionary where the key is the id of a page and the associated value is an array of indexes for each mention of the page in the instruction array.

The algorithm itself follows the same structure of the second chance algorithm until the list is full. Hits do not cause an additional effect.

Before a page fault once memory is full, the program checks each page in the list and captures the page with the latest access. If a page is never accessed again, that one is removed and the new page is appended at the end. If all pages are accessed later, it will remove the farthest to be accessed.

- wsclock.py:

Use: python3 second.py <number_of_physical_memory_pages> <tau> <access_sequence_file>

The program takes a page sequence file, a time difference minimum and a max of physical memory pages to simulate the WSClock page replacement algorithm.

Just like the other programs, the WSClock algorithm first fills all memory spaces before diverting. However, every time a page faults, they are inserted with a time of last access given by the current program counter.

On a page hit, the reference bit of the page is turned on similarly to the second chance algorithm. The last time of access is also updated for the page.


Before a page fault once memory is full, the WSClock algorithm uses a clock hand that points towards the current to-be-tested page. When a page's reference bit is 1, it is simply reset to 0 and the hand advances. 

When the page's reference bit is 0, it must check to see if the program counter - the page's last time of access is more than the time difference minimum stated as a parameter. If it is, the page is replaced exactly in place, and the new page is given its latest access time.

If the time difference minimum is not superceded, the clock hand advances and continues checking. Should the algorithm do a full loop, it removes the page with the eldest access time.

- testgen.py:

Use: python3 testgen.py <test_file_amount>

The program generates as many randomized test files as indicated in the parameter.

### Sources consulted

People:
1. Sergio Rodriguez: Described a method to generative the remaining instructions array for optimal
