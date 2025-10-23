class Node:
	def __init__(self, data):
		self.data = data
		self.next = None

class PageTable:
	def __init__(self, id):
		self.id = id
		self.access = 0 #Amount of times page has been accessed
		self.bit = 0 #Reference bit for Second Chance and WSClock
	
	def toggle_bit(self, bit):
		if self.bit == 0:
			self.bit = 1
		else:
			self.bit = 0

    def __eq__(self, other):
        if isinstance(other, PageTable):
            return self.id == other.id
        return False

class CircularLinkedList:
	def __init__(self, max)
		self.head = None
		self.max = max
		self.size = 0

	def append(self, data):
		new_node = Node(data)
		
		if self.size == self.max:
			return False
		elif not self.head:
			new_node.next = new_node
			self.head = new_node
			self.size += 1
		else:
			curr = self.head
			while curr.next != self.head:
				curr = curr.next
			curr.next = new_node
			new_node.next = self.head
			self.size +=1

	def search(self, data):
    	if not self.head:
        	return False

    	curr = self.head
    	while True:
        	if curr.data == data:
            	return True
        	curr = curr.next
        	if curr == self.head:
            	break
    	return False

	def remove(self, data):
    	if not self.head:
        	return False

    	curr = self.head
    	prev = None

    	while True:
        	if curr.data == data:
            	if curr == self.head and curr.next == self.head:
                	self.head = None
            	elif curr == self.head:
                	tail = self.head
                	while tail.next != self.head:
                    	tail = tail.next
                	tail.next = curr.next
                	self.head = curr.next
            	else:
                	prev.next = curr.next
            	self.size -= 1
            	return True

        	prev = curr
        	curr = curr.next

        	if curr == self.head:
            	break
    	return False

	def replace(self, old, new):
    	removed = self.remove(old)
    	if removed:
        	return self.append(new)
    	return False


