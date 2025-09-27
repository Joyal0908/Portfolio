// Animation on scroll functionality
document.addEventListener('DOMContentLoaded', function () {
    const skillCards = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');

                // Animate progress bars
                const progressBar = entry.target.querySelector('.skill-progress');
                if (progressBar) {
                    const width = progressBar.getAttribute('data-width');
                    setTimeout(() => {
                        progressBar.style.width = width + '%';
                    }, 300);
                }
            }
        });
    }, {
        threshold: 0.1
    });

    skillCards.forEach(card => {
        observer.observe(card);
    });
});