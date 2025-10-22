// Horoscope Calculator JavaScript

// Zodiac icons
const zodiacIcons = {
    'Aries': '♈',
    'Taurus': '♉',
    'Gemini': '♊',
    'Cancer': '♋',
    'Leo': '♌',
    'Virgo': '♍',
    'Libra': '♎',
    'Scorpio': '♏',
    'Sagittarius': '♐',
    'Capricorn': '♑',
    'Aquarius': '♒',
    'Pisces': '♓'
};

// Chinese zodiac animal icons
const chineseIcons = {
    'Rat': '🐭',
    'Ox': '🐂',
    'Tiger': '🐅',
    'Rabbit': '🐰',
    'Dragon': '🐉',
    'Snake': '🐍',
    'Horse': '🐎',
    'Goat': '🐐',
    'Monkey': '🐵',
    'Rooster': '🐓',
    'Dog': '🐕',
    'Pig': '🐷'
};

// Set today
function setToday() {
    const today = new Date();
    const dateString = today.toISOString().split('T')[0];
    document.getElementById('birthDate').value = dateString;
}

// Clear form
function clearForm() {
    document.getElementById('birthDate').value = '';
    document.getElementById('birthTime').value = '12:00';
    document.getElementById('birthPlace').value = 'Istanbul';
    document.getElementById('resultCard').style.display = 'none';
}

// Calculate horoscope
async function calculateHoroscope() {
    const birthDate = document.getElementById('birthDate').value;
    const birthTime = document.getElementById('birthTime').value;
    const birthPlace = document.getElementById('birthPlace').value;
    
    if (!birthDate) {
        alert('⚠️ Input Required: Please enter birth date!');
        return;
    }
    
    const formData = new FormData();
    formData.append('birth_date', birthDate);
    formData.append('birth_time', birthTime);
    formData.append('birth_place', birthPlace);
    
    try {
        const response = await fetch('/horoscope/calculate/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            showResults(data);
        } else {
            const error = await response.json();
            alert('❌ Error: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Connection Issue: Django server may not be running. Please start the server.');
        } else {
            alert('⚠️ Unexpected Error: ' + error.message);
        }
    }
}

// Show results
function showResults(data) {
    // Western zodiac
    const zodiac = data.zodiac_sign;
    document.getElementById('zodiacIcon').textContent = zodiacIcons[zodiac.name] || '⭐';
    document.getElementById('zodiacName').textContent = zodiac.name;
    document.getElementById('zodiacElement').textContent = zodiac.element;
    document.getElementById('zodiacPlanet').textContent = zodiac.planet;
    
    // Zodiac traits
    const traitsHtml = zodiac.traits.map(trait => 
        `<span class="trait-badge">${trait}</span>`
    ).join('');
    document.getElementById('zodiacTraits').innerHTML = traitsHtml;
    
    // Chinese zodiac
    const chinese = data.chinese_zodiac;
    document.getElementById('chineseAnimal').textContent = chineseIcons[chinese.animal] || '🐾';
    document.getElementById('chineseName').textContent = chinese.full_name;
    
    // Chinese zodiac traits
    const chineseTraitsHtml = chinese.traits.map(trait => 
        `<span class="trait-badge">${trait}</span>`
    ).join('');
    document.getElementById('chineseTraits').innerHTML = chineseTraitsHtml;
    
    // Other information
    document.getElementById('ascendant').textContent = data.ascendant;
    document.getElementById('age').textContent = data.age + ' years';
    document.getElementById('lifeNumber').textContent = data.life_number.number;
    document.getElementById('lifeNumberMeaning').textContent = data.life_number.meaning;
    document.getElementById('season').textContent = data.birth_info.season;
    document.getElementById('dayOfWeek').textContent = data.birth_info.day_of_week + ', ' + data.birth_info.date;
    
    // Show result card
    document.getElementById('resultCard').style.display = 'block';
    
    // Scroll to result card
    document.getElementById('resultCard').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

// Set today on page load
document.addEventListener('DOMContentLoaded', function() {
    // Don't set today by default, let user choose
});