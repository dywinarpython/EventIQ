document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.reviews-toggle').forEach(toggle => {
        toggle.addEventListener('click', function () {
            const content = this.nextElementSibling;
            content.style.display = content.style.display === 'block' ? 'none' : 'block';
            this.textContent = content.style.display === 'block'
                ? 'Скрыть отзывы'
                : 'Отзывы (' + content.querySelectorAll('.review').length + ')';
        });
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Button hover effect
    document.querySelectorAll('.cta-button, .search-button, .details-button').forEach(button => {
        button.addEventListener('mousedown', function () {
            this.style.transform = 'translateY(0)';
        });
        button.addEventListener('mouseup', function () {
            this.style.transform = 'translateY(-2px)';
        });
        button.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });
});
// Typewriter Effect
const typedTextSpan = document.querySelector('.typed-text');
const textArray = event_extensions = [
    'без оплаты',
    'с ИИ',
    'для бизнеса',
    'с поддержкой',
    'с инновациями',
    'с уникальностью',
    'с опытом',
    'для команд',
    'по запросу',
    'по новейшим стандартам',
    'с анализом',
    'с оптимизацией',
    'по методикам',
    'для корпораций'
]
    ;
let textArrayIndex = 0;
let charIndex = 0;

function type() {
    if (charIndex < textArray[textArrayIndex].length) {
        typedTextSpan.textContent += textArray[textArrayIndex].charAt(charIndex);
        charIndex++;
        setTimeout(type, 100);
    } else {
        setTimeout(erase, 2000);
    }
}

function erase() {
    if (charIndex > 0) {
        typedTextSpan.textContent = textArray[textArrayIndex].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(erase, 50);
    } else {
        textArrayIndex++;
        if (textArrayIndex >= textArray.length) textArrayIndex = 0;
        setTimeout(type, 500);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (textArray.length) setTimeout(type, 1000);
});
















