import random
import sys

test_amount = int(sys.argv[1])

def main():

	for i in range(1, test_amount):
		instruction_amount = random.randint(50, 200)
		page_amount_max = random.randint(15, 20)
		with open(f"test{i}.txt", "w") as file:
			for j in range(1, instruction_amount):
				instruction_rand = random.randint(1, 2)
				delimiter_rand = random.randint(1, 2)
				if instruction_rand % 2 == 0:
					instruction = "W:" + f"{random.randint(1, page_amount_max)}"
				else:
					instruction = "R:" + f"{random.randint(1, page_amount_max)}"

				if delimiter_rand % 2 == 0:
					instruction += "\n"
				else:
					instruction += " "
	
				file.write(instruction)
		file.close()				



if __name__ == "__main__":
    #Check to see if program is run with the correct amount of arguments
    if len(sys.argv) == 2:
    	main()
    else:
    	#Disclose correct usage of program
        print("Usage: python3 testgen.py <number of test files to generate>")
        sys.exit(1)
