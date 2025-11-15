# Gradient Boost (Part 4)

In this StatQuest, we will walk through the original **Gradient Boost** algorithm for **classification**, step-by-step. Just like in Part 2 of this series, we will use an incredibly small **Training Dataset** for the examples.

![alt text](image-101.png)

The small size will help us focus on the algorithm's details, but it will mean using stumps instead of larger trees.

However, by now you know what in practice **Gradient Boost** usually uses trees with between 8 and 32 leaves.

## Input data

### Data ${(x_i,y_i)}^n_{i=1}$ , and a differentiable **Loss Function** $L(y_i, F(x))$

$${(x_i,y_i)}^n_{i=1}$$
- $x_i$ refers to a row of measurements that we will use to **Predict** if someone **Loves Troll 2**
- $y_i$ refers whether or not someone **Loves Troll 2**

The easiest way to understand the most commonly used **Loss Function** for classification is to show how it words on a graph.

![alt text](image-102.png)
- <span style="color:red">**Red Dot**</span>, with the **Probability of Loving Troll 2** =0, represents the one person that **Does not Love Troll 2
- <span style="color:blue">**Blue Dots**</span>, with a **Probability of Loving Troll** =1, represent the two people that **Love Troll 2**
- In other words, the **Red** and **Blue** dots are observed values and we can draw a dotted line to represent the predicted probability that someone **Loves Troll 2**

![alt text](image-103.png)

In this example, I have set the predicted probability to 0.67

Now, just like we do for **Logistic Regression**, we can calculate the **Log(likelihood)** of the data given the predicted probability

$$ \text{Log(Likelihood of the Observed Data given the Prediction)} \\
= \sum_{i=1}^{N} [ y_i \log(p) + (1 - y_i)\log(1 - p) ] 
$$
- the $p$'s refer to the predicted probability, which is 0.67 in this example
- and the $y_i$'s refer to the **Observed** values for **Loves Troll 2**
- for two people who **Love Troll 2**, $y_i = 1$, which means that $(1 - y_i)\log(1 - p)$ will be 0, leaving just the $log(p)$
- In contrast, for the one person who does not **Love Troll 2**, $y_i=0$, which means this term will be 0.

Now let's use the summation to calculate the **Log(likelihood)** of all three **Observe** values. 

![alt text](image-104.png)

We will start by calculating the **log(likelihood)** for the first person. Because this person Love Troll 2, $y_1 = 1$

$$
[ y_1 \log(p) + (1 - y_1)\log(1 - p) ] = 1 \times \log(1 - p) + (1 - 1) \times \log(1 - p)
$$

![alt text](image-105.png)

then we plug in 0.67 for the predicted probability, $p$

$$
\begin{align*}
[ y_1 \log(p) + (1 - y_1)\log(1 - p) ] &= 1 \times \log(1 - 0.67) + (1 - 1) \times \log(1 - 0.67) \\
&= \log(0.67)
\end{align*}
$$

and the **log(likelihood)** for the first person, given the predicted probability, is the $\log(0.67)$

Now let's  to calculate the **Log(likelihood)** of the second person.

![alt text](image-106.png)

we plug in the value of $y_2 = 1$ and plug in 0.67 for the predicted probability, $p$

$$
\begin{align*}
[ y_2 \log(p) + (1 - y_2)\log(1 - p) ] &= 1 \times \log(1 - 0.67) + (1 - 1) \times \log(1 - 0.67) \\
&= \log(0.67)
\end{align*}
$$

and then we get the $\log(0.67)$ since the predicted probability was the same 

![alt text](image-107.png)

Now let's calculate the **log(likelihood)** for the third person

We plug in the **Observed Value**, 0 for $y_3$ since this person does not love the movie.Also, plug in the $p=0.67$

$$
\begin{align*}
[ y_3 \log(p) + (1 - y_3)\log(1 - p) ] &= 0 \times \log(1 - 0.67) + (1 - 0) \times \log(1 - 0.67) \\
&= \log(1 - 0.67)
\end{align*}
$$

> Note: The better the prediction, the larger the log(likelihood), and this is why, when doing **Logistic Regression**, the goal is to maximize the **log(likelihood)**

>That means that if we want to use the log(likelihood) as **Loss Function**, where smaller values represent better fitting models, then we need to multiply the **log(likelihood)** by **-1** 

$$ - \text{Log(Likelihood of the Observed Data given the Prediction)} \\
= - \sum_{i=1}^{N} [ y_i \log(p) + (1 - y_i)\log(1 - p) ] 
$$

So, we will put this subtle, but very impotant minus sign in front of everything. And since a **Loss Function** sometimes only deals with one sample at a time, we can get rid of the summation, and to make it easier to readm we will replace $y$ with $Observed$

$$-[ \text{Observed} \times \log(p) + (1 - \text{Observed}) \times \log(1 - p) ] $$

Now we need to transform this equation, the **negative log(likelihood)**, so that it is a function of the predicted **log(odds)** instead of the predicted probability, $p$ and we need to simplify it.

Simplify:

$$
\begin{align*}
& - \left[ \text{Observed} \times \log(p) + (1 - \text{Observed}) \times \log(1 - p) \right] \\
&= -\text{Observed} \times \log(p) - (1 - \text{Observed}) \times \log(1 - p) \\
&= -\text{Observed} \times \log(p) - \log(1 - p) + \text{Observed} \times \log(1 - p) \\
&= -\text{Observed} \times \left[\log(p) - \log(1 - p)\right] - \log(1 - p) \\
&= -\text{Observed} \times \log(\text{odds}) - \log(1 - p)
\end{align*}
$$

