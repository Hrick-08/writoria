document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.testimonials-track');
    const slides = Array.from(track.children);
    const nextButton = document.querySelector('.next-arrow');
    const prevButton = document.querySelector('.prev-arrow');
    const dotsNav = document.querySelector('.slider-dots');
    
    // Create dots based on number of slides
    slides.forEach((_, index) => {
        const dot = document.createElement('span');
        dot.classList.add('dot');
        if (index === 0) dot.classList.add('active');
        dotsNav.appendChild(dot);
    });
    
    const dots = Array.from(dotsNav.children);

    // Set initial position of slides
    slides[0].classList.add('active');
    track.style.transform = 'translateX(0)';

    let currentIndex = 0;
    let isDragging = false;
    let startPos = 0;
    let currentTranslate = 0;
    let prevTranslate = 0;

    // Prevent default behavior on touch events
    track.addEventListener('touchstart', e => e.preventDefault());

    // Update slide positions
    const updateSlidePositions = () => {
        const slideWidth = slides[0].getBoundingClientRect().width;
        slides.forEach((slide, index) => {
            slide.style.left = `${slideWidth * index}px`;
        });
    };

    // Call initially and on window resize
    updateSlidePositions();
    window.addEventListener('resize', updateSlidePositions);

    const moveToSlide = (targetIndex) => {
        if (targetIndex < 0 || targetIndex >= slides.length) return;

        const targetSlide = slides[targetIndex];
        const currentSlide = slides[currentIndex];
        
        track.style.transform = `translateX(-${targetSlide.style.left})`;
        
        // Update active states
        currentSlide.classList.remove('active');
        targetSlide.classList.add('active');
        
        // Update dots
        dots[currentIndex].classList.remove('active');
        dots[targetIndex].classList.add('active');
        
        // Update arrows
        prevButton.style.opacity = targetIndex === 0 ? '0.5' : '1';
        nextButton.style.opacity = targetIndex === slides.length - 1 ? '0.5' : '1';
        
        currentIndex = targetIndex;
    };

    // Touch events for mobile swipe
    track.addEventListener('touchstart', (e) => {
        isDragging = true;
        startPos = e.touches[0].clientX;
        track.style.transition = 'none';
    });

    track.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        const currentPosition = e.touches[0].clientX;
        const diff = currentPosition - startPos;
        
        if (
            (currentIndex === 0 && diff > 0) || // Prevent dragging right on first slide
            (currentIndex === slides.length - 1 && diff < 0) // Prevent dragging left on last slide
        ) return;
        
        const slideWidth = slides[0].getBoundingClientRect().width;
        currentTranslate = prevTranslate + diff;
        track.style.transform = `translateX(${currentTranslate}px)`;
    });

    track.addEventListener('touchend', () => {
        isDragging = false;
        const slideWidth = slides[0].getBoundingClientRect().width;
        const diff = currentTranslate - prevTranslate;
        
        if (Math.abs(diff) > slideWidth * 0.3) {
            if (diff > 0 && currentIndex > 0) {
                moveToSlide(currentIndex - 1);
            } else if (diff < 0 && currentIndex < slides.length - 1) {
                moveToSlide(currentIndex + 1);
            } else {
                moveToSlide(currentIndex);
            }
        } else {
            moveToSlide(currentIndex);
        }
        
        track.style.transition = 'transform 0.5s ease';
    });

    // Button click events with debounce
    let isAnimating = false;
    
    nextButton.addEventListener('click', () => {
        if (isAnimating || currentIndex >= slides.length - 1) return;
        isAnimating = true;
        moveToSlide(currentIndex + 1);
        setTimeout(() => isAnimating = false, 500);
    });

    prevButton.addEventListener('click', () => {
        if (isAnimating || currentIndex <= 0) return;
        isAnimating = true;
        moveToSlide(currentIndex - 1);
        setTimeout(() => isAnimating = false, 500);
    });

    // Dot navigation
    dotsNav.addEventListener('click', e => {
        const targetDot = e.target.closest('.dot');
        if (!targetDot || isAnimating) return;
        
        const targetIndex = dots.findIndex(dot => dot === targetDot);
        if (targetIndex !== currentIndex) {
            isAnimating = true;
            moveToSlide(targetIndex);
            setTimeout(() => isAnimating = false, 500);
        }
    });

    // Auto advance slides every 5 seconds if not interacting
    let autoplayInterval;
    const startAutoplay = () => {
        autoplayInterval = setInterval(() => {
            if (!isDragging && !isAnimating) {
                if (currentIndex >= slides.length - 1) {
                    moveToSlide(0);
                } else {
                    moveToSlide(currentIndex + 1);
                }
            }
        }, 5000);
    };

    // Pause autoplay on user interaction
    const pauseAutoplay = () => {
        clearInterval(autoplayInterval);
    };

    // Restart autoplay after user interaction
    const restartAutoplay = () => {
        pauseAutoplay();
        startAutoplay();
    };

    track.addEventListener('touchstart', pauseAutoplay);
    track.addEventListener('touchend', restartAutoplay);
    nextButton.addEventListener('mouseenter', pauseAutoplay);
    nextButton.addEventListener('mouseleave', restartAutoplay);
    prevButton.addEventListener('mouseenter', pauseAutoplay);
    prevButton.addEventListener('mouseleave', restartAutoplay);
    dotsNav.addEventListener('mouseenter', pauseAutoplay);
    dotsNav.addEventListener('mouseleave', restartAutoplay);

    // Start autoplay initially
    startAutoplay();
});