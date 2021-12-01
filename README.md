# Product Recommendation #

Recommendation is a very core part for retail business. For improving sales, retail business should recommend products to users in a way that help customers to get better experience. One of the way of recommendation is by calculating the co-purchase of different products.

Our main goal is to get top 5 recommended product names from a specific product id based on the co-purchase frequency. I converted this task in two separate processes:

1. Getting top recommendations

    I started from transactions.txt file, and just took the purchase items id of each transaction. Then, calculated the co-purchase frequency of requested product id with all other product ids, and only took the 5 products with highest co-occurrence frequency. By this way, we got the top 5 recommended product ids.

    However, we were interested in the product's name. So, I considered the products.txt file, and got associated product names for those recommended ids. 

2. Submitting the recommendations

    For this, I took the OpenID connection token using the service account credentials. Then, I hit the POST API, with OpenID token, to the provided endpoint after formatting the recommendation results in json format. 

## How to Run ##

If you have docker installed in the machine, then:

```
docker build -t recommendation_app .
docker run recommendation_app:latest
```