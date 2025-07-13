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
              btn.innerHTML = '<i class="fas fa-shopping-cart me-2"></i>Add from Cart';
              btn.classList.add("btn-outline-primary");
              btn.classList.remove("btn-primary");
              btn.onclick = () => addToCart(bookId, btn);

            }
    } else {
      // alert("Failed to remove from cart.");
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
      // alert("Failed to remove from list.");
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
    .then(response => {
        if (response.redirected) {
            // Redirect to login page
            window.location.href = response.url;
            return; // Stop further processing
        }
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
          if (document.querySelector('.cart-section')) {
            // document.getElementById("successAlert").style.display = "block";
            appendBookToCart(data.book)
          }
          if (btn != null) {
            console.log("Toggling back to Add to Cart", btn);
            btn.innerHTML = '<i class="fas fa-shopping-cart me-2"></i>Remove from Cart';
            btn.classList.add("btn-primary");
            btn.classList.remove("btn-outline-primary");
            btn.onclick = () => removeFromCart(bookId, btn);
          }
          const section = document.querySelector('.cart-section');

          if (section) {
            const spans = section.querySelectorAll('span');
            spans.forEach(span => {
              if (span.textContent.trim() === 'Empty Cart') {
                span.remove();
              }
            });
          }
         
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
    .then(response => {
        if (response.redirected) {
            // Redirect to login page
            window.location.href = response.url;
            return; // Stop further processing
        }
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            if (btn != null) {
              btn.classList.remove("btn-outline-danger");
              btn.classList.add("btn-danger");
              btn.onclick = () => removeFromWishList(bookId, btn);
            }
            if (document.querySelector('.wishlist-section')) {
              appendBookToWishList(data.book)
            }
        } else {
            // alert("Error: " + data.message);
        }
    });
}

function clearCart() {
    fetch(clearCartUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded"
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelectorAll('.cart-section .card').forEach(card => card.remove());
        } 
    });
}

function clearWishList() {
    fetch(clearWishListUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded"
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelectorAll('.wishlist-section .card').forEach(card => card.remove());

        } 
    });
}



function appendBookToWishList(book) {
  const wishlistSection = document.querySelector('.wishlist-section')
  const cardHTML = `<div class="row">
           
            
            <div class="card my-2" id="wishlist-book-${book.id}">
              <div class="row">
                <div class="col-2 d-flex justify-content-center">
                  <div class="card-body">
                    <div class="btn-group-vertical">
                      <button onclick="addToCart(${book.id})" class="btn btn-outline-primary btn-sm">
                        Add To Cart
                      </button>
                      <button class="btn btn-outline-danger btn-sm" onclick="removeFromWishList(${book.id})">
                        Remove
                      </button>  
                    </div>
                  </div>
                </div>
                <div class="col-2">
                  <div class="card-body">
                    <h3 class="card-title">$${book.cost.toFixed(2)}</h3>
                  </div>
                </div>
                <div class="col-8">
                  <div class="card-body">
                      <h5 class="card-title">
                        <a class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover" href="/books/${book.id}/">
                          ${book.title}
                        </a>
                      </h5>
                      <p class="card-text">
                      by ${book.authors.map(a => `${a.first_name} ${a.last_name}`).join(', ')}
                      </p>
                  </div>
                </div>
              </div>
            </div>`
  wishlistSection.insertAdjacentHTML('beforeend', cardHTML);
}

function appendBookToCart(book) {
  const cartSection = document.querySelector('.cart-section');

  const cardHTML = `
    <div class="card my-2" id="cart-book-${book.id}">
      <div class="row">
        <div class="col-2">
          <div class="card-body">
            <div class="btn-group-vertical">
              <button class="btn btn-outline-primary btn-sm">Purchase</button>
              <button class="btn btn-outline-warning btn-sm" onclick="addToWishList(${book.id})">
                Add to Wish List
              </button>  
              <button class="btn btn-outline-danger btn-sm" onclick="removeFromCart(${book.id})">Remove from Cart</button>
            </div>
          </div>
        </div>
        <div class="col-2">
          <div class="card-body">
            <h3 class="card-title">$${book.cost.toFixed(2)}</h3>
          </div>
        </div>
        <div class="col-8">
          <div class="card-body">
            <h5 class="card-title">
              <a class="link-dark link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover" href="/books/${book.id}/">
                ${book.title}
              </a>
            </h5>
            <p class="card-text">by ${book.authors.map(a => `${a.first_name} ${a.last_name}`).join(', ')}</p>
          </div>
        </div>
      </div>
    </div>
  `;

  cartSection.insertAdjacentHTML('beforeend', cardHTML);
}
