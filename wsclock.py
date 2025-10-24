from classes import PageFrame, CircularLinkedList
import sys

file = sys.argv[3]
max_size = int(sys.argv[1])
tau = int(sys.argv[2])

physical_memory = CircularLinkedList(max_size)

def main():

	global physical_memory 
	page_table = [] #Table for access to Page Frame objects
	page_hits = 0
	page_faults = 0
	clock_hand = None #Clock hand for WSClock algorithm
	pc = 1 #Program counter

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

		#Start of WSClock page replacement algorithm

		if physical_memory.size == 0: #First entry
			physical_memory.append(page_table[page_idx]) #Insert into linked list
			page_table[page_idx].access += 1 #Increment visit amount
			page_faults += 1 #Add to page faults	
			
			clock_hand = physical_memory.head #Clock hand will stay here until the list is filled
			physical_memory[0].last_access = pc #Update the last time page was accessed on memory
			
		elif physical_memory.search(page_table[page_idx]): #Page Hit
			page_table[page_idx].access += 1
			page_hits += 1 #Add to page hits
			for idx in range(physical_memory.size): #Find the element in the list that corresponds to the page hit
				if page_table[page_idx].id == physical_memory[idx]:
					physical_memory[idx].last_access = pc
					if physical_memory[idx].bit == 0: 
						physical_memory[idx].toggleBit() #Turn reference bit to 1
						break
		else: #Page not in physical memory
			if physical_memory.size == max_size: #Memory is full
				greatest_age_page = clock_hand.data
				pages_visited = 0
				while True: #Main WSClock logic
					if pages_visited == max_size: #If a full loop has been made, remove the oldest page
						physical_memory.replaceInPlace(greatest_age_page, page_table[page_idx])
						clock_hand.data.last_access = pc
						clock_hand = clock_hand.next #Advance the clock hand to next node
						page_table[page_idx].access += 1
						page_faults += 1
						break
					elif clock_hand.data.bit == 0: #Reference bit 0
						if pc - clock_hand.data.last_access > tau: #Current time - page's last access time > tau
							physical_memory.replaceInPlace(clock_hand, page_table[page_idx]) #Both conditions have been filled
							clock_hand.data.last_access = pc
							clock_hand = clock_hand.next
							page_table[page_idx].access += 1 
							page_faults += 1
							break
						else: #If the time constraint is not met, keep track of oldest page
							if clock_hand.data.last_access < greatest_age_page.last_access:
								greatest_age_page = clock_hand.data #Update oldest page
								clock_hand = clock_hand.next
							else:
								clock_hand = clock_hand.next
					else: #Reference bit 1
						clock_hand.data.toggleBit()
						clock_hand = clock_hand.next
	
			else: #Memory is not full. Append new page
				physical_memory.append(page_table[page_idx])
				physical_memory[physical_memory.size - 1].last_access = pc
				page_table[page_idx].access += 1
				page_faults += 1
		pc += 1 #Since at this point a page fault or page hit must happen, update program counter (time)

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
    if len(sys.argv) == 4:
    	main()
    else:
    	#Disclose correct usage of program
        print("Usage: python3 wsclock.py <number_of_physical_memory_pages> <tau> <access_sequence_file>")
        sys.exit(1)
