function fetchNewJoke() {
    const jokeContainer = document.querySelector('.joke-container');
    const button = document.querySelector('.refresh-button');
    const laughSound = document.getElementById('laughSound');
    
    laughSound.volume = 0.5;
    
    jokeContainer.classList.add('loading');
    jokeContainer.classList.remove('loaded');
    button.disabled = true;

    fetch('/')
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const newDoc = parser.parseFromString(html, 'text/html');
            const newJoke = newDoc.querySelector('.joke-content');
            
            setTimeout(() => {
                document.querySelector('.joke-content').innerHTML = newJoke.innerHTML;
                jokeContainer.classList.remove('loading');
                jokeContainer.classList.add('loaded');
                button.disabled = false;

                setTimeout(() => {
                    laughSound.play().catch(e => {
                        if (e.name === 'NotAllowedError') {
                            console.log('Audio playback requires user interaction first');
                        } else {
                            console.error('Audio playback failed:', e);
                        }
                    });
                }, 2000);
            }, 1000);
        })
        .catch(error => {
            console.error('Error fetching joke:', error);
            jokeContainer.classList.remove('loading');
            jokeContainer.classList.remove('loaded');
            button.disabled = false;
        });
}

window.addEventListener('load', () => {
    const jokeContainer = document.querySelector('.joke-container');
    const laughSound = document.getElementById('laughSound');
    
    laughSound.volume = 0.5;
    
    jokeContainer.classList.add('loaded');
    
    setTimeout(() => {
        laughSound.play().catch(e => {
            if (e.name === 'NotAllowedError') {
                console.log('Audio playback requires user interaction first');
            } else {
                console.error('Audio playback failed:', e);
            }
        });
    }, 4000);
});