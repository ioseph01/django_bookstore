document.addEventListener('DOMContentLoaded', function() {
        const placeholders = document.querySelectorAll('.book-placeholder');
        
        placeholders.forEach(function(placeholder) {
            const bookId = parseInt(placeholder.getAttribute('data-book-id'));
            
            // Method 1: Simple hash-based color generation
            const color = generateColorFromBookId(bookId);
            placeholder.style.backgroundColor = color;
            
            // Ensure text is readable
            const brightness = getBrightness(color);
            placeholder.style.color = brightness > 128 ? '#000' : '#fff';
        });
    });

// document.addEventListener('DOMContentLoaded', function() {
//     const bookcovers = document.querySelectorAll('.image-col img');

//     bookcovers.forEach((el) => {
//         const bookId = el.getAttribute('data-book-id');
//         const color = generateColorFromBookId(bookId);
//         el.style.border = `4px solid ${color}`;
//     });
// });

    // Generate consistent color from book ID
    function generateColorFromBookId(bookId) {
        // Method 1: Using golden ratio for good color distribution
        const golden_ratio = 0.618033988749895;
        const hue = (bookId * golden_ratio) % 1;
        const saturation = 0.7; // 70% saturation
        const lightness = 0.5;  // 50% lightness
        
        return hslToHex(hue * 360, saturation * 100, lightness * 100);
    }
    
    // Alternative method using direct hash
    function generateColorFromBookIdHash(bookId) {
        // Create a simple hash from book ID
        let hash = bookId;
        hash = ((hash << 5) - hash) + bookId;
        hash = hash & hash; // Convert to 32-bit integer
        
        // Extract RGB values
        const r = (hash & 0xFF0000) >> 16;
        const g = (hash & 0x00FF00) >> 8;
        const b = hash & 0x0000FF;
        
        // Ensure minimum brightness
        const minBrightness = 100;
        const adjustedR = Math.max(r, minBrightness);
        const adjustedG = Math.max(g, minBrightness);
        const adjustedB = Math.max(b, minBrightness);
        
        return `rgb(${adjustedR}, ${adjustedG}, ${adjustedB})`;
    }
    
    // Convert HSL to Hex
    function hslToHex(h, s, l) {
        l /= 100;
        const a = s * Math.min(l, 1 - l) / 100;
        const f = n => {
            const k = (n + h / 30) % 12;
            const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
            return Math.round(255 * color).toString(16).padStart(2, '0');
        };
        return `#${f(0)}${f(8)}${f(4)}`;
    }
    
    // Calculate color brightness for text contrast
    function getBrightness(hexColor) {
        const rgb = hexColor.match(/\w\w/g);
        const r = parseInt(rgb[0], 16);
        const g = parseInt(rgb[1], 16);
        const b = parseInt(rgb[2], 16);
        return (r * 299 + g * 587 + b * 114) / 1000;
    }
    
    // Auto-submit form when filters change
    document.querySelectorAll('.filter-checkbox').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            this.form.submit();
        });
    });
    
    // Search suggestions (basic implementation)
    const searchInput = document.querySelector('.search-input');
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length > 2) {
            searchTimeout = setTimeout(function() {
                // You can implement live search here
                console.log('Searching for:', query);
            }, 300);
        }
    });