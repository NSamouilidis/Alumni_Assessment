/**
 * Main JavaScript file for Mediterranean College Alumni Portal
 */

document.addEventListener('DOMContentLoaded', () => {
    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(tooltipTriggerEl => {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add active class to navbar links based on current page
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.startsWith(href) && href !== '/') {
            link.classList.add('active');
        } else if (href === '/' && currentPath === '/') {
            link.classList.add('active');
        }
    });

    // Initialize any date pickers
    const datePickers = document.querySelectorAll('input[type="date"]');
    
    datePickers.forEach(picker => {
        // If the date is empty, set it to empty (remove default value)
        if (!picker.value) {
            picker.value = '';
        }
    });

    // Mobile menu toggle effect
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', () => {
            navbarToggler.classList.toggle('active');
        });
    }

    // Scroll to top button
    window.addEventListener('scroll', () => {
        const scrollTopBtn = document.getElementById('scrollTopBtn');
        if (scrollTopBtn) {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                scrollTopBtn.style.display = 'block';
            } else {
                scrollTopBtn.style.display = 'none';
            }
        }
    });

    // Function to scroll to top
    window.scrollToTop = function() {
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    };
});