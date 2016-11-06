import register_usage
values = []

def storeValues(key, value):
    print("I'll store "+key+" with the value "+value)
    values.append([key, value])
    register_usage.registerUsage()
    print("the store now looks like this: "+str(values))

def getValues():
    return str(values)