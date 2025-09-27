// Animation on scroll functionality
document.addEventListener('DOMContentLoaded', function() {
    // Animate skill cards on scroll
    const skillCards = document.querySelectorAll('.skill-card');
    const skillProgressBars = document.querySelectorAll('.skill-progress');
    
    const animateOnScroll = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                
                // Animate skill progress bars
                if (entry.target.querySelector('.skill-progress')) {
                    const progressBar = entry.target.querySelector('.skill-progress');
                    const width = progressBar.getAttribute('data-width');
                    setTimeout(() => {
                        progressBar.style.width = width + '%';
                    }, 300);
                }
            }
        });
    }, { threshold: 0.1 });
    
    skillCards.forEach(card => {
        animateOnScroll.observe(card);
    });
    
    // Animate footer elements on scroll
    const footerElements = document.querySelectorAll('.animate-fade-in');
    
    const footerObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, { threshold: 0.1 });
    
    footerElements.forEach(el => {
        footerObserver.observe(el);
    });
    
    // Animate general elements on scroll
    // const scrollTriggers = document.querySelectorAll('.scroll-trigger');
    
    // const scrollObserver = new IntersectionObserver((entries) => {
    //     entries.forEach(entry => {
    //         if (entry.isIntersecting) {
    //             entry.target.classList.add('visible');
    //         }
    //     });
    // }, { threshold: 0.1 });
    
    // scrollTriggers.forEach(el => {
    //     scrollObserver.observe(el);
    // });
});