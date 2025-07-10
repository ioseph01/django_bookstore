function removeFromCart(bookId, btn) {
  fetch(removeFromCartUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `book_id=${bookId}`
    })
  .then(response => {
    if (response.ok) {
      if (document.getElementById(`cart-book-${bookId}`) != null) {
       document.getElementById(`cart-book-${bookId}`).remove();
      }
      if (btn != null) {
              btn.classList.remove("btn-outline-primary");
              btn.classList.add("btn-primary");
              btn.onclick = () => addToCart(bookId, btn);
            }
    } else {
      alert("Failed to remove from cart.");
    }
  });
}

function removeFromWishList(bookId, btn) {
  fetch(removeFromWishListUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `book_id=${bookId}`
    })
  .then(response => {
    if (response.ok) {
      if (document.getElementById(`wishlist-book-${bookId}`) != null) {
       document.getElementById(`wishlist-book-${bookId}`).remove();
      }
      if (btn != null) {
              btn.classList.add("btn-outline-danger");
              btn.classList.remove("btn-danger");
              btn.onclick = () => addToWishList(bookId, btn);
            }
    } else {
      alert("Failed to remove from list.");
    }
  });
}

function addToCart(bookId, btn) {
    fetch(addToCartUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `book_id=${bookId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
          if (document.getElementById("successAlert") != null) {
            document.getElementById("successAlert").style.display = "block";
          }
            if (btn != null) {
              console.log("Toggling back to Add to Cart", btn);

              btn.classList.remove("btn-primary");
              btn.classList.add("btn-outline-primary");
              btn.onclick = () => removeFromCart(bookId, btn);
            }
        } else {
          
            // alert("Error: " + data.message);
        }
    });
}

function addToWishList(bookId, btn) {
    fetch(addToWishListUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `book_id=${bookId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (btn != null) {
              btn.classList.remove("btn-outline-danger");
              btn.classList.add("btn-danger");
              btn.onclick = () => removeFromWishList(bookId, btn);
            }
        } else {
            alert("Error: " + data.message);
        }
    });
}