// ============ Logo animations ============
let parentLogo = document.querySelector('.logo');
let logo = parentLogo.querySelector('img');

const strTransition = window.getComputedStyle(logo).getPropertyValue('transition');
const halfTransition = extractTransition(strTransition) * 1000 / 3;

parentLogo.addEventListener('mouseenter', () => {
    setTimeout(() => {
        logo.src = 'assets/img/icon.png';
        logo.style.opacity = '100%';
    }, halfTransition);

    logo.style.transform = 'rotateZ(360deg)';
    logo.style.opacity = '0';
});

parentLogo.addEventListener('mouseleave', () => {
    setTimeout(() => {
        logo.src = 'assets/img/logo.png';
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



// ========== Scrolling animations =========
let inverted = false;

let navbar = document.querySelector('#top-page');
let toolLinks = document.querySelectorAll('.tool-bar #tools a');
let navLinks = navbar.querySelectorAll('.account a');
let navBtns = navbar.querySelectorAll('.account .btn');
let separation = navbar.querySelector('hr');

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

    for (let btn of toolLinks) {
        btn.style.color = 'var(--dark-main)';
    }

    for (let btn of navLinks) {
        btn.style.color = 'var(--deep-main)';
    }

    for (let btn of navBtns) {
        btn.style.color = 'var(--deep-main)';
        btn.style.borderColor = 'var(--main)';
    }

    setCSSVariables({
        'pseudo-elements-color':      'var(--grey-main)',
        'link-hover-color':           'var(--dark-main)',
        'btn-hover-color':            'white',
        'btn-hover-background-color': 'var(--main)'
    });
    // setCSSVariables('var(--grey-main)', 'var(--dark-main)');
    inverted = false;
}

function invertStyle() {
    navbar.style.backgroundColor = 'var(--main)';
    separation.style.backgroundColor = 'white';

    for (let btn of toolLinks) {
        btn.style.color = 'white';
    }

    for (let btn of navLinks) {
        btn.style.color = 'white';
    }

    for (let btn of navBtns) {
        btn.style.color = 'white';
        btn.style.borderColor = 'white';
    }

    setCSSVariables({
        'pseudo-elements-color':      'white',
        'link-hover-color':           'black',
        'btn-hover-color':            'var(--deep-main)',
        'btn-hover-background-color': 'white'
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