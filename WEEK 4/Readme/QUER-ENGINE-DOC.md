

## Product API Query Engine Documentation

### Overview

This API allows clients to query the `products` collection dynamically. It supports:

* Text search with regex (OR conditions)
* Filtering (price range, tags)
* Sorting
* Pagination
* Soft-deleted record handling
* Unified error responses

---

### Base URL

```
http://localhost:3000/products
```

---

### Query Parameters

| Parameter        | Type    | Description                                                            | Example                |
| ---------------- | ------- | ---------------------------------------------------------------------- | ---------------------- |
| `search`         | string  | Search term matched against `name` or `description` (case-insensitive) | `?search=phone`        |
| `minPrice`       | number  | Minimum price (inclusive)                                              | `?minPrice=100`        |
| `maxPrice`       | number  | Maximum price (inclusive)                                              | `?maxPrice=500`        |
| `tags`           | string  | Comma-separated list of tags (all must match)                          | `?tags=apple,samsung`  |
| `sort`           | string  | Sorting field and direction (`field:asc` or `field:desc`)              | `?sort=price:desc`     |
| `page`           | number  | Pagination page number                                                 | `?page=1`              |
| `limit`          | number  | Number of items per page                                               | `?limit=10`            |
| `includeDeleted` | boolean | Include soft-deleted products if `true`                                | `?includeDeleted=true` |

---

### Example Requests

**1. Get all products:**

```http
GET http://localhost:3000/products
```

**2. Search and filter by price:**

```http
GET http://localhost:3000/products?search=phone&minPrice=100&maxPrice=500
```

**3. Filter by tags and sort by price descending:**

```http
GET http://localhost:3000/products?tags=apple,samsung&sort=price:desc
```

**4. Pagination (page 2, 5 items per page):**

```http
GET http://localhost:3000/products?page=2&limit=5
```

**5. Include soft-deleted products:**

```http
GET http://localhost:3000/products?includeDeleted=true
```

---

### Soft Delete

**Endpoint:**

```http
DELETE /products/:id
```

* Marks a product as deleted by setting `deletedAt` timestamp.
* Does **not** remove the record from MongoDB.

**Example:**

```http
DELETE http://localhost:3000/products/6485f3e7a2b3c5f1e2d4a9b0
```

---

### Response Format

**Success:**

```json
{
  "success": true,
  "data": [
    {
      "_id": "6485f3e7a2b3c5f1e2d4a9b0",
      "name": "iPhone 14",
      "description": "Latest Apple iPhone",
      "price": 499,
      "tags": ["apple", "smartphone"],
      "deletedAt": null,
      "createdAt": "2025-12-31T11:00:00.000Z"
    }
  ],
  "page": 1,
  "limit": 10,
  "total": 15
}
```

**Error (Unified Error Contract):**

```json
{
  "success": false,
  "message": "Product not found",
  "code": "PRODUCT_NOT_FOUND",
  "timestamp": "2025-12-31T12:00:00.000Z",
  "path": "/products/6485f3e7a2b3c5f1e2d4a9b0"
}
```

---

### Internal Query Engine Behavior

1. **Dynamic filters:**

   * Builds a MongoDB query object based on request parameters.
   * Example:

```js
filters.$or = [
  { name: { $regex: search, $options: "i" } },
  { description: { $regex: search, $options: "i" } }
];

filters.price = { $gte: minPrice, $lte: maxPrice };
filters.tags = { $all: tags.split(",") };
```

2. **Sorting:**

```js
const [field, order] = sort.split(":");
const sortObj = { [field]: order === "desc" ? -1 : 1 };
```

3. **Pagination:**

```js
const skip = (page - 1) * limit;
Product.find(filters).sort(sortObj).skip(skip).limit(limit);
```

4. **Soft delete:**

   * Only include products where `deletedAt` is `null` by default.
   * Include deleted products if `includeDeleted=true`.

---

### Notes / Best Practices

* Use **Postman or curl** to test complex queries.
* All search operations are **case-insensitive**.
* Always check the **response format** for success and errors.
* Avoid sending both `minPrice` and `maxPrice` as empty strings; they should be numbers.
* Use `tags` as comma-separated values; order doesn’t matter.

