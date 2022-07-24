Cart API

```
Operation
Create a cart
Add items to a cart
Update the quantity of items
Remove items from a cart
Get cart with its items
```

| Method | URL                         | REQUEST | RESPONSE |
| ------ | --------------------------- | ------- | -------- |
| POST   | shops/carts                 | user_id |          |
| POST   | shops/carts/<cart_id>/items | {items} |          |
| PUT    | shops/carts/<cart_id>/items | {items} |          |
| DELETE | shops/carts/<cart_id>       |         |          |
| GET    | shops/carts/<cart_id>/items |         | {items}  |

```
Cart
1) Creates a cart for the Customer everytime they sign up for an account.
2) Get the cart of a Customer by doing queryset.last()
3) Add new item to cart by : ...
4) Once user hits submit Order, hit the orders/ endpoint
    Create a new Cart for the user
```
