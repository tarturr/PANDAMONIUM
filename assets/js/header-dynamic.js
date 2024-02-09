// ========== Scrolling animations =========
let inverted = false;

let navbar = document.querySelector('#top-page');
let toolLinks = document.querySelectorAll('.tool-bar #tools a');
let buttonThin = navbar.querySelectorAll('.button.thin');
let buttonBold = navbar.querySelectorAll('.button.bold');
let separation = navbar.querySelector('hr');
let parentLogo = document.querySelector('.logo');
let logoText = parentLogo.querySelector('.logo-text');
let logoIcon = parentLogo.querySelector('.logo-icon');

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
    logoText.src = 'assets/img/logo-no-icon.png';
    logoIcon.src = 'assets/img/icon.png';

    for (let btn of toolLinks) {
        btn.style.color = 'var(--dark-main)';
    }

    for (let btn of buttonThin) {
        btn.style.color = 'var(--deep-main)';
    }

    for (let btn of buttonBold) {
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
    logoText.src = 'assets/img/inverted-logo-no-icon.png';
    logoIcon.src = 'assets/img/inverted-icon.png';

    for (let btn of toolLinks) {
        btn.style.color = 'white';
    }

    for (let btn of buttonThin) {
        btn.style.color = 'white';
    }

    for (let btn of buttonBold) {
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
for (let btn of buttonBold) {
    btn.addEventListener('mouseenter', () => {
        btn.style.color = inverted ? 'var(--deep-main)' : 'white';
        btn.style.backgroundColor = inverted ? 'white' : 'var(--main)';
        console.log('ENTER')
    });

    btn.addEventListener('mouseleave', () => {
        btn.style.color = inverted ? 'white' : 'var(--deep-main)';
        btn.style.backgroundColor = inverted ? 'var(--main)' : 'white';
        console.log('LEAVE')
    });
}




// ============ Logo animations ============
const strTransition = window.getComputedStyle(logoText).getPropertyValue('transition');
const transition = extractTransition(strTransition) * 1000;

const between = transition / 3.6;
const total = between + transition + 250;

const logoIconSize = window.getComputedStyle(logoIcon).width;
const newLocation = 205 / 2 - +logoIconSize.substring(0, logoIconSize.length - 2) / 2;

let isMouseOver = false;

parentLogo.addEventListener('mouseenter', () => {
    isMouseOver = true;
    logoText.style.transform = 'translateY(10px)';

    if (isMouseOver)
        setTimeout(() => {
            if (isMouseOver) logoText.style.transform = 'translateY(-25px)';
        }, between);

    if (isMouseOver)
        setTimeout(() => {
            if(isMouseOver) logoText.style.transform = 'translateY(100px)';
        }, transition);

    if (isMouseOver)
        setTimeout(() => {
            if (isMouseOver) logoIcon.style.transform = `translateX(-${newLocation}px) rotateZ(-360deg)`;
        }, total);

    if (isMouseOver)
        setTimeout(() => {
            if (isMouseOver) {
                logoText.style.display = 'none';
                parentLogo.style.justifyContent = 'right';
            }
        }, total + transition);
});

parentLogo.addEventListener('mouseleave', () => {
    isMouseOver = false;
    logoIcon.style.transform = `translateX(0px) rotateZ(-0deg)`;

    setTimeout(() => {
        logoText.style.display = 'block';
        parentLogo.style.justifyContent = 'space-between';
    }, between);

    setTimeout(() => {
        logoText.style.transform = 'translateY(-25px)';
    }, transition);

    setTimeout(() => {
        logoText.style.transform = 'translateY(10px)';
    }, total);

    setTimeout(() => {
        logoText.style.transform = 'translateY(0)';
    }, total + 250);
});

function extractTransition(strTransition) {
    const regex = /\d+(.\d+)?s/d;
    const indexes = regex.exec(strTransition).indices[0];
    return +strTransition.substring(indexes[0], indexes[1] - 1);
}