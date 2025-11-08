# Gradient Boost (Part 2)

We are going to walk through the original **Gradient Boost** step-by-step. In order to keep the example from getting out of hand, we are going to use Gradient Boost to fit a model to super simple **Training Dataset**

![alt text](image.png)

which contains the **Height** measurements, **Favorite colour**,**gender** and **Weight** from three people.

## Gradient Descent algorithm

### Input:

Data ${(x_i , y_i)}^n_{i=1}$, and differentiable **Loss Function** $L(y_i,F(x))$

This line describes the **Training Dataset**, and the method we will use to evaluate how well the model fits the **Training Dataset**

![alt text](image-26.png)

> Data : ${(x_i , y_i)}^n_{i=1}$
- $x_i$ refer to each row of measurements that we will use to predict **Weight**
- $ y_i$ refers to the **Weights** measured for the each person in the dataset
- the $n$ and $i=1$ says that the $X_i$ and $y_i$ go from 1 to $n$, where $n$ is the number of people in our dataset,$n=3$.

> $L(y_i,F(x))$
- **Loss Function** is just something that evaluates how well we can predict **Weight**
- The Lost Function that is most commonly used when doing **Regression** with **Gradient Boost** is 
$$ \frac{1}{2} (\text{Observed} - \text{Predicted})^2 $$

- When we remove the 1/2, we end up with the sa,e **Loss Function** we use for **Linear Regression**
$$ (\text{Observed} - \text{Predicted})^2 $$

![alt text](image-27.png)

For Example, if we had Height and Weight measurements from three people, then we could fit a line to the data.
- Residuals are the difference between the **Observed** Weights and the Weights that are **Predicted** by the line

![alt text](image-28.png)

We can evaluate how well this **Greenish Line** fits the data with the sum of squared **Residuals**.

Thus, the **Loss Function** is just a squared **Residual** $ (\text{Observed} - \text{Predicted})^2 $. If want to compare between two lines, we can just compare the **Sum of the Squared Residuals**

![alt text](image-29.png)

>Note: If i multipled both sides of the formulas by $\frac{1}{2}$ then we would get smaller numbers but we wil still know that the **Greenish Line** fits the data better since its number is still relatively smaller. So it doesn't matter

The reason why people choose this **Loss Function** for **Gradient Boost** is that when we differentiate with respect to "Predicted" and use **The Chain Rule** and bring the square down to the front and multiply by the derivative of **-Predicted**, which is -1, and $\frac{2}{2}$ cancel out, and that leaves you with the $-(\text{Observed} - \text{Predicted})$

$$ 
\begin{align*}
& \frac{d}{d(Predicted)} \frac{1}{2} (\text{Observed} - \text{Predicted})^2 \\
&=\frac{2}{2} (\text{Observed} - \text{Predicted}) \times -1 \\
&= -(\text{Observed} - \text{Predicted})
\end{align*}
$$

In other words, we are left with the negative **Residual**, and this makes the math easier since **Gradient Boost** uses the derivative a lot
- $y_i$ is the observed value
- $F(x)$ is the function that gives us the **Predicted** values

These will be the Input for the **Gradient Boost** algorithm
- Data
- differentiable Loss Function

### Step 1: 

**Initialize model with a constant value: $F_0(x) = \text{argmin}_{\gamma} \sum^n_{i=1} L(y_i , \gamma)$**
- we start by initializing the model with a constant value that is determined by $F_0(x)$
- $L(y_i , \gamma)$ this is the Loss function, $y_i$ refers to the **Observed** values, and $\gamma$ refers to **Predicted** values.
- The summation means that we add up one **Loss Function** for each **Observed** value
- "argmin over gamma" means we need to find a **Predicted** value that minimizes the sum

![alt text](image-30.png)

Here is a plot of one half of the sum of the squared residuals for potential **Predicted** values

>Note: We could use the **Gradient Descent** to find the optimal value for **Predicted** but we also can just solve for it, because the math isn't that hard.

![alt text](image-31.png)

The first thing we do is take the derivative of each term with respect to **Predicted**. Since we already showed how to take the derivaticve of our **Loss Function**, we can just plug it in.

![alt text](image-32.png)

Then we set the sum og the derivative equals to 0, then solve for the **Predicted**

$$
\begin{align*}
-(88 - \text{Predicted}) + -(76 - \text{Predicted}) + -(56 - \text{Predicted}) &= 0 \\
\text{Predicted} &= \frac{88+76+56}{3} 
\end{align*} 
$$

the value of $\gamma$ is the average of the **Observed Weights**. So the value of $ \gamma $ that minimizes the sum Loss function is the average of the **Observed Weights**

$$
F_0(x) = \frac{88+76+56}{3} = 73.3
$$

We have now created the initial predicted value is 73.3. That means that initial predicted value $F_0(x)$, is just a leaf. The leaf predicts that all samples will weigh 73.3.

We finised Step 1! We initialized the model with a constant value,73.3. In other words, we created a leaf that predicts all samples will weigh 73.3

### Step 2

![alt text](image-34.png)

step 2 is a loop where we make all of the trees. In generic terms, we will make *M* trees, but in practice, most people set *M* = 100 and make 100 trees
- *m* refers to individual tree. So when *m* = 1, we are talking about first tree

#### (A) Calculating residuals

![alt text](image-36.png)

![alt text](image-35.png)

This part is just the derivative of the **Loss Function** with respect to the **Predicted** value

![alt text](image-37.png)

and we already calculated this. and there is a big minus sign, and taht leave us with the Observed value minus the Predicted value

$$(\text{Observed - Predicted})$$

Now we plug $F_{m-1}(x)$ in for **Predicted** and since *m* = 1 that means we plug in $F_0(x)$ for $F_{m-1}(x)$

$$(\text{Observed} - F_0(x))$$

and since $F_0(x)$ is just the leaf set to 73.3, we plug in 73.3

$$(\text{Observed} - 73.3)$$

Now we can compute $r_{i,m}$, where $r$ is short for **Residual**, *i* is the sample number and *m* us tge tree tthat we are trying to build.

![alt text](image-38.png)

This tells us to calculate **Residuals** for all 3 samples in the dataset.

---

So we will start with $r_{1,1}$ the **Residual** for the first sample (i=1) and the first tree (*m*=1)

we plug in the **Observed Weight** for the first sample

$$ r_{1,1} = (88 - 73.3) = 14.7 $$

Now we calculate $r_{2,1}$

$$ r_{2,1} = (76 - 73.3) = 2.7 $$

Now we calculate $r_{3,1}$

$$ r_{3,1} = (56 - 73.3) = -17.3 $$

![alt text](image-39.png)

We have finish Part A of Step 2 by calculating residual for each sample

![alt text](image-40.png)
> Note: this derivative is the **Gradient** that **Gradient Boost** is named after

> $r_{i,m}$ values are technically called **Pseudo Residuals**. When we

#### (B) Fit a regression tree

Fit a regression tree to the $r_{im}$ values and create terminal regions $R_{jm}$, for - = 1...$J_m$
- this means we will build a regression tree to predict the **Residuals** instead of **Weights**

![alt text](image-41.png)