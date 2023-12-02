# CS305 Project Report
**12012427 Kerui Huang**

**12010641 Jingxuan Niu**

**12011619 Liquan Wang**



Our data collected below are all based on the follwing event:

```
0 link 200000
20 link 20000
20 link 1000
20 link 200
```

In the event file, we make the bandwidth decrease every 20s, so the network becomes more congested.



## Smoothness

|       |                           onelink                            |                           twolink                            |                          sharelink                           |
| :---: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| α=0.1 | <img src="README.pictures/image-20220531225519275.png" alt="image-20220531225519275" style="zoom:50%;" /> | <img src="README.pictures/image-20220531232042267.png" alt="image-20220531232042267" style="zoom:50%;" /> | <img src="README.pictures/image-20220531232101741.png" alt="image-20220531232101741" style="zoom:50%;" /> |
| α=0.5 | <img src="README.pictures/image-20220531232121011.png" alt="image-20220531232121011" style="zoom:50%;" /> | <img src="README.pictures/image-20220531232427787.png" alt="image-20220531232427787" style="zoom:50%;" /> | <img src="README.pictures/image-20220531232446774.png" alt="image-20220531232446774" style="zoom:50%;" /> |
| α=0.9 | <img src="README.pictures/image-20220531232504160.png" alt="image-20220531232504160" style="zoom:50%;" /> | <img src="README.pictures/image-20220601123426232.png" alt="image-20220601123426232" style="zoom:50%;" /> | <img src="README.pictures/image-20220531232550156.png" alt="image-20220531232550156" style="zoom:50%;" /> |

```python
ylabels = ['% of link utilization', 'Jain Fairness', 'Derivative of BR wrt time']
```

By checking the code in `grapher.py` we can see that **smoothness** means "Derivative of BR wrt time"

<img src="README.pictures/image-20220601172440699.png" alt="image-20220601172440699" style="zoom:80%;" />

The fifth param in proxy's log file is **BR** (bit rate), so the smoothness means **the change rate of bit rate**

We can see clearly that at the beginning the bit rate suddenly increased because we initialized the bit rate as 200 but the bandwidth is 200000

At 20000->1000, the bit rate suddenly decreased because the bandwidth becomes too narrow, and at this time the video becomes vaguer

There's no good params to improve this because the change of bandwidth defined in the event file is stable



## Fairness

|       |                           onelink                            |                           twolink                            |                          sharelink                           |
| :---: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| α=0.1 | <img src="README.pictures/image-20220531215450473.png" alt="image-20220531215450473" style="zoom:50%;" /> | <img src="README.pictures/image-20220531215806258.png" alt="image-20220531215806258" style="zoom:50%;" /> | <img src="README.pictures/image-20220531215947560.png" alt="image-20220531215947560" style="zoom:50%;" /> |
| α=0.5 | <img src="README.pictures/image-20220531215521181.png" alt="image-20220531215521181" style="zoom:50%;" /> | <img src="README.pictures/image-20220531215845553.png" alt="image-20220531215845553" style="zoom:50%;" /> | <img src="README.pictures/image-20220531220004636.png" alt="image-20220531220004636" style="zoom:50%;" /> |
| α=0.9 | <img src="README.pictures/image-20220531215719677.png" alt="image-20220531215719677" style="zoom:50%;" /> | <img src="README.pictures/image-20220601123337613.png" alt="image-20220601123337613" style="zoom:50%;" /> | <img src="README.pictures/image-20220531223638727.png" alt="image-20220531223638727" style="zoom:50%;" /> |

**Jain's Faireness** index is widely used to value the fairness of specific stream distribution system, whose formula$[1]$ is 
$$
F\left(x_{1}, \ldots x_{n}\right)=\frac{\left(\Sigma_{i=1}^{n} x_{i}\right)^{2}}{n \Sigma_{i=1}^{n} x_{i}^{2}} \in\left[\frac{1}{n}, 1\right]
$$

Here we only test two proxy, so the formula becomes

$$
F(x_1,x_2)=\frac{(x_1+x_2)^2}{2(x_1^2+y_2^2)}
$$

