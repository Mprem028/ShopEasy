// static/js/cart.js
console.log("✅ cart.js loaded");

// Initialize cart
let cart = JSON.parse(localStorage.getItem("cart")) || {};
updateCartCount();

// Add product to cart
function addToCart(id, name, price) {
  const isLoggedIn = window.IS_AUTH === true;
  if (!isLoggedIn) {
    alert("Please login or register before adding items to cart.");
    window.location.href = window.LOGIN_URL || "/login/";
    return;
  }

  if (cart[id]) cart[id].qty += 1;
  else cart[id] = { name: name, price: parseFloat(price), qty: 1 };

  localStorage.setItem("cart", JSON.stringify(cart));
  updateCartCount();
  alert(`${name} added to cart ✅`);
}

// Update navbar cart count
function updateCartCount() {
  const count = Object.values(cart).reduce((sum, item) => sum + item.qty, 0);
  const el = document.getElementById("cart-count");
  if (el) el.innerText = count;
}

// Remove item from cart
function removeFromCart(id) {
  if (cart[id]) {
    delete cart[id];
    localStorage.setItem("cart", JSON.stringify(cart));
    alert("Item removed from cart 🗑️");
    location.reload();
  }
}

// Clear cart after checkout success
function clearCart() {
  localStorage.removeItem("cart");
  updateCartCount();
}