>Note: The relationship between probability, $p$, and the **log(odds)** is derived in the **StatQuest** on odds and log(odds), so check that out if you want more details. $ log(\frac{p}{1-p}) = log(odds)$

Now we need to convert **log(1-p)** into a function of the **log(odds)**. 

Now, we replace 1 with this fraction do the subtraction, then convert the division into subtraction, and since the log(1) = 0, we can remove it 

$$ 
\begin{align*}
log(1-p) &= log(1- \frac{e^{log(odds)}}{1+ e^{log(odds)}}) \\
&= log(\frac{1+ e^{log(odds)}}{1+ e^{log(odds)}}- \frac{e^{log(odds)}}{1+ e^{log(odds)}}) \\
&= log(\frac{1}{1+ e^{log(odds)}}) \\
&= log(1) - log(1 + e^{log(odds)}) \\
&= - log(1 + e^{log(odds)}) 
\end{align*}$$

> Note: The relationship between probability, $p$, and the **log(odds)** is derived in the **Logistic Regression StatQuest** on estimating parameters with **Maximum Likelihood**

Thus, the **log(1-p)**, which is a function of the predicted probability, p, can be transformed into a function of the predicted **log(odds)**, so lets plug that in 

$$
\begin{align*}
& - \left[ \text{Observed} \times \log(p) + (1 - \text{Observed}) \times \log(1 - p) \right] \\
&= -\text{Observed} \times \log(p) - (1 - \text{Observed}) \times \log(1 - p) \\
&= -\text{Observed} \times \log(p) - \log(1 - p) + \text{Observed} \times \log(1 - p) \\
&= -\text{Observed} \times \left[\log(p) - \log(1 - p)\right] - \log(1 - p) \\
&= -\text{Observed} \times \log(\text{odds}) - \log(1 - p)\\
&= - \text{Observed} \times log(odds) + log( 1+ e^{log(odds)})
\end{align*}
$$

>Note : the sign changed from negative(line 5) to positive(line 6) because we replaced **log( 1 - p )** with $-log(1+e^{log(odds)})$

We converted the negative **log(likelihood)** of the data, which is a function of the predicted probability, $p$ into a function of predicted **log(odds)**. So
$$ - \text{Observed} \times log(odds) + log( 1+ e^{log(odds)}) $$
is the **Loss Function**. Now we just need to show that it is differentiable

So let's take the derivative of the **Loss Function** with respect to predicted **log(odds)**

$$
\begin{align*}
&\frac{d}{d \log(odds)} -\text{Observed} \times \log(odds) + log( 1+ e^{log(odds)}) \\
&= -\text{Observed} + \frac{1}{1+ e^{log(odds)}}\times e^{log(odds)} \\ 
&= -\text{Observed} + \frac{e^{log(odds)}}{1+ e^{log(odds)}} \\ 
&= -\text{Observed} + p
\end{align*}
$$

> Note: Earlier we saw that we can substitute the predicted probability, $p$, with this fraction $\frac{e^{log(odds)}}{1+ e^{log(odds)}}$ but we can also swap the predicted probability, $p$, back in

As we will soon see, sometimes it's easier to use the function of the **logg=(odds)** and sometimes it's easier to use the function of the probability,$p$.

![alt text](image-108.png)

In summary, the input data is the **Training Dataset** 

![alt text](image-109.png)

and this is just a transformation of the negative **log(likehood)**, is the differentiable **Loss Function** and the derivative can be a function of the predicted **log(odds)** or a function of the predicted probability, $p$

![alt text](image-110.png)

## Step 1

### Initialize model with a constant value: 

$$F_0(x) = argmin_\gamma \sum^n_{i=1} L(y_i,\gamma)$$

Just like when we used **Gradient Boost** for  **Regression**, we need to come up with the initial **Prediction** and just like before, we will use this funky looking equation to find the optimal initial **Prediction**

![alt text](image-111.png)

this is just the **Loss Function**
- $y_i$ refers to the **Observed** values
- $\gamma$ refers to a **log(odds)** value
- in theory, we could go ahead and replace the **Log(odds)** with **gamma** but it's actually easier to see what's going on if we leave the **log(odds)** in and remember that it represents **Gamma**
- The summation means that we add up one **Loss function** for each **Observed** value
- The "argmin over gamma" means we need to find a **log(odds)** value that minimizes this sum

The first thing we do is take the derivative of each term with respect to the **Log(odds)**

![alt text](image-112.png)![alt text](image-113.png)

Now, to make the next steps super easy, let's replace the **log(odds)** with the predicted probability, $p$ 

![alt text](image-114.png)

set the sum of the derivatives equal to zero

![alt text](image-115.png)

and solve.

$$
\begin{align*}
-1 + p -1 + p - 0 + p &= 0 \\
-2 + 3 \times p &= 0 \\
 p &= \frac{2}{3}
\end{align*}
$$

![alt text](image-116.png)

and we end up with the $\frac{2}{3}$ for the initial predicted probability, $p$, because 2 people **Love Troll 2** and there are 3 people in the **Training Dataset**

