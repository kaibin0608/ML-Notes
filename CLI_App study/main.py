import click

# example
# myprogram myfunction --name akjbra --other ajsdavkbj -l -k

@click.group() # group all the functions together to run in one command line
def mycommands():
    pass

@click.command() # register hello as command
@click.option("--name", prompt="Enter your name: ", help ="The name of the user") # define the option params
def hello(name):
    click.echo(f"Hello {name}!")

PRIORITIES = {
    "o":"Optional",
    "l":"Low",
    "m":"Medium",
    "h":"High",
    "c":"Crucial"
}

@click.command()
@click.argument("priority",type = click.Choice(PRIORITIES.keys()),default='m') # specify arguments choices
@click.argument("todofile",type=click.Path(exists=False),required = 0) # use this when we need to add arguments
@click.option("-n","--name",prompt ="Enter the todo name",help = "The name of the todo item")
@click.option("-d","--desc",prompt ="Describe the todo",help = "The description of the todo item")
def add_todo(name, desc, priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "a+") as f: #a+ means appending plus mode, means we append to the file, if doesnt exist, we create one
        f.write(f"{name}: {desc} [Priority: {PRIORITIES[priority]}]\n")

@click.command()
@click.argument("idx",type = int, required=1)
def delete_todo(idx):
    with open("mytodos.txt","r")as f:
        todo_list = f.read().splitlines() #.splitlines() , after each linebreak we will ahve a new item
        todo_list.pop(idx) # remove an item according to index 'idx' and return 
    with open("mytodos.txt","w") as f: # open in writing mode because we need to rewrite the file with other text
        f.write("\n".join(todo_list))
        f.write('\n')

@click.command()
@click.option("-p","--priority",type=click.Choice(PRIORITIES.keys()))
@click.argument("todofile",type=click.Path(exists = True), required = 0) # = 0 becasue we will take the default if is doesn't specified
def list_todos(priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename,"r") as f:
        todo_list = f.read().splitlines()
    if priority is None:
        for idx, todo in enumerate(todo_list):
            print(f"({idx}) - {todo}")
    else:
        for idx, todo in enumerate(todo_list):
            if f"[Priority: {PRIORITIES[priority]}]" in todo:
                print(f"({idx}) - {todo}")

mycommands.add_command(hello)
mycommands.add_command(add_todo)
mycommands.add_command(delete_todo)
mycommands.add_command(list_todos)

if __name__ == "__main__":
    # hello()
    mycommands()

################################################
#  Command line
################################################

# python main.py --help 
# python main.py add-todo --help
# python main.py add-todo --name "Test priority" --desc "just another test" h anotherfile.txt
# python main.py delete-todo 1  
# python main.py list-todos -p m 
