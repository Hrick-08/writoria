document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');
    
    // Mobile menu functionality with ARIA support
    const mobileMenuBtn = document.getElementById('mobile-menu');
    const navLinks = document.getElementById('nav-links');
    const menuIcon = mobileMenuBtn.querySelector('i');
    
    function toggleMenu(show) {
        navLinks.classList.toggle('active', show);
        menuIcon.className = show ? 'fas fa-times' : 'fas fa-bars';
        mobileMenuBtn.setAttribute('aria-expanded', show);
    }
    
    mobileMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
        toggleMenu(!isExpanded);
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target) && navLinks.classList.contains('active')) {
            toggleMenu(false);
        }
    });

    // Close menu when clicking a link
    navLinks.addEventListener('click', (e) => {
        if (e.target.tagName === 'A' || e.target.closest('form')) {
            toggleMenu(false);
        }
    });

    // Check for saved theme preference or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    // Theme toggle functionality with animation
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Add rotation animation
        themeToggle.style.transform = 'rotate(360deg)';
        
        // Update theme after rotation
        setTimeout(() => {
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
            themeToggle.style.transform = 'rotate(0deg)';
        }, 200);
    });

    function updateThemeIcon(theme) {
        themeIcon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add intersection observer for smooth card animations
    const animateOnScroll = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        },
        { threshold: 0.1 }
    );

    // Animate cards, blog posts, and other elements
    const elements = document.querySelectorAll('.card, .blog-card, .auth-container, .form-container');
    elements.forEach(el => {
        el.classList.add('animate-on-scroll');
        animateOnScroll.observe(el);
    });

    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = button.getBoundingClientRect();
            
            ripple.className = 'ripple';
            ripple.style.left = `${e.clientX - rect.left}px`;
            ripple.style.top = `${e.clientY - rect.top}px`;
            
            button.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 1000);
        });
    });

    // Stagger animation for blog cards
    const animateCards = () => {
        const cards = document.querySelectorAll('.blog-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100); // Stagger each card by 100ms
        });
    };

    // Run animations on page load
    animateCards();

    // Smooth reveal for page content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.style.opacity = '0';
        mainContent.style.transform = 'translateY(20px)';
        requestAnimationFrame(() => {
            mainContent.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            mainContent.style.opacity = '1';
            mainContent.style.transform = 'translateY(0)';
        });
    }

    // Add hover effect for cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
            card.classList.add('card-hover');
        });

        card.addEventListener('mouseleave', () => {
            card.classList.remove('card-hover');
        });
    });

    // Add loading animation for images
    document.querySelectorAll('img').forEach(img => {
        img.classList.add('image-loading');
        img.onload = () => {
            img.classList.remove('image-loading');
            img.classList.add('image-loaded');
        };
    });

    // Message popup functionality
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        // Check if close button already exists
        if (!message.querySelector('.alert-close')) {
            // Add close button
            const closeBtn = document.createElement('button');
            closeBtn.innerHTML = '&times;';
            closeBtn.className = 'alert-close';
            message.appendChild(closeBtn);
        }

        // Get the close button (existing or newly created)
        const closeBtn = message.querySelector('.alert-close');

        // Add slide-in animation
        message.style.transform = 'translateX(100%)';
        setTimeout(() => {
            message.style.transform = 'translateX(0)';
        }, 100);

        // Close on button click
        closeBtn.addEventListener('click', () => {
            message.style.transform = 'translateX(100%)';
            message.style.opacity = '0';
            setTimeout(() => {
                message.parentElement.removeChild(message);
            }, 300);
        });

        // Auto-close after 5 seconds
        setTimeout(() => {
            if (message && message.parentElement) {
                message.style.transform = 'translateX(100%)';
                message.style.opacity = '0';
                setTimeout(() => {
                    if (message.parentElement) {
                        message.parentElement.removeChild(message);
                    }
                }, 300);
            }
        }, 5000);
    });

    // Voting functionality
    const voteButtons = document.querySelectorAll('.vote-btn');
    const voteCount = document.querySelector('.vote-count');

    voteButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (!this.classList.contains('vote-btn')) return;
            
            const postSlug = window.location.pathname.split('/')[2];
            const formData = new FormData();
            formData.append('vote_type', 'life');

            fetch(`/blog/${postSlug}/vote/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Update vote count
                voteCount.textContent = data.votes;

                // Update heart state
                if (data.has_life) {
                    this.classList.add('active');
                } else {
                    this.classList.remove('active');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error processing your vote. Please try again.');
            });
        });
    });

    // Enhanced Password Toggle Functionality
    const setupPasswordToggles = () => {
        const toggleBtns = document.querySelectorAll('.password-toggle');
        
        toggleBtns.forEach(btn => {
            // Remove any existing listeners first
            const newBtn = btn.cloneNode(true);
            btn.parentNode.replaceChild(newBtn, btn);
            
            newBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                const input = newBtn.closest('.input-group').querySelector('input[type="password"], input[type="text"]');
                const icon = newBtn.querySelector('i');

                if (input) {
                    if (input.type === 'password') {
                        input.type = 'text';
                        icon.classList.remove('fa-eye');
                        icon.classList.add('fa-eye-slash');
                    } else {
                        input.type = 'password';
                        icon.classList.remove('fa-eye-slash');
                        icon.classList.add('fa-eye');
                    }
                }
            });
        });
    };

    // Initialize password toggles
    setupPasswordToggles();

    // Re-initialize password toggles after any dynamic content changes
    const observer = new MutationObserver(() => {
        setupPasswordToggles();
    });

    // Observe the entire document for changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // Chat Widget Functions
    function toggleChat() {
        const chatBody = document.getElementById('chat-body');
        if (chatBody) {
            const isHidden = chatBody.style.display === 'none';
            chatBody.style.display = isHidden ? 'flex' : 'none';
            if (isHidden) {
                chatBody.querySelector('input').focus();
            }
        }
    }

    function sendMessage() {
        const input = document.getElementById('user-message');
        const message = input.value.trim();
        
        if (!message) return;
        
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML += `<div class="user-message">${message}</div>`;
        
        input.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Show loading message
        const loadingId = Date.now();
        chatMessages.innerHTML += `<div id="loading-${loadingId}" class="bot-message"><div class="typing-indicator"><span></span><span></span><span></span></div></div>`;
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Send message to server
        fetch('/chat/response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `message=${encodeURIComponent(message)}`
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            document.getElementById(`loading-${loadingId}`).remove();
            
            if (data.error) {
                chatMessages.innerHTML += `<div class="bot-message error">${data.error}</div>`;
            } else {
                chatMessages.innerHTML += `<div class="bot-message">${data.response}</div>`;
            }
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(error => {
            // Remove loading message
            document.getElementById(`loading-${loadingId}`).remove();
            
            chatMessages.innerHTML += `<div class="bot-message error">Sorry, I encountered an error. Please try again.</div>`;
            chatMessages.scrollTop = chatMessages.scrollHeight;
            console.error('Error:', error);
        });
    }

    // Add event listener for Enter key in chat input
    document.addEventListener('DOMContentLoaded', function() {
        const chatInput = document.getElementById('user-message');
        if (chatInput) {
            chatInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    sendMessage();
                }
            });
        }
    });
});