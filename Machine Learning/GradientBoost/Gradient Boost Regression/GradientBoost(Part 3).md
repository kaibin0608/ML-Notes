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

Since 4 people in the Training Dataset **Loves Troll 2** and 2 people do not, then the **log(odds)** that someone **loves Troll 2** is $log(\frac{4}{2}) = 0.7$