# Gradient Boost for Classification

When **Gradient boost** is use for **classification** it has a lot in common of **logistic regression**.

Context: 

![alt text](image-63.png)

We will use this **Training Data** which include popcorn preference, age, favorite color, and whether or not they love the movie **Troll 2**and walk through the most common way that **Gradient Boost** fits a model to this **Training Data**

## Calculate Log(odds)

Just like in **Part 1**, we start with a leaf that represents an initial **Prediction** for every individual.

When we use **Gradient Boost for Classification**, the initial **Prediction** for every individial is the **log(odds)**
> think of the log(odds) as the **Logistic Regression** equivalent of the average

So let's calculate the overall **log(odds)** that someone **Loves Troll 2**

Since 4 people in the Training Dataset **Loves Troll 2** and 2 people do not, then the **log(odds)** that someone **loves Troll 2** is $log(\frac{4}{2}) = 0.7$ which we will put into our initial leaf.

![alt text](image-64.png)
- This is the initial **Prediction**

### How do we use this for **Classification**? 

Just like with **Logistic Regression**, the easiest way to use the **Log(Odds)** for **Classification** is to convert it to a **Probability** and we do that with a **Logistic Function**

$$\text{ Probability of Loving Troll 2} =\frac{e{log(odds)}}{1+ e^log(odds)}$$

so we plug in the **log(odds)** into the **Logistic Function**

$$\text{ Probability of Loving Troll 2} =\frac{e^{log(\frac{4}{2})}}{1+ e^{log(\frac{4}{2})}} = 0.7$$

> Note: These two numbers, the log(4/2) and the **Probability** are the same only because I am rounding. If I allowed 4 digits passed the decimal place

$$log(\frac{4}{2}) = 0.6931$$

$$ \frac{e^{log(\frac{4}{2})}}{1+ e^{log(\frac{4}{2})}} = 0.6667$$

Since the **Probability** of Loving Troll 2 is greater than 0.5, we can **Classify** everyone in the Training Dataset as someone who **Loves Troll 2**.

> Note: While 0.5 is a very common threshold for making **Classification** decisions based on **Probability**, we could have just as easily used a different value. 

Now, Classifying everyone in the Training Dataset as someone who **Loves Troll 2** is pretty lame, because two of the people do not love the movie.

We can measure how bad the initial **Prediction** is by calculating **Pseudo Residuals**, the difference between the **Observed** and the **Predicted** values.

$$\text{Residual = Observed - Predicted}$$

Although the math is easy, i think it's easier to grasp what's going on if we draw the **Residuals** on a graph.

![alt text](image-65.png)

- The **Predicted Probability of Loving Troll 2** is 0.7 (the dotted line)
- The **Red Dots**, with the **Probability of Loving Troll 2 = 0**, represent the two people that do not Love Troll 2
- and the **Blue Dots**, with a **Probability of Loving Troll 2 = 1**, represent the four people that **Love Troll 2**

![alt text](image-66.png)

So for this sample, we plug in one for the **Observed** value, and 0.7 for the **Predicted** value, and we get 0.3. Then we calculate the rest of the **Residuals**

![alt text](image-67.png)

We have calculated the **Residuals** for the leaf's initial **Prediction**

Now we build a **Tree**, using **Likes popcorn, Ages and Favorite Color** to predict the residuals

![alt text](image-68.png)

and here is the tree.

> Note: Just like when we used **Gradient Boost for Regression**, we are limiting the number of leaves that we will allow in the tree

In this simple example, we are limiting the number of leaves to 3

In practice people often set the maximum number of leaves to between 8 and 32

Now let's calculate the **Output Values** for the leaves

![alt text](image-69.png)

> Note: These three rows of data, goes to the same leaf

![alt text](image-70.png)
> These two rows of data, goes to the same leaf

![alt text](image-71.png)
> lastly, this row of data, goes to its own leaf

When we use **Gradient Boost** for **Regression**, a leaf with single **Residual** had an **Output Value** equal to that **Residual**

In contrast, when we use **Gradient Boost** for **Classification**, the situation is a little more complex. This is because the **Predictions** are in terms of the **log(odds)**

![alt text](image-72.png)

and this leaf is derived from a **Probability**, so we can't just add them together and get a new **Log(odds) Prediction** without some sort of transformation

When we use **Gradient Boost** for **Classification**, the most common transformation is the following formula

$$ 
\frac{\sum_i \text{Residual}_i}{\sum_i \left[ \text{Previous Probability}_i \times (1 - \text{Previous Probability}_i) \right]}
$$

- The numerator is the sum of all of the **Residuals** in the leaf
- The denominator is the sum of the previously predicted probabilities for each **Residual** times 1 minus the same predicted probability.

![alt text](image-73.png)

Since there is only one **Residual** in this leaf, we can ignore these summation signs for now.

So we plug in the residuals from the leaf, and since we are building the first tree, the **Previous Probability** refers to the probability from the initial leaf, 0.7

$$ 
\frac{-0.7}{0.7 \times (1 - 0.7)} = -3.3
$$

![alt text](image-74.png)

and we end up with -3.3 as the new **Output value** for this leaf. 

![alt text](image-75.png)

Now we need to calculate the **Output Value** for this leaf.

Since we have two **Residuals** in the leaf, we all them together in numerator

$$ 
\frac{0.3 - 0.7}{(0.7 \times (1 - 0.7)) + (0.7 \times (1 - 0.7))} = -1
$$

> Note: For now, the **Previous Probabilities** are the same for all of the **Residuals**, but this will change when we build the next tree.

and the **Output Value** for this leaf is -1