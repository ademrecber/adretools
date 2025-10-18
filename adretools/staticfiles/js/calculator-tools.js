// Calculator Tools JavaScript

// BMI Calculator
function calculateBMI() {
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);
    
    if (!weight || !height || weight <= 0 || height <= 0) {
        document.getElementById('bmiResult').innerHTML = 
            '<div class="alert alert-warning">Lütfen geçerli değerler girin!</div>';
        return;
    }
    
    const heightInMeters = height / 100;
    const bmi = weight / (heightInMeters * heightInMeters);
    
    let category, color;
    if (bmi < 18.5) {
        category = 'Zayıf';
        color = 'info';
    } else if (bmi < 25) {
        category = 'Normal';
        color = 'success';
    } else if (bmi < 30) {
        category = 'Fazla Kilolu';
        color = 'warning';
    } else {
        category = 'Obez';
        color = 'danger';
    }
    
    document.getElementById('bmiResult').innerHTML = `
        <div class="alert alert-${color}">
            <h5>BMI Sonucu: ${bmi.toFixed(1)}</h5>
            <p><strong>Kategori:</strong> ${category}</p>
            <small>
                • Zayıf: < 18.5<br>
                • Normal: 18.5 - 24.9<br>
                • Fazla Kilolu: 25 - 29.9<br>
                • Obez: ≥ 30
            </small>
        </div>
    `;
}

// Age Calculator
function calculateAge() {
    const birthDate = new Date(document.getElementById('birthDate').value);
    const today = new Date();
    
    if (!birthDate || birthDate > today) {
        document.getElementById('ageResult').innerHTML = 
            '<div class="alert alert-warning">Lütfen geçerli bir doğum tarihi girin!</div>';
        return;
    }
    
    let years = today.getFullYear() - birthDate.getFullYear();
    let months = today.getMonth() - birthDate.getMonth();
    let days = today.getDate() - birthDate.getDate();
    
    if (days < 0) {
        months--;
        days += new Date(today.getFullYear(), today.getMonth(), 0).getDate();
    }
    
    if (months < 0) {
        years--;
        months += 12;
    }
    
    const totalDays = Math.floor((today - birthDate) / (1000 * 60 * 60 * 24));
    const totalWeeks = Math.floor(totalDays / 7);
    const totalMonths = years * 12 + months;
    
    document.getElementById('ageResult').innerHTML = `
        <div class="alert alert-success">
            <h5>Yaşınız: ${years} yıl, ${months} ay, ${days} gün</h5>
            <hr>
            <p><strong>Toplam:</strong></p>
            <ul class="mb-0">
                <li>${totalMonths} ay</li>
                <li>${totalWeeks} hafta</li>
                <li>${totalDays} gün</li>
                <li>${totalDays * 24} saat</li>
            </ul>
        </div>
    `;
}

// World Clock
function updateWorldClocks() {
    const timezones = [
        { name: 'İstanbul', timezone: 'Europe/Istanbul', flag: '🇹🇷' },
        { name: 'London', timezone: 'Europe/London', flag: '🇬🇧' },
        { name: 'New York', timezone: 'America/New_York', flag: '🇺🇸' },
        { name: 'Tokyo', timezone: 'Asia/Tokyo', flag: '🇯🇵' },
        { name: 'Dubai', timezone: 'Asia/Dubai', flag: '🇦🇪' },
        { name: 'Sydney', timezone: 'Australia/Sydney', flag: '🇦🇺' },
        { name: 'Paris', timezone: 'Europe/Paris', flag: '🇫🇷' },
        { name: 'Moscow', timezone: 'Europe/Moscow', flag: '🇷🇺' }
    ];
    
    const clocksContainer = document.getElementById('worldClocks');
    clocksContainer.innerHTML = '';
    
    timezones.forEach(tz => {
        const now = new Date();
        const timeString = now.toLocaleString('tr-TR', {
            timeZone: tz.timezone,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
        
        clocksContainer.innerHTML += `
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-body text-center">
                        <h5>${tz.flag} ${tz.name}</h5>
                        <h4 class="text-primary">${timeString}</h4>
                    </div>
                </div>
            </div>
        `;
    });
}

// Percentage Calculator
function calculatePercentage() {
    const number = parseFloat(document.getElementById('number').value);
    const percentage = parseFloat(document.getElementById('percentage').value);
    
    if (isNaN(number) || isNaN(percentage)) {
        document.getElementById('percentResult').value = 'Geçersiz değer';
        return;
    }
    
    const result = (number * percentage) / 100;
    document.getElementById('percentResult').value = result.toFixed(2);
}

// Date Calculator
function calculateDateDiff() {
    const startDate = new Date(document.getElementById('startDate').value);
    const endDate = new Date(document.getElementById('endDate').value);
    
    if (!startDate || !endDate) {
        document.getElementById('dateResult').innerHTML = 
            '<div class="alert alert-warning">Lütfen her iki tarihi de girin!</div>';
        return;
    }
    
    if (startDate > endDate) {
        document.getElementById('dateResult').innerHTML = 
            '<div class="alert alert-warning">Başlangıç tarihi bitiş tarihinden sonra olamaz!</div>';
        return;
    }
    
    const timeDiff = endDate.getTime() - startDate.getTime();
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
    const weeksDiff = Math.floor(daysDiff / 7);
    const monthsDiff = Math.floor(daysDiff / 30.44);
    const yearsDiff = Math.floor(daysDiff / 365.25);
    
    document.getElementById('dateResult').innerHTML = `
        <div class="alert alert-success">
            <h5>Tarihler Arası Fark</h5>
            <ul class="mb-0">
                <li><strong>${daysDiff}</strong> gün</li>
                <li><strong>${weeksDiff}</strong> hafta</li>
                <li><strong>${monthsDiff}</strong> ay (yaklaşık)</li>
                <li><strong>${yearsDiff}</strong> yıl (yaklaşık)</li>
            </ul>
        </div>
    `;
}

// World Clock modal açıldığında saatleri güncelle
document.addEventListener('DOMContentLoaded', function() {
    const worldClockModal = document.getElementById('world-clockModal');
    if (worldClockModal) {
        worldClockModal.addEventListener('shown.bs.modal', function() {
            updateWorldClocks();
            // Her saniye güncelle
            const interval = setInterval(updateWorldClocks, 1000);
            
            // Modal kapandığında interval'i temizle
            worldClockModal.addEventListener('hidden.bs.modal', function() {
                clearInterval(interval);
            }, { once: true });
        });
    }
    
    // Percentage calculator real-time update
    const numberInput = document.getElementById('number');
    const percentageInput = document.getElementById('percentage');
    
    if (numberInput && percentageInput) {
        numberInput.addEventListener('input', calculatePercentage);
        percentageInput.addEventListener('input', calculatePercentage);
    }
});