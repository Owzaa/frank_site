// Enhanced AJAX Loading
function loadProjects(url) {
    const projectList = document.getElementById('project-list');
    projectList.style.minHeight = '400px';
    projectList.innerHTML = `
        <div class="loading-overlay">
            <div class="text-center">
                <div class="spinner-border" style="width: 3rem; height: 3rem; color: var(--primary);" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3" style="color: var(--primary);">Curating Projects...</p>
            </div>
        </div>
    `;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            projectList.innerHTML = data.html;
            history.replaceState(null, '', url);
            // Re-initialize any interactive elements
            initHoverEffects();
        })
        .catch(error => {
            projectList.innerHTML = `
                <div class="alert alert-danger" role="alert" style="color: var(--primary);">
                    Error loading projects. Please refresh the page.
                </div>
            `;
        });
}

// Hover effect initialization
function initHoverEffects() {
    document.querySelectorAll('.project-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.transform = `
                translateY(-5px)
                rotateX(${(y - rect.height/2)/15}deg)
                rotateY(${-(x - rect.width/2)/15}deg)
            `;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initHoverEffects();

    // Initialize all category swipers
    document.querySelectorAll('.categorySwiper').forEach((swiperEl, index) => {
      new Swiper(swiperEl, {
        slidesPerView: "auto",
        spaceBetween: 20,
        loop: true,
        autoplay: {
          delay: 3000,
          disableOnInteraction: false,
          pauseOnMouseEnter: true
        },
        navigation: {
          nextEl: swiperEl.querySelector('.swiper-button-next'),
          prevEl: swiperEl.querySelector('.swiper-button-prev'),
        },
        pagination: {
          el: swiperEl.querySelector('.swiper-pagination'),
          clickable: true,
          dynamicBullets: true
        },
        breakpoints: {
          640: { slidesPerView: 2 },
          768: { slidesPerView: 3 },
          1024: { slidesPerView: 4 }
        },
        on: {
          init: function() {
            // Add animation delay to slides
            this.slides.forEach((slide, slideIndex) => {
              slide.style.transitionDelay = `${slideIndex * 0.1}s`;
            });
          }
        }
      });
    });
    
    // Grid/List view toggle functionality
    const gridViewBtn = document.getElementById('grid-view-btn');
    const listViewBtn = document.getElementById('list-view-btn');
    const productsContainer = document.getElementById('products-container');
    const productItems = document.querySelectorAll('.product-item');
    
    // Set default active state
    if (gridViewBtn) {
        gridViewBtn.classList.add('active');
    }
    
    // Grid view (default)
    if (gridViewBtn) {
        gridViewBtn.addEventListener('click', () => {
            gridViewBtn.classList.add('active');
            listViewBtn.classList.remove('active');
            
            productItems.forEach(item => {
                item.classList.remove('col-12');
                item.classList.add('col-md-4');
                
                // Reset card layout
                const card = item.querySelector('.card');
                card.classList.remove('flex-row');
                
                // Reset image container
                const imgContainer = item.querySelector('.position-relative');
                if (imgContainer) {
                    imgContainer.style.width = '100%';
                }
                
                // Reset image size
                const img = item.querySelector('.card-img-top, .bg-light');
                if (img) {
                    img.style.height = '250px';
                    img.style.width = '100%';
                }
                
                // Adjust card body
                const cardBody = item.querySelector('.card-body');
                if (cardBody) {
                    cardBody.style.width = '100%';
                }
            });
        });
    }
    
    // List view
    if (listViewBtn) {
        listViewBtn.addEventListener('click', () => {
            listViewBtn.classList.add('active');
            gridViewBtn.classList.remove('active');
            
            productItems.forEach(item => {
                item.classList.remove('col-md-4');
                item.classList.add('col-12');
                
                // Change card layout to horizontal
                const card = item.querySelector('.card');
                card.classList.add('flex-row');
                
                // Adjust image container
                const imgContainer = item.querySelector('.position-relative');
                if (imgContainer) {
                    imgContainer.style.width = '200px';
                }
                
                // Adjust image size for list view
                const img = item.querySelector('.card-img-top, .bg-light');
                if (img) {
                    img.style.height = '200px';
                    img.style.width = '200px';
                }
                
                // Adjust card body
                const cardBody = item.querySelector('.card-body');
                if (cardBody) {
                    cardBody.style.width = 'calc(100% - 200px)';
                }
            });
        });
    }
    
    // Initialize any GLightbox instances for product images
    if (typeof GLightbox !== 'undefined') {
      const lightbox = GLightbox({
        selector: '.product-image-lightbox',
        touchNavigation: true,
        loop: true
      });
    }

    // Show loading splash when any link is clicked
    const splash = document.getElementById("loading-splash");
    document.querySelectorAll("a").forEach(link => {
      // Exclude anchor links and JavaScript voids
      if (link.getAttribute("href") && !link.getAttribute("href").startsWith("#") && !link.getAttribute("href").startsWith("javascript")) {
        link.addEventListener("click", function () {
          splash.style.display = "flex";
        });
      }
    });

    // Also trigger splash for form submissions
    document.querySelectorAll("form").forEach(form => {
      form.addEventListener("submit", function () {
        splash.style.display = "flex";
      });
    });

    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    }

    // Load theme on page load
    (function () {
        const theme = localStorage.getItem('theme');
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
        }
    })();

    // Initialize GLightbox
    const lightbox = GLightbox({
      selector: '.product-image-lightbox',
      touchNavigation: true,
      loop: true,
      autoplayVideos: true
    });
    
    // Make thumbnail items clickable
    document.querySelectorAll('.thumbnail-item').forEach(item => {
      item.addEventListener('click', function() {
        const slideIndex = this.getAttribute('data-bs-slide-to');
        const carousel = bootstrap.Carousel.getInstance(document.querySelector('#productCarousel'));
        if (carousel) {
          carousel.to(parseInt(slideIndex));
        }
      });
    });
    
    // Quantity selector functionality
    const quantityInput = document.getElementById('quantity');
    const quantityHiddenInput = document.getElementById('quantity-input');
    const decreaseBtn = document.getElementById('decrease-qty');
    const increaseBtn = document.getElementById('increase-qty');
    
    // Get max stock from product
    const maxStock = Number('{% if product.stock %}{{ product.stock }}{% else %}10{% endif %}');
    
    if (quantityInput && quantityHiddenInput && decreaseBtn && increaseBtn) {
      // Sync the visible input with the hidden input used in the form
      const syncInputs = () => {
        quantityHiddenInput.value = quantityInput.value;
      };
      
      decreaseBtn.addEventListener('click', () => {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
          quantityInput.value = currentValue - 1;
          syncInputs();
        }
      });
      
      increaseBtn.addEventListener('click', () => {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue < maxStock) {
          quantityInput.value = currentValue + 1;
          syncInputs();
        }
      });
      
      // Prevent manual entry of invalid values
      quantityInput.addEventListener('change', () => {
        let value = parseInt(quantityInput.value);
        if (isNaN(value) || value < 1) {
          quantityInput.value = 1;
        } else if (value > maxStock) {
          quantityInput.value = maxStock;
        }
        syncInputs();
      });
      
      // Initialize sync
      syncInputs();
    }
    
    // Add hover effect to product images
    const productImages = document.querySelectorAll('.product-image');
    productImages.forEach(img => {
      img.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.05)';
        this.style.transition = 'transform 0.3s ease';
      });
      
      img.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
      });
    });

    function incrementQuantity(button) {
        const input = button.parentNode.querySelector('input');
        input.value = parseInt(input.value) + 1;
    }
    
    function decrementQuantity(button) {
        const input = button.parentNode.querySelector('input');
        if (parseInt(input.value) > 1) {
            input.value = parseInt(input.value) - 1;
        }
    }

    // Toggle payment method details
    const paymentOptions = document.querySelectorAll('input[name="payment_option"]');
    const creditCardDetails = document.getElementById('credit_card_details');
    const paypalDetails = document.getElementById('paypal_details');
    const paymentMethodInput = document.getElementById('payment_method');
    
    paymentOptions.forEach(option => {
      option.addEventListener('change', function() {
        if (this.value === 'credit_card') {
          creditCardDetails.classList.remove('d-none');
          paypalDetails.classList.add('d-none');
          paymentMethodInput.value = 'credit_card';
        } else if (this.value === 'paypal') {
          creditCardDetails.classList.add('d-none');
          paypalDetails.classList.remove('d-none');
          paymentMethodInput.value = 'paypal';
        }
      });
    });
    
    // Set initial payment method
    paymentMethodInput.value = 'credit_card';
    
    // Handle place order button
    const placeOrderBtn = document.getElementById('place-order-btn');
    const checkoutForm = document.getElementById('checkout-form');
    
    placeOrderBtn.addEventListener('click', function() {
      if (checkoutForm.checkValidity()) {
        checkoutForm.submit();
      } else {
        checkoutForm.reportValidity();
      }
    });

    // Simulate payment processing and redirect
    {% if payment.status == 'pending' %}
    setTimeout(function() {
        window.location.href = "{% url 'payment_confirmation' payment.id %}?status=completed";
    }, 5000);
    {% endif %}
});
