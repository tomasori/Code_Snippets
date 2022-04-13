'''
Source:
https://stackoverflow.com/questions/71857924/checking-all-user-input-for-a-specific-value
'''

def say_hi():
    print('Hi!')

def bah_humbug():
    print('Bah Humbug!')


# dict with function names
list_of_functions = {"good": say_hi,
     "bad": bah_humbug}


greeting = 'bad'

# gets function name and calls it.
list_of_functions[greeting]()
