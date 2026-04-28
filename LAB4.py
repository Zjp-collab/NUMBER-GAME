# LAB4
# REMINDER: The work in this assignment must be your own original work and must be completed alone.

class Node:   # You are not allowed to modify this class
    def __init__(self, value=None):  
        self.next = None
        self.value = value
    
    def __str__(self):
        return f"Node({self.value})"

    __repr__ = __str__

class Malloc_Library:

    """
    ** This is NOT a comprehensive test sample, test beyond this doctest
        >>> lst = Malloc_Library()
        >>> lst
        <BLANKLINE>
        >>> lst.malloc(5)
        >>> lst
        None -> None -> None -> None -> None
        >>> lst[0] = 23
        >>> lst
        23 -> None -> None -> None -> None
        >>> lst[0]
        23
        >>> lst[1]
        >>> lst.realloc(1)
        >>> lst
        23
        >>> lst.calloc(5)
        >>> lst
        0 -> 0 -> 0 -> 0 -> 0
        >>> lst.calloc(10)
        >>> lst[3] = 5
        >>> lst[8] = 23
        >>> lst
        0 -> 0 -> 0 -> 5 -> 0 -> 0 -> 0 -> 0 -> 23 -> 0
        >>> lst.realloc(5)
        >>> lst
        0 -> 0 -> 0 -> 5 -> 0
        >>> other_lst = Malloc_Library()
        >>> other_lst.realloc(9)
        >>> other_lst[0] = 12
        >>> other_lst[5] = 56
        >>> other_lst[8] = 6925
        >>> other_lst[10] = 78
        Traceback (most recent call last):
            ...
        IndexError
        >>> other_lst.memcpy(2, lst, 0, 5)
        >>> lst
        None -> None -> None -> 56 -> None
        >>> other_lst
        12 -> None -> None -> None -> None -> 56 -> None -> None -> 6925
        >>> temp = lst.head.next.next
        >>> lst.free()
        >>> temp.next is None
        True
    """

    def __init__(self): # You are not allowed to modify the constructor
        self.head = None
    
    def __repr__(self):  # You are not allowed to modify this method
        current = self.head
        out = []
        while current != None:
            out.append(str(current.value))
            current = current.next
        return " -> ".join(out)

    __str__ = __repr__
    
    def __len__(self):
        # --- YOUR CODE STARTS HERE
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count
        pass  # remove when starting implementation 

    
    def __setitem__(self, pos, value):
        # --- YOUR CODE STARTS HERE
        if pos < 0:
            raise IndexError("Negative index is not allowed")
        current = self.head
        index = 0

        while current is not None:
            if index == pos:
                current.value = value
                return
            current = current.next
            index += 1
        
        raise IndexError("Index out of bounds")
        pass  # remove when starting implementation 


    def __getitem__(self, pos):
        # --- YOUR CODE STARTS HERE
        if pos < 0:
            raise IndexError("Negative index is not allowed")
        current = self.head
        index = 0

        while current is not None:
            if index == pos:
                return current.value
            current = current.next
            index += 1

        raise IndexError("Index out of bounds") 
    

    def malloc(self, size):
        # --- YOUR CODE STARTS HERE
        self.head = None

        if size <= 0:
            return
        
        self.head = Node(None)
        current = self.head

        for _ in range(size - 1):
            current.next = Node(None)
            current = current.next


    def calloc(self, size):
        # --- YOUR CODE STARTS HERE
        self.head = None

        if size <= 0:
            return
        
        self.head = Node(0)
        current = self.head

        for _ in range(size - 1):
            current.next = Node(0)
            current = current.next


    def free(self):
        # --- YOUR CODE STARTS HERE
        current = self.head

        while current is not None:
            temp = current.next
            current.next = None
            current = temp

        self.head = None


    def realloc(self, size):
        # --- YOUR CODE STARTS HERE
        if self.head is None:
            if size > 0:
                self.malloc(size)
            return
        
        if size == 0:
            self.free()
            return
        
        length = len(self)

        if size > length:
            current = self.head
            while current.next is not None:
                current = current.next
            
            for _ in range(size - length):
                current.next = Node(None)
                current = current.next

        elif size < length:
            current = self.head
            prev = None
            index = 0

            while index < size:
                prev = current
                current = current.next
                index += 1

            prev.next = None

            while current is not None:
                temp = current.next
                current.next = None
                current = temp



    def memcpy(self, ptr1_start_idx, pointer_2, ptr2_start_idx, size):
        # --- YOUR CODE STARTS HERE
        if self.head is None or pointer_2.head is None:
            return
        if ptr1_start_idx < 0 or ptr2_start_idx < 0:
            return
        
        src = self.head
        for _ in range(ptr1_start_idx):
            if src is None:
                return
            src = src.next

        dest = pointer_2.head
        for _ in range(ptr2_start_idx):
            if dest is None:
                return
            dest = dest.next
        
        count = 0
        while src is not None and dest is not None and count < size:
            dest.value = src.value
            src = src.next
            dest = dest.next
            count += 1
    


def run_tests():
    import doctest
    doctest.testmod(verbose=True)
     

if __name__ == "__main__":
     run_tests()