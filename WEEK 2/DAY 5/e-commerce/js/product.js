document.addEventListener("DOMContentLoaded", ()=> {
  const params = new URLSearchParams(location.search);
  const id = params.get("id");
  const container = document.getElementById("productDetail");

  if(!id){ container.innerHTML = "<p>Missing product id.</p>"; return; }

  async function load(){
    try{
      container.innerHTML = "<p class='loading'>Loading product…</p>";
      const res = await fetch(`https://dummyjson.com/products/${id}`);
      if(!res.ok) throw new Error("Product not found");
      const p = await res.json();

      container.innerHTML = `
        <div class="product-page">
          <div class="product-detail-left">
            <img src="${p.thumbnail}" alt="${escapeHtml(p.title)}" />
          </div>
          <div class="product-detail-right">
            <h1>${escapeHtml(p.title)}</h1>
            <div class="card-rating">Rating: ${p.rating?.toFixed(1) || "0.0"}</div>
            <h2 style="color:var(--accent); margin:8px 0">₹ ${p.price}</h2>
            <p style="color:var(--muted)">${escapeHtml(p.description)}</p>
            <p><strong>Brand:</strong> ${escapeHtml(p.brand)}</p>
            <p><strong>Category:</strong> ${escapeHtml(p.category)}</p>
            <p><strong>Stock:</strong> ${p.stock}</p>
            <p><strong>Warranty:</strong> ${p.warrantyInformation || "N/A"}</p>
            <p><strong>Shipping:</strong> ${p.shippingInformation || "N/A"}</p>
            <p><strong>Dimensions:</strong> ${p.dimensions?.width || 0} × ${p.dimensions?.height || 0} × ${p.dimensions?.depth || 0} mm</p>
            <p><strong>Tags:</strong> ${(p.tags||[]).join(", ")}</p>
            <div style="margin-top:14px">
              <button class="btn-primary" onclick="location.href='products.html'">Back to products</button>
            </div>
            <hr />
            <h3>Reviews</h3>
            <div id="reviewsList"></div>
          </div>
        </div>
      `;

      const reviewsList = document.getElementById("reviewsList");
      (p.reviews||[]).forEach(r=>{
        const d = document.createElement("div");
        d.className = "review-item";
        d.innerHTML = `<strong>${escapeHtml(r.reviewerName || "User")}</strong> — ⭐ ${r.rating}<p>${escapeHtml(r.comment || "")}</p><small>${new Date(r.date).toLocaleString()}</small>`;
        reviewsList.appendChild(d);
      });

    }catch(err){
      container.innerHTML = `<p>Unable to load product. ${err.message}</p>`;
    }
  }

  function escapeHtml(s){ if(!s) return ""; return String(s).replace(/[&<>"]/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' }[c])); }

  load();
});
