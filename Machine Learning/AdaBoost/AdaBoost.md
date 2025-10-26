# AdaBoost
Let's start by using **Decision Trees** and **Random Forests** to explain the three main concepts behind **AdaBoost**

---

In Random Forest, 

![alt text](image.png)

- each time you make a tree, you make a full sized tree. Some trees might be bigger than others, but there is no predetermined maximum depth. 
- each tree has an equal vote on the final classification 
- each decision tree is made independently of the others, in other word, it doesn't matter which three was made first

![alt text](image-1.png)

In contrast, in a **Forest of Trees** made with **AdaBoost**, 
- the trees are usually just a **node** and two **leaves**
- in a **Forest of Stumps** made with **AdaBoost**, some stumps get more say in the final classification than others
    - ![alt text](image-6.png)
    - in this illustration, the larger stumps get more say in the final classification than the smaller stumps
- **Forest of Stumps** made with **AdaBoost**, the order is important
    - The erroes that the first stump makes influence how the second stump is made
---

Terminology:
- **Stump**: A tree with just one node and two leaves
    - Stumps are not great at making accurate classifications 

![alt text](image-2.png)

---

![alt text](image-3.png)

For examples, if we were using this data to determine if someone had heart disease or no, then a full sized Dicision Tree would take advantage of all 4 variables that we measured (Chest Pain, Blood Circulation, Blocked Arteries and Weight) to make decision ...

![alt text](image-4.png)

but a Stump can only use one variable to make a decision
- Thus, **Stumps** are technically "weak learners"
- However, that's the way **AdaBoost** likes it, and it's one of the reasons why they are so commonly combined

## The three ideas behind Adaboost 

1. AdaBoost combines alot of "weak learners" to make classifications. The weak learners are almost always **stumps**

2. Some stumps get more say in the classification than the others

3. Each stump is made by taking the previous stump's mistakes into account.

## How to create a Forest of Stumps using AdaBoost

Context:

![alt text](image-5.png)

We create a **Foreast of Stumps** with AdaBoost to predict of a patient has heart disease 