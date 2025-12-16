/* products.js
   Fetch products, render cards, search, sort, categories, click -> product.html?id=...
*/
document.addEventListener("DOMContentLoaded", () => {
  const API = "https://dummyjson.com/products?limit=100";
  const grid = document.getElementById("productsGrid");
  const searchInput = document.getElementById("searchInput");
  const sortSelect = document.getElementById("sortSelect");
  const loading = document.getElementById("loading");
  const empty = document.getElementById("empty");
  const categoryRow = document.getElementById("categoryRow");

  let allProducts = [];
  let visible = [];

  // Utility: format money
  const money = v => (typeof v === "number" ? v.toFixed(2) : v);

  // Fetch & init
  async function init() {
    try {
      const res = await fetch(API);
      const data = await res.json();
      allProducts = data.products || [];
      visible = [...allProducts];

      renderCategories(allProducts);
      renderProducts(visible);
    } catch (err) {
      console.error("Failed to load products", err);
      loading.textContent = "Failed to load products.";
    }
  }

  // categories (unique from products)
  function renderCategories(list) {
    const cats = Array.from(new Set(list.map(p => p.category))).slice(0,12);
    categoryRow.innerHTML = "";
    const allBtn = document.createElement("button");
    allBtn.className = "category-btn active";
    allBtn.textContent = "All";
    allBtn.addEventListener("click", () => { document.querySelectorAll(".category-btn").forEach(b=>b.classList.remove("active")); allBtn.classList.add("active"); filterByCategory(null); });
    categoryRow.appendChild(allBtn);

    cats.forEach(c=>{
      const btn = document.createElement("button");
      btn.className = "category-btn";
      btn.textContent = c.charAt(0).toUpperCase() + c.slice(1);
      btn.addEventListener("click", () => {
        document.querySelectorAll(".category-btn").forEach(b=>b.classList.remove("active"));
        btn.classList.add("active");
        filterByCategory(c);
      });
      categoryRow.appendChild(btn);
    });
  }

  function filterByCategory(category){
    if(!category){ visible = [...allProducts]; }
    else{ visible = allProducts.filter(p=>p.category === category); }
    searchInput.value = "";
    sortSelect.value = "";
    renderProducts(visible);
  }

  // render list
  function renderProducts(list){
    loading.hidden = true;
    grid.innerHTML = "";
    if(!list || list.length===0){
      empty.hidden = false;
      return;
    } else empty.hidden = true;

    list.forEach(p => {
      const card = document.createElement("article");
      card.className = "card";
      // badges
      let badgeHTML = "";
      if(p.stock === 0){ badgeHTML = `<div class="badge out">OUT OF STOCK</div>`; }
      else if((p.discountPercentage || 0) > 0){ badgeHTML = `<div class="badge">SALE</div>`; }
      else if(Array.isArray(p.tags) && p.tags.map(t=>t.toLowerCase()).includes("new")){ badgeHTML = `<div class="badge new">NEW</div>`; }

      // rating stars (round to 1 place)
      const stars = Math.round((p.rating||0))*1; // integer stars for display
      const starHTML = `<div class="card-rating">${"★".repeat(Math.min(5, Math.round(p.rating))) } <span style="color:var(--muted);font-weight:600">${p.rating?.toFixed(1)||"0.0"}</span></div>`;

      card.innerHTML = `
        ${badgeHTML}
        <div class="img-wrap"><img loading="lazy" src="${p.thumbnail}" alt="${escapeHtml(p.title)}"></div>
        <div class="overlay" aria-hidden="true">
          <button class="icon-btn" title="Quick view" data-quick="${p.id}">🔍</button>
          <button class="icon-btn" title="Wishlist" data-wish="${p.id}">♡</button>
          <button class="icon-btn" title="Add to cart" data-cart="${p.id}">🛒</button>
        </div>
        <div class="card-body">
          <div class="card-title">${escapeHtml(p.title)}</div>
          ${starHTML}
          <div class="card-sub">${escapeHtml(p.brand)}</div>
          <div class="card-price">₹ ${money(p.price)}</div>
        </div>
      `;

      // click to open product detail
      card.addEventListener("click", (e) => {
        // if user clicked a small icon (overlay button), handle separately
        const btn = e.target.closest(".icon-btn");
        if(btn){
          e.stopPropagation();
          handleIconClick(btn);
          return;
        }
        window.location.href = `product.html?id=${p.id}`;
      });

      grid.appendChild(card);
    });
  }

  // escape simple html to avoid injection
  function escapeHtml(s){ if(!s) return ""; return String(s).replace(/[&<>"]/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' }[c])); }

  function handleIconClick(btn){
    if(btn.dataset.quick){
      // quick view - open detail in new tab
      window.open(`product.html?id=${btn.dataset.quick}`, "_blank");
    } else if(btn.dataset.wish){
      alert("Added to wishlist (demo)");
    } else if(btn.dataset.cart){
      alert("Added to cart (demo)");
    }
  }

  // search
  searchInput.addEventListener("input", ()=> {
    const q = searchInput.value.trim().toLowerCase();
    if(!q){ renderProducts(visible); return; }
    const filtered = visible.filter(p => p.title.toLowerCase().includes(q) || p.brand?.toLowerCase().includes(q) || (p.tags||[]).some(t=>t.toLowerCase().includes(q)));
    renderProducts(filtered);
  });

  // sort
  sortSelect.addEventListener("change", ()=>{
    const val = sortSelect.value;
    let list = [...visible];
    if(val === "low") list.sort((a,b)=>a.price - b.price);
    else if(val === "high") list.sort((a,b)=>b.price - a.price);
    renderProducts(list);
  });

  // init fetch
  init();
});
