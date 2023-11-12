// ========== Scrolling animations =========
let inverted = false;

let navbar = document.querySelector('#top-page');
let toolLinks = document.querySelectorAll('.tool-bar #tools a');
let navLinks = navbar.querySelectorAll('.account a');
let navBtns = navbar.querySelectorAll('.account .btn');
let separation = navbar.querySelector('hr');
let parentLogo = document.querySelector('.logo');
let logo = parentLogo.querySelector('img');

document.addEventListener('scroll', () => {
    let coord = window.scrollY;

    if (coord === 0) {
        if (inverted) {
            setDefaultStyle();
        }
    } else {
        if (!inverted) {
            invertStyle();
        }
    }
});

function setDefaultStyle() {
    navbar.style.backgroundColor = 'white';
    separation.style.backgroundColor = 'var(--dark-main)';
    logo.src = 'assets/img/logo.png';

    for (let btn of toolLinks) {
        btn.style.color = 'var(--dark-main)';
    }

    for (let btn of navLinks) {
        btn.style.color = 'var(--deep-main)';
    }

    for (let btn of navBtns) {
        btn.style.color = 'var(--deep-main)';
        btn.style.borderColor = 'var(--main)';
        btn.style.backgroundColor = 'white';
    }

    setCSSVariables({
        'pseudo-elements-color': 'var(--grey-main)'
    });
    // setCSSVariables('var(--grey-main)', 'var(--dark-main)');
    inverted = false;
}

function invertStyle() {
    navbar.style.backgroundColor = 'var(--main)';
    separation.style.backgroundColor = 'white';
    logo.src = 'assets/img/inverted-logo.png';

    for (let btn of toolLinks) {
        btn.style.color = 'white';
    }

    for (let btn of navLinks) {
        btn.style.color = 'white';
    }

    for (let btn of navBtns) {
        btn.style.color = 'white';
        btn.style.borderColor = 'white';
        btn.style.backgroundColor = 'var(--main)';
    }

    setCSSVariables({
        'pseudo-elements-color': 'white'
    })
    // setCSSVariables('white', 'black');
    inverted = true;
}

function setCSSVariables(values) {
    let cssVariables = document.querySelector(':root');

    for (let key in values) {
        cssVariables.style.setProperty('--' + key, values[key]);
    }
}




// ============= Hover effects =============
for (let btn of navLinks) {
    btn.addEventListener('mouseenter', () => {
        btn.style.color = inverted ? '#d7d7d7' : 'var(--dark-main)';
    });

    btn.addEventListener('mouseleave', () => {
        btn.style.color = inverted ? 'white' : 'var(--deep-main)';
    });
}

for (let btn of navBtns) {
    btn.addEventListener('mouseenter', () => {
        btn.style.color = inverted ? 'var(--deep-main)' : 'white';
        btn.style.backgroundColor = inverted ? 'white' : 'var(--main)';
    });

    btn.addEventListener('mouseleave', () => {
        btn.style.color = inverted ? 'white' : 'var(--deep-main)';
        btn.style.backgroundColor = inverted ? 'var(--main)' : 'white';
    });
}




// ============ Logo animations ============
const strTransition = window.getComputedStyle(logo).getPropertyValue('transition');
const halfTransition = extractTransition(strTransition) * 1000 / 3;

parentLogo.addEventListener('mouseenter', () => {
    setTimeout(() => {
        logo.src = 'assets/img/' + (inverted ? 'inverted-' : '') + 'icon.png';
        logo.style.opacity = '100%';
    }, halfTransition);

    logo.style.transform = 'rotateZ(360deg)';
    logo.style.opacity = '0';
});

parentLogo.addEventListener('mouseleave', () => {
    setTimeout(() => {
        logo.src = 'assets/img/' + (inverted ? 'inverted-' : '') + 'logo.png';
        logo.style.opacity = '100%';
    }, halfTransition);

    logo.style.transform = 'rotateZ(0)';
    logo.style.opacity = '0';
});

function extractTransition(strTransition) {
    const regex = /\d+(.\d+)?s/d;
    const indexes = regex.exec(strTransition).indices[0];
    return +strTransition.substring(indexes[0], indexes[1] - 1);
}