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
	instruction_idx = 0 #Used for searching the entire instruction set based on current instruction
	page_idxs = {} #Used to map a page to its next seen idx

	instructions = parseInstructionFile(file)
	for i in instructions: #This for loop takes every instruction and inserts each time it appears in the instructions array into a dictionary with the page_id as its key
		i_pair = i.split(':') 
		page_id = i_pair[1]

		if page_id not in page_idxs:
			page_idxs[page_id] = [instruction_idx]
		else:
			page_idxs[page_id].append(instruction_idx)
		instruction_idx += 1

	instruction_idx = 0
	for i in instructions:
		i_pair = i.split(':') #Parsing the string into instruction and page id pair
		#instruction = i_pair[0] This would go here if we were actually running the operations on the pages
		page = PageFrame(i_pair[1]) #Create page frame for page

		if page not in page_table: #Check to see if page has already been made. If so, we will be using the existing Page Frame 
			page_table.append(page)
			page_idx = page_table.index(page) #Extract index of page for updating later
		else:
			page_idx = page_table.index(page)

		#Start of optimal page replacement algorithm

		if physical_memory.size == 0: #First entry
			physical_memory.append(page_table[page_idx]) #Insert into linked list
			page_table[page_idx].access += 1 #Increment visit amount
			page_faults += 1 #Add to page faults	
		elif physical_memory.search(page_table[page_idx]): #Page Hit
			page_table[page_idx].access += 1
			page_hits += 1 #Add to page hits
		else: #Page not in physical memory
			if physical_memory.size == max_size: #Memory is full
				#latest_access is a tuple that consists of the idx of the page in memory and the idx of its next mention in the instruction array
				latest_access = [0, 0] 
				for j in range(0, max_size): #Use the preprocessed page indexes dictionary to find the page with the latest access
					remaining_instructions = list(filter(
											lambda x: x > instruction_idx, 
											page_idxs[physical_memory[j].id]))
					if not remaining_instructions: #If the remaining_instructions array is null, prep this page for removal
						latest_access = [j, -1]	
						break
					elif remaining_instructions[0] > latest_access[1]: #If the next instruction is later than the current latest, overwrite
						latest_access = [j, remaining_instructions[0]]
					else:
						continue
				#Whether the for loop breaks early or not, same thing happens
				physical_memory.replace(physical_memory[latest_access[0]], page_table[page_idx])
				page_table[page_idx].access += 1
				page_faults += 1
			else: #Memory is not full. Append new page
				physical_memory.append(page_table[page_idx])
				page_table[page_idx].access += 1
				page_faults += 1
		instruction_idx += 1

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
        print("Usage: python3 optimal.py <number_of_physical_memory_pages> <access_sequence_file>")
        sys.exit(1)
