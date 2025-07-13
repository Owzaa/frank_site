document.addEventListener("DOMContentLoaded", function() {
  const slider = document.querySelector(".logo-slider");
  let isDown = false;
  let startX;
  let scrollLeft;

  slider.addEventListener("mousedown", e => {
    isDown = true;
    slider.classList.add("active");
    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
  });

  slider.addEventListener("mouseleave", () => {
    isDown = false;
    slider.classList.remove("active");
  });

  slider.addEventListener("mouseup", () => {
    isDown = false;
    slider.classList.remove("active");
  });

  slider.addEventListener("mousemove", e => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - slider.offsetLeft;
    const walk = (x - startX) * 3; //scroll-fast
    slider.scrollLeft = scrollLeft - walk;
  });
});


function createBubbles() {
    const bubbleLayer = document.querySelector('.bubble-layer');
    const bubbleCount = 12; // Number of bubbles
    
    for(let i = 0; i < bubbleCount; i++) {
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        
        // Random size between 50px and 300px
        const size = Math.random() * 250 + 50;
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        
        // Random position
        bubble.style.left = `${Math.random() * 100}%`;
        
        // Random animation delay and duration
        bubble.style.animationDelay = `${Math.random() * 15}s`;
        bubble.style.animationDuration = `${Math.random() * 10 + 15}s`;
        
        // Random opacity
        bubble.style.background = `rgba(170, 77, 42, ${Math.random() * 0.15 + 0.05})`;
        
        bubbleLayer.appendChild(bubble);
    }
}

// Call on load and resize
window.addEventListener('load', createBubbles);
window.addEventListener('resize', createBubbles);