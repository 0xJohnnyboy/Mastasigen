const spoilers = Array.from(document.querySelectorAll('blockquote.spoiler'));
const html = document.querySelector('html');
const themeToggleBtn = document.querySelector('li#theme-toggle>a>button');
const themeToggleIcon = themeToggleBtn.querySelector('i');

spoilers.forEach(item => {
    item.addEventListener('click', (e) => {
        if (e.target.tagName === 'BLOCKQUOTE') {
            const spoiler = e.target;
            spoiler.classList.toggle('spoiler');
        }
    });
});

const theme = html.getAttribute('theme');
const sessionPreference = sessionStorage.getItem('theme');

const userPrefers = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

sessionPreference && html.setAttribute('theme', sessionPreference);
theme === 'system' && userPrefers && !sessionPreference && html.setAttribute('theme', userPrefers);

const themeFAIcons = {
    light: 'fa-moon',
    dark: 'fa-sun'
}

themeToggleIcon.classList.add(themeFAIcons[ sessionPreference ? sessionPreference : userPrefers]);

themeToggleBtn.addEventListener('click', (e) => {
    let themeToSet = '';
    if (themeToggleIcon.classList.contains(themeFAIcons['dark'])) {
        themeToggleIcon.classList.replace(themeFAIcons['dark'], themeFAIcons['light']);
        themeToSet = 'light';
    } else if (themeToggleIcon.classList.contains(themeFAIcons['light'])) {
        themeToggleIcon.classList.replace(themeFAIcons['light'], themeFAIcons['dark']);
        themeToSet = 'dark';
    }
    sessionStorage.setItem('theme', themeToSet);
    html.setAttribute('theme', themeToSet);
})

