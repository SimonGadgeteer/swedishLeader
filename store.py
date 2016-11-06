import register_usage
values = {}

def storeValues(key, value):
    print("I'll store "+key+" with the value "+value)
    values[key] = value
    register_usage.registerUsage()
    print("the store now looks like this: "+str(values))

    return "I'll store "+key+" with the value "+value

def getValues():
    return str(values)