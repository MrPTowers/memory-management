from classes import PageFrame, CircularLinkedList
import sys

file = sys.argv[2]
max_size = sys.argv[1]

physical_memory = CircularLinkedList(max_size)
page_table = []

def main():
	instructions = []
	with open(file, "r") as f:
		for line in f:
			line_instructions = line.split()
			instructions.extend(line_instructions)

	for i in instructions:
		i.split(':')
		instruction = i[0]
		page_id = i[1]





if __name__ == "__main__":
    #Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 4:
    	main()
    else:
    	#Disclose correct usage of program
        print("Usage: python3 wsclock.py <number of physical memory pages> <tau> <access sequence file>")
        sys.exit(1)
