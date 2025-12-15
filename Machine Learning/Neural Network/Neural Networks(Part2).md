# Neural Networks (Part 2): Backpropagation Main Ideas

![alt text](image-51.png)

In statquest on **Neural Networks** part 1, Inside the **Black Box**, we started with a simple dataset that showed whether or not different drug dosages were effective against a virus. 

The low and high dosages are not effective, but the medium dosage was effective. Then we talked about how a **Neural Network** like this one fits a **green squiggle** to this dataset.

![alt text](image-52.png)

Remember, the **Neural Network** starts with identical **Activation Functions** but using different **Weights** and **Biases** on the connections, it flips and stretches the **Activation Functions** into new shapes which are then added together to get a **squiggle** that are shifted to fit the data.

![alt text](image-53.png)

However, we did not talk about how to estimate the **Weight** and **Biases**. So let's talk about how **Backpropagation** optimizes the **Weight** and **Biases** in this and other **Neural Networks**

>Note: **Back propagation** is relatively simple, but there are a ton of details. So i have split it up to bite sized pieves

## Main idea of Backpropagation

1. Using the **Chain Rule** to calculate derivatives

$$\frac{\text{d SSR}}{\text{d bias}}= \frac{\text{d SSR}}{\text{d Predicted}}$$

2. Plugging the derivatives into **Gradient Descent** to optimize parameters.

In the next part, we will talk about how the **Chain Rule** and **Gradient Descent** apply to multiple parameters simultaneously, and intoduce some fancy notation.

Then we will go completely bonkers with the chain rule and show how to opti,ize all 7 parameters simultaneously in this **Neural Network**

![alt text](image-54.png)
![alt text](image-55.png)

First, let's give each one a name so we can be celar about which specific **Weights** we are talking about and also name each **Bias**

> Note: Conceptually, Backpropagation starts with the last parameter and work its way backwords to estimate all of the other parameters.

However, we can discuss all of the **Main Ideas** behund **Backpropagation** by just estimating the last **Bias,$b_3$**

![alt text](image-56.png)

So in order to start from the back, let's assume that we already have **optimal values** for all of the parameters except for the last **Bias** term, $b_3$.

> Note: Throughout this and the next **StatQuests**, I will make parameter that have already been optimized **green** and unoptimized parameters will be **red**

![alt text](image-57.png)

> Note: To keep the math simple, let's assume **Dosages** go from 0(low) to 1(high)

## Fitting the Neural Network to the data

![alt text](image-58.png)

Now, if we run **Dosages** from 0 to 1 through the connection to the top **Node** in the **Hidden Layer** then we get x-axis coordinates for the **Activation Function** that are all inside this **red box** and when we pluf the a-axis coordinates into the **Activation Function** which, in this examaple is the **Softplus Activation Function**

$$f(x) = log(1+e^x)$$

we get the corresponding y-axis coordinates.