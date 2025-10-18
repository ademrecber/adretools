from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date

def horoscope_home(request):
    return render(request, 'horoscope_tools/home.html')

@csrf_exempt
def calculate_horoscope(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        birth_date = request.POST.get('birth_date')
        birth_time = request.POST.get('birth_time', '12:00')
        birth_place = request.POST.get('birth_place', 'İstanbul')
        
        if not birth_date:
            return JsonResponse({'error': 'Birth date required'}, status=400)
        
        # Tarihi parse et
        birth_datetime = datetime.strptime(birth_date, '%Y-%m-%d')
        
        # Burç hesapla
        zodiac_sign = get_zodiac_sign(birth_datetime.month, birth_datetime.day)
        
        # Yaş hesapla
        today = date.today()
        age = today.year - birth_datetime.year - ((today.month, today.day) < (birth_datetime.month, birth_datetime.day))
        
        # Çin burcu hesapla
        chinese_zodiac = get_chinese_zodiac(birth_datetime.year)
        
        # Yükseleni hesapla (basit yaklaşım)
        ascendant = get_ascendant(birth_datetime.month, birth_datetime.day, birth_time)
        
        # Yaşam sayısı hesapla
        life_number = calculate_life_number(birth_datetime)
        
        return JsonResponse({
            'zodiac_sign': zodiac_sign,
            'chinese_zodiac': chinese_zodiac,
            'ascendant': ascendant,
            'age': age,
            'life_number': life_number,
            'birth_info': {
                'date': birth_datetime.strftime('%d.%m.%Y'),
                'day_of_week': get_turkish_day(birth_datetime.weekday()),
                'season': get_season(birth_datetime.month)
            }
        })
        
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Calculation error: {str(e)}'}, status=500)

def get_zodiac_sign(month, day):
    zodiac_signs = {
        'Aries': {'dates': [(3, 21), (4, 19)], 'element': 'Fire', 'planet': 'Mars', 'traits': ['Leader', 'Brave', 'Energetic', 'Impatient']},
        'Taurus': {'dates': [(4, 20), (5, 20)], 'element': 'Earth', 'planet': 'Venus', 'traits': ['Patient', 'Reliable', 'Stubborn', 'Practical']},
        'Gemini': {'dates': [(5, 21), (6, 20)], 'element': 'Air', 'planet': 'Mercury', 'traits': ['Smart', 'Talkative', 'Curious', 'Changeable']},
        'Cancer': {'dates': [(6, 21), (7, 22)], 'element': 'Water', 'planet': 'Moon', 'traits': ['Emotional', 'Protective', 'Intuitive', 'Sensitive']},
        'Leo': {'dates': [(7, 23), (8, 22)], 'element': 'Fire', 'planet': 'Sun', 'traits': ['Proud', 'Creative', 'Generous', 'Dramatic']},
        'Virgo': {'dates': [(8, 23), (9, 22)], 'element': 'Earth', 'planet': 'Mercury', 'traits': ['Perfectionist', 'Analytical', 'Practical', 'Critical']},
        'Libra': {'dates': [(9, 23), (10, 22)], 'element': 'Air', 'planet': 'Venus', 'traits': ['Balanced', 'Fair', 'Diplomatic', 'Indecisive']},
        'Scorpio': {'dates': [(10, 23), (11, 21)], 'element': 'Water', 'planet': 'Pluto', 'traits': ['Passionate', 'Mysterious', 'Strong', 'Jealous']},
        'Sagittarius': {'dates': [(11, 22), (12, 21)], 'element': 'Fire', 'planet': 'Jupiter', 'traits': ['Free', 'Optimistic', 'Adventurous', 'Honest']},
        'Capricorn': {'dates': [(12, 22), (12, 31), (1, 1), (1, 19)], 'element': 'Earth', 'planet': 'Saturn', 'traits': ['Disciplined', 'Ambitious', 'Responsible', 'Conservative']},
        'Aquarius': {'dates': [(1, 20), (2, 18)], 'element': 'Air', 'planet': 'Uranus', 'traits': ['Original', 'Independent', 'Humanitarian', 'Rebellious']},
        'Pisces': {'dates': [(2, 19), (3, 20)], 'element': 'Water', 'planet': 'Neptune', 'traits': ['Intuitive', 'Creative', 'Compassionate', 'Dreamy']}
    }
    
    for sign, info in zodiac_signs.items():
        dates = info['dates']
        if len(dates) == 2:  # Normal burçlar
            start_month, start_day = dates[0]
            end_month, end_day = dates[1]
            if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                return {'name': sign, **info}
        else:  # Oğlak (yıl sonu/başı)
            if (month == 12 and day >= 22) or (month == 1 and day <= 19):
                return {'name': sign, **info}
    
    return {'name': 'Unknown', 'element': '', 'planet': '', 'traits': []}

def get_chinese_zodiac(year):
    animals = ['Monkey', 'Rooster', 'Dog', 'Pig', 'Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat']
    elements = ['Metal', 'Water', 'Wood', 'Fire', 'Earth']
    
    animal_index = year % 12
    element_index = (year % 10) // 2
    
    animal = animals[animal_index]
    element = elements[element_index]
    
    traits = {
        'Rat': ['Smart', 'Adaptable', 'Hardworking'],
        'Ox': ['Reliable', 'Strong', 'Determined'],
        'Tiger': ['Brave', 'Competitive', 'Confident'],
        'Rabbit': ['Gentle', 'Lucky', 'Artistic'],
        'Dragon': ['Strong', 'Energetic', 'Lucky'],
        'Snake': ['Wise', 'Intuitive', 'Mysterious'],
        'Horse': ['Animated', 'Active', 'Energetic'],
        'Goat': ['Calm', 'Gentle', 'Compassionate'],
        'Monkey': ['Sharp', 'Smart', 'Curious'],
        'Rooster': ['Observant', 'Hardworking', 'Courageous'],
        'Dog': ['Responsible', 'Reliable', 'Loyal'],
        'Pig': ['Compassionate', 'Generous', 'Honest']
    }
    
    return {
        'animal': animal,
        'element': element,
        'full_name': f'{element} {animal}',
        'traits': traits.get(animal, [])
    }

def get_ascendant(month, day, birth_time):
    # Basit yükseleni hesaplama (gerçek hesaplama çok karmaşık)
    hour = int(birth_time.split(':')[0])
    
    # Doğum saatine göre yükseleni tahmin et
    ascendant_map = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    # Basit formül: (doğum saati + ay) % 12
    index = (hour + month) % 12
    return ascendant_map[index]

def calculate_life_number(birth_date):
    # Yaşam sayısı hesaplama (numeroloji)
    date_str = birth_date.strftime('%d%m%Y')
    total = sum(int(digit) for digit in date_str)
    
    # Tek haneli sayıya indir
    while total > 9 and total not in [11, 22, 33]:  # Master sayılar
        total = sum(int(digit) for digit in str(total))
    
    meanings = {
        1: 'Leadership, Independence, Innovation',
        2: 'Cooperation, Balance, Diplomacy',
        3: 'Creativity, Communication, Joy',
        4: 'Order, Hard Work, Practicality',
        5: 'Freedom, Adventure, Change',
        6: 'Responsibility, Love, Service',
        7: 'Spirituality, Analysis, Insight',
        8: 'Success, Power, Material Gain',
        9: 'Humanitarianism, Wisdom, Completion',
        11: 'Intuition, Inspiration, Spiritual Leadership',
        22: 'Master Builder, Big Projects',
        33: 'Master Teacher, Compassion, Service'
    }
    
    return {
        'number': total,
        'meaning': meanings.get(total, 'Unknown')
    }

def get_turkish_day(weekday):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[weekday]

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'