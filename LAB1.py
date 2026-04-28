# LAB1
# REMINDER: The work in this assignment must be your own original work and must be completed alone

#from turtle import up


def frequency(txt):
    '''
        >>> frequency('mama')
        {'m': 2, 'a': 2}
        >>> answer = frequency('We ARE Penn State!!!')
        >>> answer
        {'w': 1, 'e': 4, 'a': 2, 'r': 1, 'p': 1, 'n': 2, 's': 1, 't': 2}
        >>> frequency('One who IS being Trained')
        {'o': 2, 'n': 3, 'e': 3, 'w': 1, 'h': 1, 'i': 3, 's': 1, 'b': 1, 'g': 1, 't': 1, 'r': 1, 'a': 1, 'd': 1}
    '''
    # - YOUR CODE STARTS HERE -
    freq = {}
    for char in txt.lower():
        if char.isalpha():
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1
    return freq
    




def invert(d):
    """
        >>> invert({'one':1, 'two':2,  'three':3, 'four':4})
        {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
        >>> invert({'one':1, 'two':2, 'uno':1, 'dos':2, 'three':3})
        {3: 'three'}
        >>> invert({'123-456-78':'Sara', '987-12-585':'Alex', '258715':'sara', '00000':'Alex'}) 
        {'Sara': '123-456-78', 'sara': '258715'}
    """
    # - YOUR CODE STARTS HERE -
    inv = {}
    value_counts = {}
    for value in d.values():
        value_counts[value] = value_counts.get(value, 0) + 1

    for key, value in d.items():
        if value_counts[value] == 1:
            inv[value] = key
    return inv


    pass




def employee_update(d, bonus, year):
    """
        >>> records = {2020:{"John":["Managing Director","Full-time",65000],"Sally":["HR Director","Full-time",60000],"Max":["Sales Associate","Part-time",20000]}, 2021:{"John":["Managing Director","Full-time",70000],"Sally":["HR Director","Full-time",65000],"Max":["Sales Associate","Part-time",25000]}}
        >>> employee_update(records,7500,2022)
        {2020: {'John': ['Managing Director', 'Full-time', 65000], 'Sally': ['HR Director', 'Full-time', 60000], 'Max': ['Sales Associate', 'Part-time', 20000]}, 2021: {'John': ['Managing Director', 'Full-time', 70000], 'Sally': ['HR Director', 'Full-time', 65000], 'Max': ['Sales Associate', 'Part-time', 25000]}, 2022: {'John': ['Managing Director', 'Full-time', 77500], 'Sally': ['HR Director', 'Full-time', 72500], 'Max': ['Sales Associate', 'Part-time', 32500]}}
    """
    # - YOUR CODE STARTS HERE -
    first = True
    for y in d:
        if first:
            latest_year = y
            first = False
        elif y > latest_year:
            latest_year = y

    d[year] = {}
    for name, info in d[latest_year].items():
        role, status, salary = info
        d[year][name] = [role, status, salary + bonus]
    return d

    
    



def run_tests():
    import doctest
    
    print("Testing frequency:")
    assert frequency("mama") == {'m': 2, 'a': 2}
    assert frequency("We ARE Penn State!!!") == {'w': 1, 'e': 4, 'a': 2, 'r': 1, 'p': 1, 'n': 2, 's': 1, 't': 2}
    assert frequency("One who IS being Trained") == {'o': 2, 'n': 3, 'e': 3, 'w': 1, 'h': 1,'i': 3, 's': 1, 'b': 1, 'g': 1,'t': 1, 'r': 1, 'a': 1, 'd': 1}
    print("All tests passed!")

    
    
    print("Testing invert:")
    assert invert({'one':1, 'two':2, 'three':3, 'four':4}) == {
        1:'one', 2:'two', 3:'three', 4:'four'
    }
    assert invert({'one':1, 'two':2, 'uno':1, 'dos':2, 'three':3}) == {3:'three'}
    assert invert({'123-456-78':'Sara', '987-12-585':'Alex',
               '258715':'sara', '00000':'Alex'}) == {
        'Sara':'123-456-78', 'sara':'258715'
    }
    print("All tests passed!")

    
    print("Testing employee_update:")

    records = {
    2020:{
        "John":["Managing Director","Full-time",65000],
        "Sally":["HR Director","Full-time",60000],
        "Max":["Sales Associate","Part-time",20000]
    },
    2021:{
        "John":["Managing Director","Full-time",70000],
        "Sally":["HR Director","Full-time",65000],
        "Max":["Sales Associate","Part-time",25000]
    }
}

    updated = employee_update(records, 7500, 2022)

    assert updated[2022]["John"][2] == 77500
    assert updated[2022]["Sally"][2] == 72500
    assert updated[2022]["Max"][2] == 32500

    print("All tests passed!")








    # Run start tests in all docstrings
    #doctest.testmod(verbose=True)
    
    # Run start tests per function - Uncomment the next line to run doctest by function. Replace frequency with the name of the function you want to test
    #doctest.run_docstring_examples(frequency, globals(), name='LAB1',verbose=True)   

if __name__ == "__main__":
    run_tests()

