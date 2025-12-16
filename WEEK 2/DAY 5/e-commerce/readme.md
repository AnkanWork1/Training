📦 E-Commerce Product Listing — Mini Project

A fully responsive Flipkart-style product listing UI built using HTML, CSS, and JavaScript with live product data from:

🔗 https://dummyjson.com/products

This project demonstrates:

DOM manipulation

Fetch API

Search + Dynamic filtering

Sorting

Category filtering

Responsive layout

Code modularity

🚀 Features
✅ 1. Product Fetching (Using Fetch API)

Products are loaded from DummyJSON:

const res = await fetch("https://dummyjson.com/products");
const data = await res.json();

![alt text](<output/Screenshot from 2025-12-12 13-54-46.png>)

✅ 2. Product Cards (Title, Image, Price)

Each item is rendered dynamically with:

Thumbnail

Title

Price

Rating

![alt text](<output/Screenshot from 2025-12-12 13-57-36.png>)

✅ 3. Search Bar (Live Filtering)

Typing in the search bar instantly filters visible products.
![alt text](<output/Screenshot from 2025-12-12 13-55-14.png>)

✅ 4. Category Filtering (Flipkart Style)

Top categories displayed as rounded buttons.
![alt text](<output/Screenshot from 2025-12-12 13-54-58.png>)

✅ 5. Price Sorting

High → Low

Low → High
![alt text](<output/Screenshot from 2025-12-12 14-00-44.png>)
✅ 6. Mobile Responsive


![alt text](<output/Screenshot from 2025-12-12 13-54-46.png>)
Fully responsive layout using CSS Grid + Flexbox.



📄 How It Works
🔹 1. init() — Loads products
async function init() {
  const res = await fetch(API);
  const data = await res.json();
  allProducts = data.products;
  visibleProducts = [...allProducts];

  renderCategories(allProducts);
  renderProducts(visibleProducts);
}

🔹 2. Search
function handleSearch(value) {
  visibleProducts = allProducts.filter(p =>
    p.title.toLowerCase().includes(value.toLowerCase())
  );
  renderProducts(visibleProducts);
}

🔹 3. Categories
const cats = Array.from(new Set(list.map(p => p.category))).slice(0,12);


✔ Extract unique categories
✔ Limit to 12 for clean UI

🔹 4. Sorting
visibleProducts.sort((a, b) => b.price - a.price);

📱 Responsive Layout

Grid layout changes from:

4 columns → Desktop

2 columns → Tablet

1 column → Mobile

🧪 What I Learned

✔ DOM manipulation best practices
✔ How Fetch API returns promises
✔ Async–await execution flow
✔ Event delegation
✔ How filtering & sorting work efficiently
✔ Rendering dynamic UI from JS
✔ Making UI fully responsive with Flexbox + Grid

📸 Screenshots

(Add your screenshots here)

🧭 Future Improvements

Pagination

Add to cart

Wishlist

Product review system

📜 License

This project is for learning purposes.

If you want, I can also generate:

✅ A more advanced README
✅ GIF previews
✅ Proper folder structure with comments
✅ Deployment guide (Netlify / GitHub Pages)

Just tell me!