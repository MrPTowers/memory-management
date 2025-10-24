from classes import PageFrame, CircularLinkedList
import sys

file = sys.argv[2]
max_size = int(sys.argv[1])

physical_memory = CircularLinkedList(max_size)

def main():

	global physical_memory 
	page_table = [] #Table for access to Page Frame objects
	page_hits = 0
	page_faults = 0

	instructions = parseInstructionFile(file)
	for i in instructions:
		i_pair = i.split(':') #Parsing the string into instruction and page id pair
		#instruction = i_pair[0] This would go here if we were actually running the operations on the pages		
		page = PageFrame(i_pair[1]) #Create page frame for page

		if page not in page_table: #Check to see if page has already been made. If so, we will be using the existing Page Frame 
			page_table.append(page)
			page_idx = page_table.index(page) #Extract index of page for updating later
		else:
			page_idx = page_table.index(page)

		#Start of second chance page replacement algorithm

		if physical_memory.size == 0: #First entry
			physical_memory.append(page_table[page_idx]) #Insert into linked list
			page_table[page_idx].access += 1 #Increment visit amount
			page_faults += 1 #Add to page faults	
		elif physical_memory.search(page_table[page_idx]): #Page Hit
			page_table[page_idx].access += 1
			page_hits += 1 #Add to page hits
			for idx in range(physical_memory.size): #Find the element in the list that corresponds to the page hit
				if page_table[page_idx].id == physical_memory[idx]:
					if physical_memory[idx].bit == 0:
						physical_memory[idx].toggleBit() #Turn second chance bit to 1
						break
		else: #Page not in physical memory
			if physical_memory.size == max_size: #Memory is full
				for idx in range(max_size):
					if physical_memory[idx].bit == 0: #Page fault
						physical_memory.replace(physical_memory[idx], page_table[page_idx]) #Remove old page and add new
						page_table[page_idx].access += 1
						page_faults += 1
						break
					else:
						physical_memory[idx].toggleBit #Return second chance bit to 0
			else: #Memory is not full. Append new page
				physical_memory.append(page_table[page_idx])
				page_table[page_idx].access += 1
				page_faults += 1

	print(f"Page Hits: {page_hits} Page Faults: {page_faults}") #Display all results
	print("Page access amounts:\n")
	for page in page_table:
		print(f"Page {page.id}: Accessed {page.access} times")

def parseInstructionFile(file): #Parse file regardless of if delimiters are newlines or whitespace
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
