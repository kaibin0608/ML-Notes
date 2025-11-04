# Gradient Boost 

## (Part1) Gradient Boost for Regression

Context: 

We will use this dataset

![alt text](image.png)

> Note: When **Gradient Boost** is used to Predict a continuous value, like **Weight**, we say that we are using **Gradient Boost** for regression

This StatQuest focuses on showing you the most common way Gradient Boost is used to predict a continuous value like **Weight**

### Compare and contrast **AdaBoost** and **Gradient Boost**

![alt text](image-1.png)

If we want to use these measurement to predict **Weight** ,

**AdaBoost** 
- starts by building a very short tree, called a **Stump**, from the training data 
- and the amount of say that the stump has on the final output is based on how well it cmopensate for those previous errors.
- Then build the next stump based on errors that the previous stump made until a specify amount of stump or until it perfectly fit.

![alt text](image-2.png)

**Gradient Boost**
- starts by making a single leaf, instead of a tree or stump
- This leaf represents an initial guess for the **Weights** of all of the samples.
- When trying to **Predict** a continuous value like **Weight**, the first guess is the average value.
- then **Gradient Boost** builds a tree, like AdaBoost, this tree is based on the error made by the previous tree but unlike Adaboost, this tree is usually larger than a stump
- That's said, gradient boost still restrict the size of the tree 

>In the simple example that we will go through in this StatQuest, we will build trees with up to four leaves but no larger. However, in practice, people often set the maximum number of leaves to between 8 and 32

Thus, like **AdaBoost**, **Gradient Boost** Builds fixed sized trees based on the previous tree's error, but unlike **AdaBoost**, each tree can be larger than a stump

Also like **AdaBoost**, **Gradient Boost** scales the trees. However, **Gradient Boost** scales all trees by the same amount. 

Then **Gradient Boost** builds another tree based on the errors made by the previous tree and then it scales the tree. And **Gradient Boost** continues to build trees in this fashion until it has made the number of trees you asked for, or additional trees fail to improve the fit

### The most common **Gradient Boost** configuration

let's see how the most common Gradient Boost configuration would use this Training Data to Predict Weight

![alt text](image-3.png)

The first thing we do is to calculate the average weight, this is the first attempt at predicting everyone's weight. $\text{Average Weight} = 71.2$ In other words, if we stopped right now, we would predict that everyone weighed 71.2 kg. However, Gradient boost doesn't stop here

![alt text](image-4.png)

The next thing we do is build a tree based on the errors from the first tree. The **error** that the previous tree made are the differences between the **Observed Weights** and the **Predicted Weight**(71.2). so lets start by plugging in the predicted weight and observed weight and do the maths

$$
\begin{align*}
(\text{Observed Weight} - \text{Predicted Weight}) 
&= (88 - 71.2) \\
&= 16.8 \\
\end{align*}
$$

![alt text](image-5.png)

and save the difference which is called the **Pseudo Residual**, in a new column.

![alt text](image-6.png)

> Note: The term **Pseudo Residual** is based on **Linear Regression**, where the difference between the **Observed** vales and the **Predicted** values results in **Residuals**

> The "Pseudo: part of Pseudo Residual is a reminder that we are doing Gradient Boost, not Linear Regression

Now we do the same thign for the remaining weight

![alt text](image-7.png)

Now we will build a Tree using **Height**, **Favourite Color** and **Gender** to predict the residuals.

![alt text](image-8.png)

Setting aside the reason why we are building a tree to predict the residuals for the time being, here's the tree. In the example, we are only allowing up to four leaves but when using a larger dataset, it is common to allow anywhere from 8 to 32 

By restricting the total number of leaves, we get fewer leaves than residuals.

![alt text](image-9.png)

As a result, these two rows of data go to the same leaf.

![alt text](image-10.png)

so we replace these residuals with their average.

$$ \frac{(-14.2-15.2){2} = -14.7} $$

![alt text](image-11.png)

And these two rows of data go to the same leaf, so we replace the residuals with the average (1.8+5.8)/2 = 3.8

![alt text](image-12.png)

Now we can combine the original leaf with the new tree to make a new prediction of an individual's *Weight** from the **Training Data**

We start with the initial **Prediction**,71.2