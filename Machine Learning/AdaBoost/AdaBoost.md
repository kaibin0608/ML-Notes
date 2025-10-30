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
- we will make these predictions based on a patient's **Chest Pain** and **Blocked Artery** status and their **Weight**

![alt text](image-7.png)
- the first thing we do is give each sample a weight that indicates how important it is to be correctly classified
- **Note:** The **Sample Weight** is different from the **Patient Weight**

![alt text](image-8.png)

1. At the start, all samples get the same weight , 1 / total number of samples = 1/8, and that makes the samples all equally important. However, after we make the first stump, these wright will change in order to guide how the next stump created.

2. Now we need to make the first stump in the forest,this is done by finding the variable, **Chest Pain**, **Blocked Arteries** or **Patient Weight**, that does the best job classifying the samples.
    - >Note: Because all of the weights are the same, we can ignore them right now.

3. We start by seeing how well chest pain classifies the samples.

![alt text](image-9.png)
- Of the 5 samples with Chest Pain, 3 were correctly classified as having **Heart Disease**

![alt text](image-10.png)
- and 2 were incorrectly classified

![alt text](image-11.png)
- Of the 3 samples without Chest Pain, 2 were correctly classified as not having Heart Disease

![alt text](image-12.png)
- and 1 was incorrectly classified



4. Now we do the same for **Blocked Arteries**
![alt text](image-13.png)

5. And for **Patient Weight**

![alt text](image-14.png)

>Note: We used the techniques described in the Decision Tree StatQuest to determine that 176 was the best weight to separate the patients

6. Now we calculate the Gini index for the three stumps. 

![alt text](image-15.png)

- the Gini index for the **Patient Weight** is the lowest, so this will be the first stump in the forest.
- Now we need to determine how much say this stump will have in the final classification 

7. We determine how much say a stump has in the final classification based on how well it classified the samples.

![alt text](image-17.png)
- this stump made one error
- This patient, who weight less than 176, has heart disease, but the stump says they do not.
- The **Total Error** for a stump is the sum of weight associated with the incorrectly classified samples, Thus the **Total Error** here is 1/8


>**Note:** Because all of the **Sample Weights** add up to 1, **Total Error** will always be between 0, for a perfect stump, and 1, for a horrible stump.

- We use the **Total Error** to determine **Amount of Say** this stump has in the final classification with the following formula:

$$ \text{Amount of say} = \frac{1}{2} log(\frac{1 - \text{Total Error}}{\text{Total Error}}) $$

![alt text](image-16.png)

We can draw graph of **Amount of say** by plugging in a bunchof numbers between 0 and 1 for total error.
- The blue line tells us the **Amount of Say** for total Error values between 0 and 1
- When a stump does a good job, and the **Total Error** is small then the **Amount of Say** is relatively large positive value
- When a stump is no better at classification than flipping a coin (i.e. half of the samples are correctly classified and half are incorrectly classified) and **Total Error** = 0.5 then the **Amount of Say** is 0
- When a stump does a terrible job and the **Total Error** is close to 1, ie: if the stump consistently gives you the opposite classification then the **Amount of SAY** will be a large negative value
- So if a stump votes for "HEart Disease", the negative Amount of say will turn that vote into "Not Heart Disease".

>Note: If **Total Error** is 1 or 0, then this equation will freak out, in practice, a small error term is added to prevent this from hapenning 

8. with **Patient Weight**> 176, the **Total Error** is 1/8, so we just plug and calculate the **Amount of say**

$$ \text{Amount of say} = \frac{1}{2} log(7) = 0.97 $$

9. After we work out the **Amount of say** of **Weight**, we work it out for **Chest Pain** and **Blocked Arteries**, which are 0.42 and 0.
This is how we determine the amount of say 
