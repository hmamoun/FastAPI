def decorator_list(fnc):
    def inner(list_of_tuples):
        return[fnc(val[0],val[1]) for val in list_of_tuples]
    return inner

@decorator_list
def add_together (a,b):
    return a+b



x = [(1,2),(3,5),(3,56,4),(34,555)]

#print([a[1],a[0]] for a in x)


print(add_together(x))





