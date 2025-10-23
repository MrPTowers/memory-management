from classes import PageFrame, CircularLinkedList
import sys

file = sys.argv[2]
max_size = sys.argv[1]

physical_memory = CircularLinkedList(max_size)
page_table = []

def main():

	instructions = parseInstructionFile(file)
	for i in instructions:
		i_pair = i.split(':') #Parsing the string into instruction and page id pair
		instruction = split[0]
		page = PageFrame(split[1]) #Create page frame for page

		if page not in page_table: #Check to see if page has already been made. If so, we will be using the existing Page Frame 
			page_table.append(page)
			page_idx = page_table.index(page)
		else:
			page_idx = page_table.index(page)
			page = page_table[page_idx] #Replace page frame with existing
		
		if physical_memory.size == 0: #First entry
			physical_memory.append(page)
			page.access += 1
		elif physical_memory.search(page): #Hit
			page.access += 1
			if (page.bit == 0):
				page.toggleBit()
			else:
				continue
		elif not physical_memory.search(page): #Page not in physical memory
			
			
		

def parseInstructionFile(file):
	instructions = []
	with open(file, "r") as f:
		for line in f:
			line_instructions = line.split()
			instructions.extend(line_instructions)
	return instructions


if __name__ == "__main__":
    #Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 3:
    	main()
    else:
    	#Disclose correct usage of program
        print("Usage: python3 second.py <number of physical memory pages> <access sequence file>")
        sys.exit(1)
