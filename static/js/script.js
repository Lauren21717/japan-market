// Wait for DOM to be fully loaded
$(document).ready(function() {
    const $searchBar = $('#searchBar');
    const $searchInput = $searchBar.find('input[type="text"]');
    const $searchTriggers = $('[onclick="toggleSearch()"]');
    
    initializeSearchBar();
    
    $searchTriggers.removeAttr('onclick').on('click', function(e) {
        e.preventDefault();
        toggleSearch();
    });
    
    $(document).on('keyup', function(e) {
        if (e.key === 'Escape' && $searchBar.is(':visible')) {
            toggleSearch();
        }
    });
    
    /**
     * Initialize search bar visibility based on current page
     */
    function initializeSearchBar() {
        const path = window.location.pathname;
        if (path.includes('collection')) {
            $searchBar.show();
        }
    }
    
    /**
     * Toggle search bar visibility and handle focus
     */
    function toggleSearch() {
        const isVisible = $searchBar.is(':visible');
        
        if (isVisible) {
            $searchBar.fadeOut(200);
            $searchInput.val('');
        } else {
            $searchBar.fadeIn(200);
            setTimeout(() => {
                $searchInput.focus();
            }, 250);
        }
    }
});
