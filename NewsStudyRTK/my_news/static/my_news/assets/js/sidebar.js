document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('#sidebar-wrapper') == null) {
        document.querySelector('.hamburger').remove()
    } else {
        const trigger = document.querySelector('.hamburger');
        const overlay = document.querySelector('.overlay');
        let isClosed = false;

        trigger.addEventListener('click', function () {
            hamburger_cross();
        });

        function hamburger_cross() {
            if (isClosed === true) {
                overlay.style.display = 'none';
                trigger.classList.remove('is-open');
                trigger.classList.add('is-closed');
                isClosed = false;
            } else {
                overlay.style.display = 'block';
                trigger.classList.remove('is-closed');
                trigger.classList.add('is-open');
                isClosed = true;
            }
        }

        const offcanvasToggle = document.querySelectorAll('[data-toggle="offcanvas"]');
        for (let i = 0; i < offcanvasToggle.length; i++) {
            offcanvasToggle[i].addEventListener('click', function () {
                const wrapper = document.getElementById('wrapper');
                wrapper.classList.toggle('toggled');
            });
        }
    }
});