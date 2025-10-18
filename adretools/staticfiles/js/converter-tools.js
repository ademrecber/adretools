// Birim Dönüştürücü JavaScript

let currentCategory = 'length';

// Birim tanımları
const units = {
    length: {
        'mm': 'Milimetre',
        'cm': 'Santimetre', 
        'm': 'Metre',
        'km': 'Kilometre',
        'inch': 'İnç',
        'ft': 'Feet',
        'yard': 'Yard',
        'mile': 'Mil'
    },
    weight: {
        'mg': 'Miligram',
        'g': 'Gram',
        'kg': 'Kilogram',
        'ton': 'Ton',
        'oz': 'Ons',
        'lb': 'Pound',
        'stone': 'Stone'
    },
    temperature: {
        'celsius': 'Celsius (°C)',
        'fahrenheit': 'Fahrenheit (°F)',
        'kelvin': 'Kelvin (K)'
    },
    area: {
        'mm2': 'Milimetre²',
        'cm2': 'Santimetre²',
        'm2': 'Metre²',
        'km2': 'Kilometre²',
        'inch2': 'İnç²',
        'ft2': 'Feet²',
        'acre': 'Acre',
        'hectare': 'Hektar'
    },
    volume: {
        'ml': 'Mililitre',
        'l': 'Litre',
        'm3': 'Metre³',
        'gallon_us': 'Galon (US)',
        'gallon_uk': 'Galon (UK)',
        'pint': 'Pint',
        'quart': 'Quart',
        'cup': 'Cup'
    },
    speed: {
        'mps': 'Metre/Saniye',
        'kmh': 'Kilometre/Saat',
        'mph': 'Mil/Saat',
        'knot': 'Knot',
        'fps': 'Feet/Saniye'
    }
};

// Hızlı dönüştürme örnekleri
const quickConversions = {
    length: [
        {from: 'm', to: 'cm', value: 1, label: '1 metre = 100 cm'},
        {from: 'km', to: 'm', value: 1, label: '1 kilometre = 1000 m'},
        {from: 'inch', to: 'cm', value: 1, label: '1 inç = 2.54 cm'},
        {from: 'ft', to: 'm', value: 1, label: '1 feet = 0.3048 m'}
    ],
    weight: [
        {from: 'kg', to: 'g', value: 1, label: '1 kilogram = 1000 g'},
        {from: 'lb', to: 'kg', value: 1, label: '1 pound = 0.454 kg'},
        {from: 'ton', to: 'kg', value: 1, label: '1 ton = 1000 kg'},
        {from: 'oz', to: 'g', value: 1, label: '1 ons = 28.35 g'}
    ],
    temperature: [
        {from: 'celsius', to: 'fahrenheit', value: 0, label: '0°C = 32°F'},
        {from: 'celsius', to: 'fahrenheit', value: 100, label: '100°C = 212°F'},
        {from: 'celsius', to: 'kelvin', value: 0, label: '0°C = 273.15 K'},
        {from: 'fahrenheit', to: 'celsius', value: 32, label: '32°F = 0°C'}
    ],
    area: [
        {from: 'm2', to: 'cm2', value: 1, label: '1 m² = 10,000 cm²'},
        {from: 'hectare', to: 'm2', value: 1, label: '1 hektar = 10,000 m²'},
        {from: 'acre', to: 'm2', value: 1, label: '1 acre = 4,047 m²'},
        {from: 'km2', to: 'hectare', value: 1, label: '1 km² = 100 hektar'}
    ],
    volume: [
        {from: 'l', to: 'ml', value: 1, label: '1 litre = 1000 ml'},
        {from: 'm3', to: 'l', value: 1, label: '1 m³ = 1000 litre'},
        {from: 'gallon_us', to: 'l', value: 1, label: '1 galon (US) = 3.785 l'},
        {from: 'cup', to: 'ml', value: 1, label: '1 cup = 237 ml'}
    ],
    speed: [
        {from: 'kmh', to: 'mps', value: 1, label: '1 km/h = 0.278 m/s'},
        {from: 'mph', to: 'kmh', value: 1, label: '1 mph = 1.609 km/h'},
        {from: 'knot', to: 'kmh', value: 1, label: '1 knot = 1.852 km/h'},
        {from: 'mps', to: 'kmh', value: 1, label: '1 m/s = 3.6 km/h'}
    ]
};

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', function() {
    selectCategory('length');
    
    // Input değiştiğinde otomatik dönüştür
    document.getElementById('inputValue').addEventListener('input', convertUnit);
    document.getElementById('fromUnit').addEventListener('change', convertUnit);
    document.getElementById('toUnit').addEventListener('change', convertUnit);
});

// Kategori seç
function selectCategory(category) {
    currentCategory = category;
    
    // Aktif kategori butonunu güncelle
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Birim listelerini güncelle
    updateUnitSelects();
    
    // Hızlı dönüştürmeleri güncelle
    updateQuickConversions();
    
    // Dönüştürme yap
    convertUnit();
}

// Birim seçim listelerini güncelle
function updateUnitSelects() {
    const fromSelect = document.getElementById('fromUnit');
    const toSelect = document.getElementById('toUnit');
    
    // Listeleri temizle
    fromSelect.innerHTML = '';
    toSelect.innerHTML = '';
    
    // Yeni seçenekleri ekle
    const categoryUnits = units[currentCategory];
    Object.keys(categoryUnits).forEach(unit => {
        const option1 = new Option(categoryUnits[unit], unit);
        const option2 = new Option(categoryUnits[unit], unit);
        fromSelect.add(option1);
        toSelect.add(option2);
    });
    
    // Varsayılan seçimleri ayarla
    const unitKeys = Object.keys(categoryUnits);
    if (unitKeys.length > 1) {
        toSelect.selectedIndex = 1;
    }
}

// Hızlı dönüştürmeleri güncelle
function updateQuickConversions() {
    const quickList = document.getElementById('quickList');
    const conversions = quickConversions[currentCategory];
    
    quickList.innerHTML = conversions.map(conv => 
        `<div class="quick-convert" onclick="applyQuickConversion('${conv.from}', '${conv.to}', ${conv.value})">
            ${conv.label}
        </div>`
    ).join('');
}

// Hızlı dönüştürme uygula
function applyQuickConversion(from, to, value) {
    document.getElementById('inputValue').value = value;
    document.getElementById('fromUnit').value = from;
    document.getElementById('toUnit').value = to;
    convertUnit();
}

// Birimleri değiştir
function swapUnits() {
    const fromSelect = document.getElementById('fromUnit');
    const toSelect = document.getElementById('toUnit');
    
    const temp = fromSelect.value;
    fromSelect.value = toSelect.value;
    toSelect.value = temp;
    
    convertUnit();
}

// Birim dönüştürme
async function convertUnit() {
    const value = parseFloat(document.getElementById('inputValue').value) || 0;
    const fromUnit = document.getElementById('fromUnit').value;
    const toUnit = document.getElementById('toUnit').value;
    
    if (!fromUnit || !toUnit) return;
    
    const formData = new FormData();
    formData.append('category', currentCategory);
    formData.append('from_unit', fromUnit);
    formData.append('to_unit', toUnit);
    formData.append('value', value);
    
    try {
        const response = await fetch('/converter/convert/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('resultValue').textContent = data.formatted;
        } else {
            const error = await response.json();
            document.getElementById('resultValue').textContent = 'Hata: ' + error.error;
        }
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            document.getElementById('resultValue').textContent = 'Bağlantı Hatası';
        } else {
            document.getElementById('resultValue').textContent = 'Hata: ' + error.message;
        }
    }
}