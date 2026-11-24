// ShopEase - Frontend JavaScript

document.addEventListener("DOMContentLoaded", () => {
    initAddToCart();
    initCartActions();
});

function initAddToCart() {
    // Home page add-to-cart buttons
    document.querySelectorAll(".add-to-cart").forEach((button) => {
        button.addEventListener("click", async (e) => {
            e.preventDefault();
            const productId = button.dataset.id;
            const form = document.getElementById("add-to-cart-form");
            let quantity = 1;
            if (form) {
                const qtyInput = form.querySelector('input[name="quantity"]');
                if (qtyInput) quantity = parseInt(qtyInput.value) || 1;
            }

            await addToCart(productId, quantity);
        });
    });

    // Product detail form
    const form = document.getElementById("add-to-cart-form");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const productId = form.dataset.id;
            const qtyInput = form.querySelector('input[name="quantity"]');
            const quantity = parseInt(qtyInput.value) || 1;
            await addToCart(productId, quantity);
        });
    }
}

async function addToCart(productId, quantity) {
    try {
        const response = await fetch("/cart/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: productId, quantity }),
        });

        const result = await response.json();
        if (result.success) {
            updateCartCount(result.cart_count);
            showToast(`${result.product} added to cart`);
        }
    } catch (error) {
        console.error("Add to cart failed:", error);
    }
}

function initCartActions() {
    // Update quantity
    document.querySelectorAll(".update-qty").forEach((button) => {
        button.addEventListener("click", async (e) => {
            e.preventDefault();
            const itemId = button.closest("form").dataset.id;
            const input = button.closest("form").querySelector('input[name="quantity"]');
            const quantity = parseInt(input.value) || 1;
            await updateCartItem(itemId, quantity);
        });
    });

    // Remove item
    document.querySelectorAll(".remove-item").forEach((button) => {
        button.addEventListener("click", async (e) => {
            e.preventDefault();
            const itemId = button.dataset.id;
            await removeCartItem(itemId);
        });
    });
}

async function updateCartItem(productId, quantity) {
    try {
        const response = await fetch("/cart/update", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: productId, quantity }),
        });

        const result = await response.json();
        if (result.success) {
            updateCartCount(result.cart_count);
            location.reload();
        }
    } catch (error) {
        console.error("Update cart failed:", error);
    }
}

async function removeCartItem(productId) {
    if (!confirm("Remove this item from cart?")) return;

    try {
        const response = await fetch("/cart/remove", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: productId }),
        });

        const result = await response.json();
        if (result.success) {
            updateCartCount(result.cart_count);
            location.reload();
        }
    } catch (error) {
        console.error("Remove from cart failed:", error);
    }
}

function updateCartCount(count) {
    const elements = document.querySelectorAll("#cart-count");
    elements.forEach((el) => {
        el.textContent = count;
    });
}

function showToast(message) {
    const toast = document.createElement("div");
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #059669;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        font-size: 0.95rem;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
