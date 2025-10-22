# inheritance
class Pet:
    def __init__(self,name, age):
        self.name = name 
        self.age=age

    def show(self):
        print(f"I am {self.name} and I am {self.age} years old")

    def speak(self):
        print("I don't know what I say")

class Cat(Pet):# we didnt define __init__ method, it still work fine, because we inherit Pet class to this class
    def __init__(self,name,age,color):
        # use this, we cannot rewrite the name and age defined before, we cannot redefine them
        super().__init__(name,age) # super() means we reference the super class, which is the pet class here, it will run whatever we have in the initialization
        self.color = color

    def speak(self):
        print("Meow")

    def show(self):
        print(f"I am {self.name} and I am {self.age} years old, I am {self.color}")

class Dog(Pet):
    def speak(self):
        print("Bark")

p = Pet("Tim",19)
p.show()
p.speak()
c = Cat("Bill",34,"Brown")
c.show()
c.speak() # will overwrite
d = Dog("Jill",25)
d.show()
d.speak()