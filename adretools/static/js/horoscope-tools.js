// Burç Hesaplayıcı JavaScript

// Burç ikonları
const zodiacIcons = {
    'Koç': '♈',
    'Boğa': '♉',
    'İkizler': '♊',
    'Yengeç': '♋',
    'Aslan': '♌',
    'Başak': '♍',
    'Terazi': '♎',
    'Akrep': '♏',
    'Yay': '♐',
    'Oğlak': '♑',
    'Kova': '♒',
    'Balık': '♓'
};

// Çin burcu hayvan ikonları
const chineseIcons = {
    'Fare': '🐭',
    'Öküz': '🐂',
    'Kaplan': '🐅',
    'Tavşan': '🐰',
    'Ejder': '🐉',
    'Yılan': '🐍',
    'At': '🐎',
    'Keçi': '🐐',
    'Maymun': '🐵',
    'Horoz': '🐓',
    'Köpek': '🐕',
    'Domuz': '🐷'
};

// Bugünü ayarla
function setToday() {
    const today = new Date();
    const dateString = today.toISOString().split('T')[0];
    document.getElementById('birthDate').value = dateString;
}

// Formu temizle
function clearForm() {
    document.getElementById('birthDate').value = '';
    document.getElementById('birthTime').value = '12:00';
    document.getElementById('birthPlace').value = 'İstanbul';
    document.getElementById('resultCard').style.display = 'none';
}

// Burç hesapla
async function calculateHoroscope() {
    const birthDate = document.getElementById('birthDate').value;
    const birthTime = document.getElementById('birthTime').value;
    const birthPlace = document.getElementById('birthPlace').value;
    
    if (!birthDate) {
        alert('⚠️ İçerik Gerekli: Doğum tarihi girin!');
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
            alert('❌ Hata: ' + error.error);
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            alert('🔌 Bağlantı Sorunu: Django sunucusu çalışmıyor olabilir. Lütfen sunucuyu başlatın.');
        } else {
            alert('⚠️ Beklenmeyen Hata: ' + error.message);
        }
    }
}

// Sonuçları göster
function showResults(data) {
    // Batı burcu
    const zodiac = data.zodiac_sign;
    document.getElementById('zodiacIcon').textContent = zodiacIcons[zodiac.name] || '⭐';
    document.getElementById('zodiacName').textContent = zodiac.name;
    document.getElementById('zodiacElement').textContent = zodiac.element;
    document.getElementById('zodiacPlanet').textContent = zodiac.planet;
    
    // Burç özellikleri
    const traitsHtml = zodiac.traits.map(trait => 
        `<span class="trait-badge">${trait}</span>`
    ).join('');
    document.getElementById('zodiacTraits').innerHTML = traitsHtml;
    
    // Çin burcu
    const chinese = data.chinese_zodiac;
    document.getElementById('chineseAnimal').textContent = chineseIcons[chinese.animal] || '🐾';
    document.getElementById('chineseName').textContent = chinese.full_name;
    
    // Çin burcu özellikleri
    const chineseTraitsHtml = chinese.traits.map(trait => 
        `<span class="trait-badge">${trait}</span>`
    ).join('');
    document.getElementById('chineseTraits').innerHTML = chineseTraitsHtml;
    
    // Diğer bilgiler
    document.getElementById('ascendant').textContent = data.ascendant;
    document.getElementById('age').textContent = data.age + ' yaş';
    document.getElementById('lifeNumber').textContent = data.life_number.number;
    document.getElementById('lifeNumberMeaning').textContent = data.life_number.meaning;
    document.getElementById('season').textContent = data.birth_info.season;
    document.getElementById('dayOfWeek').textContent = data.birth_info.day_of_week + ', ' + data.birth_info.date;
    
    // Sonuç kartını göster
    document.getElementById('resultCard').style.display = 'block';
    
    // Sonuç kartına kaydır
    document.getElementById('resultCard').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

// Sayfa yüklendiğinde bugünü ayarla
document.addEventListener('DOMContentLoaded', function() {
    // Varsayılan olarak bugünü ayarlamayalım, kullanıcı kendisi seçsin
});