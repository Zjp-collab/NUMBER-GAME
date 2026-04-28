def sum_evens(numList):
    """
    Traverses numList and returns the accumulated sum of all the even numbers present in the sequence.

    Preconditions:
        numList --> list: a non-empty list of numbers
    Postconditions:
        returns --> float: the sum of even numbers in numList

    Examples:
    >>> sum_evens([1, 2, 3, 4, 5, 6])
    12.0
    >>> sum_evens([10, 15, 20, 25])
    30.0
    >>> sum_evens([1, 3, 5])
    0.0
    >>> sum_evens([2, 4, 6, 8, 10])
    30.0
    >>> sum_evens([7])
    0.0
    >>> sum_evens([95, 70, 6, 86, 47])
    162.0
    >>> sum_evens([-32, 67, 54, 49, -90, 58, 41, -55, -6, 31, -5, -21, 39, 77, -40, -35, -32, -70, -51, 11])
    -158.0
    >>> sum_evens([34, 59, 0, 56, -10, 39, 73, -4, 30, 83, 51, 1, 47, 88, 20])
    214.0
    """
    # -- YOUR CODE STARTS HERE
    total = 0.0  # Make the sum a float from the start
    for num in numList:
        if num % 2 == 0:
            total += num
    return total

if __name__ == "__main__":
    import doctest
    doctest.testmod()

