$(document).ready(function () {
    // Function to set the theme
    function setTheme(theme) {
        const themeClassList = ['theme-light', 'theme-dark', 'theme-cool', 'theme-warm', 'theme-muted-light', 'theme-muted-dark'];
        $('body').removeClass(themeClassList.join(' ')); // Remove all theme classes
        if (theme) {
            $('body').addClass(theme); // Add selected theme class
            localStorage.setItem('theme', theme); // Save the selected theme in localStorage
        }
    }

    // Function to set the background pattern
    function setPattern(pattern) {
        const $bgDiv = $('.bg'); // Select the background div
        $bgDiv.attr('class', 'bg'); // Reset to default class
        if (pattern) {
            $bgDiv.addClass(pattern); // Add selected pattern class
            localStorage.setItem('pattern', pattern); // Save the selected pattern in localStorage
        }
    }

    // Apply saved theme on page load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme); // Apply saved theme
    } else {
        setTheme('theme-dark'); // Default to dark theme
    }

    // Apply saved pattern on page load
    const savedPattern = localStorage.getItem('pattern');
    if (savedPattern) {
        setPattern(savedPattern); // Apply saved pattern
    }

    // jQuery ready function to handle select changes
    $('#bg-select').on('change', function () {
        const selectedPattern = $(this).val();
        setPattern(selectedPattern); // Change the background pattern
    });

    $('#theme-select').on('change', function () {
        const selectedTheme = $(this).val();
        setTheme(selectedTheme); // Change the theme
        setPattern($('#bg-select').val()); // Reapply background in case the theme changes
    });

    // Set initial values for selects from localStorage or defaults
    $('#bg-select').val(savedPattern || 'default-bg'); // Default background if none saved
    $('#theme-select').val(savedTheme || 'theme-dark'); // Default theme if none saved

    // Apply the current theme and background when the page loads
    setTheme($('#theme-select').val());
    setPattern($('#bg-select').val());
});



$('.dropdown').on('click', function() {
    $('#'+ $(this).attr("id")+"-menu").toggle(600);
    $('#'+ $(this).attr("id")+"-svg").toggleClass('rotate')
});