where $x_i$ is each stream's bandwidth, the more $F$ gets close to 1, the system is fairer to each proxy.



From the pictures, we can see that **sharelink α=0.1** performs the best

1. This may because that the **sharelink** shares the same link, so the difference is less

   <img src="README.pictures/image-20220601125511373.png" alt="image-20220601125511373" style="zoom: 80%;" />

2. And because **α=0.1**, the weight of $T_{current}$ is low, so the change rate of bit rate is low, which makes the fluctuation of network milder, the fairness will more likely to be 1



Another feature we noted is that in the **onelink** column, there are always imbalance after the `100000->10000` and `2000->200`

This feature is the same as Jain Fairness's change feature, from this, we can know that the mutation of bit rate can also cause the imbalance between two proxies

<img src="README.pictures/image-20220601130654835.png" alt="image-20220601130654835" style="zoom: 67%;" />



## Utilization

|       |                           onelink                            |                           twolink                            |                          sharelink                           |
| :---: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| α=0.1 | <img src="README.pictures/image-20220531232706372.png" alt="image-20220531232706372" style="zoom:50%;" /> | <img src="README.pictures/image-20220531232851878.png" alt="image-20220531232851878" style="zoom:50%;" /> | <img src="README.pictures/image-20220531232755024.png" alt="image-20220531232755024" style="zoom:50%;" /> |
| α=0.5 | <img src="README.pictures/image-20220531232726870.png" alt="image-20220531232726870" style="zoom:50%;" /> | <img src="README.pictures/image-20220531232905508.png" alt="image-20220531232905508" style="zoom:50%;" /> | <img src="README.pictures/image-20220531232809819.png" alt="image-20220531232809819" style="zoom:50%;" /> |
| α=0.9 | <img src="README.pictures/image-20220531232740904.png" alt="image-20220531232740904" style="zoom:50%;" /> | <img src="README.pictures/image-20220601123443954.png" alt="image-20220601123443954" style="zoom:50%;" /> | <img src="README.pictures/image-20220531232823041.png" alt="image-20220531232823041" style="zoom:50%;" /> |

- We can see clearly that at the bandwidth's sudden decrease, the utilization suddenly increase, especially in **twolink α=0.1**. This is because the network can't decrease the bit rate of segment requested in time, and α=0.1 makes the change rate more slower

   <img src="README.pictures/image-20220601133758551.png" alt="image-20220601133758551" style="zoom: 80%;" />

- Generally we can see that as bandwidth becomes narrower, the utilization becomes bigger, which is reasonable

- As for the param choice, twolink and sharelink are both good choice, but they have different advantage and disadvantage

  - **Twolink**'s advantage is its high utilization(twolink is higher than 20%, but sharelink is lower than 20%), which means in the same bandwidth, the picture quality is better.

    But the disadvantage is its fluctuation, which can be seen clearly in the picture

  - **Sharelink**'s advantage is its stability of utilization at **α=0.1**, which means the picture quality is more stable 



## Bandwidth's increase and decrease

Instead of decreasing the bandwidth, here we increase the bandwidth using the following event with **onelink α=0.5**

```
0 link_1 200
20 link_1 1000
20 link_1 20000
20 link_1 100000
```

The fairness is perfectly maintained at 1, so the increase of bandwidth doesn't affect the balance between two proxies, but the decrease does.

<img src="README.pictures/image-20220601175306742.png" alt="image-20220601175306742" style="zoom: 50%;" />



Then we test the real case, the bit rate will both increase and decrease

```
0 link_1 1000
10 link_1 500
10 link_1 2000
10 link_1 10000
10 link_1 100
10 link_1 5000
```

Below picture is the fairness change, the feature is the same as we analyze before: there is imbalance when the bit rate decreases

<img src="README.pictures/image-20220601193543645.png" alt="image-20220601193543645" style="zoom:50%;" />

Utilization change, the feature is the same as we analyze before: there is utilization increase when the bit rate decreases

<img src="README.pictures/image-20220601193721595.png" alt="image-20220601193721595" style="zoom:50%;" />



## Reference

[1] Jain's paper in 1984: https://arxiv.org/ftp/cs/papers/9809/9809099.pdf
