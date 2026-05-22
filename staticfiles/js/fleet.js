

window.addEventListener('scroll', function() {
        const topbar = document.querySelector('.topbar');
        if (window.scrollY > 50) {
            topbar.classList.add('scrolled');
        } else {
            topbar.classList.remove('scrolled');
        }
    });
    
    

    document.addEventListener('DOMContentLoaded', function() {
        const hamburger = document.getElementById('hamburger');
        const navList = document.getElementById('nav-list');

        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('toggle');
            navList.classList.toggle('active');
        });
    });
    
    
// Toggle mobile menu
    document.getElementById('hamburger').addEventListener('click', function() {
        this.classList.toggle('toggle');
        document.getElementById('nav-list').classList.toggle('active');
    });