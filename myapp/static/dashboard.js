function removeFromCart(bookId) {
  fetch(`/cart/remove/${bookId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': '{{ csrf_token }}',
    },
  })
  .then(response => {
    if (response.ok) {
      document.getElementById(`book-${bookId}`).remove();
    } else {
      alert("Failed to remove.");
    }
  });
}

function removeFromWishList(bookId) {
  fetch(`/list/remove/${bookId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': '{{ csrf_token }}',
    },
  })
  .then(response => {
    if (response.ok) {
      document.getElementById(`book-${bookId}`).remove();
    } else {
      alert("Failed to remove.");
    }
  });
}

function addToCart(bookId) {
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
            alert("Added to cart!");
        } else {
            alert("Error: " + data.message);
        }
    });
}
