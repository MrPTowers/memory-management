from classes import PageFrame, CircularLinkedList
import sys

file = sys.argv[2]
max_size = sys.argv[1]

physical_memory = CircularLinkedList(max_size)
page_table = []


def main():

	page_hits = 0
	page_faults = 0

	instructions = parseInstructionFile(file)
	for i in instructions:
		i_pair = i.split(':') #Parsing the string into instruction and page id pair
		instruction = i_pair[0]
		page = PageFrame(i_pair[1]) #Create page frame for page

		if page not in page_table: #Check to see if page has already been made. If so, we will be using the existing Page Frame 
			page_table.append(page)
			page_idx = page_table.index(page) #Extract index of page for updating later
		else:
			page_idx = page_table.index(page)

		#Start of WSClock page replacement algorithm
		
		if physical_memory.size == 0: #First entry
			physical_memory.append(page) #Insert into linked list
			page_table[page_idx].access += 1 #Increment visit amount
			page_faults += 1 #Add to page faults	
		elif physical_memory.search(page): #Page Hit
			page_table[page_idx].access += 1
			page_hits += 1 #Add to page hits
			if (page.bit == 0):
				page_table[page_idx].toggleBit()
			else:
				continue
		elif not physical_memory.search(page): #Page not in physical memory
			if not physical_memory.append(page): #Memory is full
				for idx in range(physical_memory.size):
					if physical_memory[idx].bit == 0: #Page fault
						physical_memory.replace(physical_memory[idx], page) #Remove old page and add new
						page_table[page_idx].access += 1
						page_faults += 1
						break
					else:
						physical_memory[idx].toggleBit() #Remove the second chance
						continue
			else: #Memory is not full, page already appended in prior if
				page_table[page_idx].access += 1
				page_faults += 1	

	print(f"Page Hits: {page_hits} Page Faults: {page_faults}\n\n")
	print("Page access amounts:\n")
	for page in page_table:
		print(f"Page {page.id}: {page.access}")

def parseInstructionFile(file):
	instructions = []
	with open(file, "r") as f:
		for line in f:
			line_instructions = line.split()
			instructions.extend(line_instructions)
	return instructions


if __name__ == "__main__":
    #Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 4:
    	main()
    else:
    	#Disclose correct usage of program
        print("Usage: python3 wsclock.py <number of physical memory pages> <tau> <access sequence file>")
        sys.exit(1)
