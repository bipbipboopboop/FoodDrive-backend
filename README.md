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
