#!/usr/bin/env python3
"""
Создает полный файл locations.js с переводами всех стран на 4 языка
"""

import json
import re

# Загружаем словарь переводов (из предыдущего скрипта)
country_translations = {
    'Россия': {'en': 'Russia', 'zh': '俄罗斯', 'es': 'Rusia'},
    'Китай': {'en': 'China', 'zh': '中国', 'es': 'China'},
    'США': {'en': 'United States', 'zh': '美国', 'es': 'Estados Unidos'},
    'Бразилия': {'en': 'Brazil', 'zh': '巴西', 'es': 'Brasil'},
    'Индия': {'en': 'India', 'zh': '印度', 'es': 'India'},
    'Индонезия': {'en': 'Indonesia', 'zh': '印度尼西亚', 'es': 'Indonesia'},
    'Мексика': {'en': 'Mexico', 'zh': '墨西哥', 'es': 'México'},
    'Филиппины': {'en': 'Philippines', 'zh': '菲律宾', 'es': 'Filipinas'},
    'Таиланд': {'en': 'Thailand', 'zh': '泰国', 'es': 'Tailandia'},
    'Вьетнам': {'en': 'Vietnam', 'zh': '越南', 'es': 'Vietnam'},
    'Испания': {'en': 'Spain', 'zh': '西班牙', 'es': 'España'},
    'Италия': {'en': 'Italy', 'zh': '意大利', 'es': 'Italia'},
    'Франция': {'en': 'France', 'zh': '法国', 'es': 'Francia'},
    'Германия': {'en': 'Germany', 'zh': '德国', 'es': 'Alemania'},
    'Великобритания': {'en': 'United Kingdom', 'zh': '英国', 'es': 'Reino Unido'},
    'Япония': {'en': 'Japan', 'zh': '日本', 'es': 'Japón'},
    'Австралия': {'en': 'Australia', 'zh': '澳大利亚', 'es': 'Australia'},
    'Канада': {'en': 'Canada', 'zh': '加拿大', 'es': 'Canadá'},
    'Аргентина': {'en': 'Argentina', 'zh': '阿根廷', 'es': 'Argentina'},
    'Колумбия': {'en': 'Colombia', 'zh': '哥伦比亚', 'es': 'Colombia'},
    'Чили': {'en': 'Chile', 'zh': '智利', 'es': 'Chile'},
    'Перу': {'en': 'Peru', 'zh': '秘鲁', 'es': 'Perú'},
    'Египет': {'en': 'Egypt', 'zh': '埃及', 'es': 'Egipto'},
    'ЮАР': {'en': 'South Africa', 'zh': '南非', 'es': 'Sudáfrica'},
    'Нигерия': {'en': 'Nigeria', 'zh': '尼日利亚', 'es': 'Nigeria'},
    'Кения': {'en': 'Kenya', 'zh': '肯尼亚', 'es': 'Kenia'},
    'Турция': {'en': 'Turkey', 'zh': '土耳其', 'es': 'Turquía'},
    'ОАЭ': {'en': 'UAE', 'zh': '阿联酋', 'es': 'EAU'},
    'Саудовская Аравия': {'en': 'Saudi Arabia', 'zh': '沙特阿拉伯', 'es': 'Arabia Saudí'},
    'Израиль': {'en': 'Israel', 'zh': '以色列', 'es': 'Israel'},
    'Южная Корея': {'en': 'South Korea', 'zh': '韩国', 'es': 'Corea del Sur'},
    'Малайзия': {'en': 'Malaysia', 'zh': '马来西亚', 'es': 'Malasia'},
    'Сингапур': {'en': 'Singapore', 'zh': '新加坡', 'es': 'Singapur'},
    'Новая Зеландия': {'en': 'New Zealand', 'zh': '新西兰', 'es': 'Nueva Zelanda'},
    'Албания': {'en': 'Albania', 'zh': '阿尔巴尼亚', 'es': 'Albania'},
    'Андорра': {'en': 'Andorra', 'zh': '安道尔', 'es': 'Andorra'},
    'Австрия': {'en': 'Austria', 'zh': '奥地利', 'es': 'Austria'},
    'Беларусь': {'en': 'Belarus', 'zh': '白俄罗斯', 'es': 'Bielorrusia'},
    'Бельгия': {'en': 'Belgium', 'zh': '比利时', 'es': 'Bélgica'},
    'Босния и Герцеговина': {'en': 'Bosnia and Herzegovina', 'zh': '波黑', 'es': 'Bosnia y Herzegovina'},
    'Болгария': {'en': 'Bulgaria', 'zh': '保加利亚', 'es': 'Bulgaria'},
    'Хорватия': {'en': 'Croatia', 'zh': '克罗地亚', 'es': 'Croacia'},
    'Кипр': {'en': 'Cyprus', 'zh': '塞浦路斯', 'es': 'Chipre'},
    'Чехия': {'en': 'Czech Republic', 'zh': '捷克', 'es': 'República Checa'},
    'Дания': {'en': 'Denmark', 'zh': '丹麦', 'es': 'Dinamarca'},
    'Эстония': {'en': 'Estonia', 'zh': '爱沙尼亚', 'es': 'Estonia'},
    'Финляндия': {'en': 'Finland', 'zh': '芬兰', 'es': 'Finlandia'},
    'Греция': {'en': 'Greece', 'zh': '希腊', 'es': 'Grecia'},
    'Венгрия': {'en': 'Hungary', 'zh': '匈牙利', 'es': 'Hungría'},
    'Исландия': {'en': 'Iceland', 'zh': '冰岛', 'es': 'Islandia'},
    'Ирландия': {'en': 'Ireland', 'zh': '爱尔兰', 'es': 'Irlanda'},
    'Латвия': {'en': 'Latvia', 'zh': '拉脱维亚', 'es': 'Letonia'},
    'Литва': {'en': 'Lithuania', 'zh': '立陶宛', 'es': 'Lituania'},
    'Люксембург': {'en': 'Luxembourg', 'zh': '卢森堡', 'es': 'Luxemburgo'},
    'Мальта': {'en': 'Malta', 'zh': '马耳他', 'es': 'Malta'},
    'Молдова': {'en': 'Moldova', 'zh': '摩尔多瓦', 'es': 'Moldavia'},
    'Монако': {'en': 'Monaco', 'zh': '摩纳哥', 'es': 'Mónaco'},
    'Черногория': {'en': 'Montenegro', 'zh': '黑山', 'es': 'Montenegro'},
    'Нидерланды': {'en': 'Netherlands', 'zh': '荷兰', 'es': 'Países Bajos'},
    'Северная Македония': {'en': 'North Macedonia', 'zh': '北马其顿', 'es': 'Macedonia del Norte'},
    'Норвегия': {'en': 'Norway', 'zh': '挪威', 'es': 'Noruega'},
    'Польша': {'en': 'Poland', 'zh': '波兰', 'es': 'Polonia'},
    'Португалия': {'en': 'Portugal', 'zh': '葡萄牙', 'es': 'Portugal'},
    'Румыния': {'en': 'Romania', 'zh': '罗马尼亚', 'es': 'Rumania'},
    'Сербия': {'en': 'Serbia', 'zh': '塞尔维亚', 'es': 'Serbia'},
    'Словакия': {'en': 'Slovakia', 'zh': '斯洛伐克', 'es': 'Eslovaquia'},
    'Словения': {'en': 'Slovenia', 'zh': '斯洛文尼亚', 'es': 'Eslovenia'},
    'Швейцария': {'en': 'Switzerland', 'zh': '瑞士', 'es': 'Suiza'},
    'Украина': {'en': 'Ukraine', 'zh': '乌克兰', 'es': 'Ucrania'},
    'Швеция': {'en': 'Sweden', 'zh': '瑞典', 'es': 'Suecia'},
    'Афганистан': {'en': 'Afghanistan', 'zh': '阿富汗', 'es': 'Afganistán'},
    'Бангладеш': {'en': 'Bangladesh', 'zh': '孟加拉国', 'es': 'Bangladesh'},
    'Бутан': {'en': 'Bhutan', 'zh': '不丹', 'es': 'Bután'},
    'Бруней': {'en': 'Brunei', 'zh': '文莱', 'es': 'Brunéi'},
    'Камбоджа': {'en': 'Cambodia', 'zh': '柬埔寨', 'es': 'Camboya'},
    'Мьянма': {'en': 'Myanmar', 'zh': '缅甸', 'es': 'Myanmar'},
    'Непал': {'en': 'Nepal', 'zh': '尼泊尔', 'es': 'Nepal'},
    'Пакистан': {'en': 'Pakistan', 'zh': '巴基斯坦', 'es': 'Pakistán'},
    'Шри-Ланка': {'en': 'Sri Lanka', 'zh': '斯里兰卡', 'es': 'Sri Lanka'},
    'Лаос': {'en': 'Laos', 'zh': '老挝', 'es': 'Laos'},
    'Монголия': {'en': 'Mongolia', 'zh': '蒙古', 'es': 'Mongolia'},
    'Северная Корея': {'en': 'North Korea', 'zh': '朝鲜', 'es': 'Corea del Norte'},
    'Казахстан': {'en': 'Kazakhstan', 'zh': '哈萨克斯坦', 'es': 'Kazajistán'},
    'Кыргызстан': {'en': 'Kyrgyzstan', 'zh': '吉尔吉斯斯坦', 'es': 'Kirguistán'},
    'Таджикистан': {'en': 'Tajikistan', 'zh': '塔吉克斯坦', 'es': 'Tayikistán'},
    'Туркменистан': {'en': 'Turkmenistan', 'zh': '土库曼斯坦', 'es': 'Turkmenistán'},
    'Узбекистан': {'en': 'Uzbekistan', 'zh': '乌兹别克斯坦', 'es': 'Uzbekistán'},
    'Армения': {'en': 'Armenia', 'zh': '亚美尼亚', 'es': 'Armenia'},
    'Азербайджан': {'en': 'Azerbaijan', 'zh': '阿塞拜疆', 'es': 'Azerbaiyán'},
    'Грузия': {'en': 'Georgia', 'zh': '格鲁吉亚', 'es': 'Georgia'},
    'Мальдивы': {'en': 'Maldives', 'zh': '马尔代夫', 'es': 'Maldivas'},
    'Тимор-Лешти': {'en': 'East Timor', 'zh': '东帝汶', 'es': 'Timor Oriental'},
    'Алжир': {'en': 'Algeria', 'zh': '阿尔及利亚', 'es': 'Argelia'},
    'Ангола': {'en': 'Angola', 'zh': '安哥拉', 'es': 'Angola'},
    'Бенин': {'en': 'Benin', 'zh': '贝宁', 'es': 'Benín'},
    'Ботсвана': {'en': 'Botswana', 'zh': '博茨瓦纳', 'es': 'Botsuana'},
    'Буркина-Фасо': {'en': 'Burkina Faso', 'zh': '布基纳法索', 'es': 'Burkina Faso'},
    'Бурунди': {'en': 'Burundi', 'zh': '布隆迪', 'es': 'Burundi'},
    'Камерун': {'en': 'Cameroon', 'zh': '喀麦隆', 'es': 'Camerún'},
    'ЦАР': {'en': 'Central African Republic', 'zh': '中非', 'es': 'República Centroafricana'},
    'Чад': {'en': 'Chad', 'zh': '乍得', 'es': 'Chad'},
    'Коморы': {'en': 'Comoros', 'zh': '科摩罗', 'es': 'Comoras'},
    'Конго': {'en': 'Congo', 'zh': '刚果', 'es': 'Congo'},
    'ДР Конго': {'en': 'DR Congo', 'zh': '刚果民主共和国', 'es': 'RD del Congo'},
    'Кот-д\'Ивуар': {'en': 'Ivory Coast', 'zh': '科特迪瓦', 'es': 'Costa de Marfil'},
    'Джибути': {'en': 'Djibouti', 'zh': '吉布提', 'es': 'Yibuti'},
    'Экваториальная Гвинея': {'en': 'Equatorial Guinea', 'zh': '赤道几内亚', 'es': 'Guinea Ecuatorial'},
    'Эритрея': {'en': 'Eritrea', 'zh': '厄立特里亚', 'es': 'Eritrea'},
    'Эсватини': {'en': 'Eswatini', 'zh': '斯威士兰', 'es': 'Esuatini'},
    'Эфиопия': {'en': 'Ethiopia', 'zh': '埃塞俄比亚', 'es': 'Etiopía'},
    'Габон': {'en': 'Gabon', 'zh': '加蓬', 'es': 'Gabón'},
    'Гамбия': {'en': 'Gambia', 'zh': '冈比亚', 'es': 'Gambia'},
    'Гана': {'en': 'Ghana', 'zh': '加纳', 'es': 'Ghana'},
    'Гвинея': {'en': 'Guinea', 'zh': '几内亚', 'es': 'Guinea'},
    'Гвинея-Бисау': {'en': 'Guinea-Bissau', 'zh': '几内亚比绍', 'es': 'Guinea-Bisáu'},
    'Лесото': {'en': 'Lesotho', 'zh': '莱索托', 'es': 'Lesoto'},
    'Либерия': {'en': 'Liberia', 'zh': '利比里亚', 'es': 'Liberia'},
    'Ливия': {'en': 'Libya', 'zh': '利比亚', 'es': 'Libia'},
    'Мадагаскар': {'en': 'Madagascar', 'zh': '马达加斯加', 'es': 'Madagascar'},
    'Малави': {'en': 'Malawi', 'zh': '马拉维', 'es': 'Malaui'},
    'Мали': {'en': 'Mali', 'zh': '马里', 'es': 'Malí'},
    'Мавритания': {'en': 'Mauritania', 'zh': '毛里塔尼亚', 'es': 'Mauritania'},
    'Маврикий': {'en': 'Mauritius', 'zh': '毛里求斯', 'es': 'Mauricio'},
    'Марокко': {'en': 'Morocco', 'zh': '摩洛哥', 'es': 'Marruecos'},
    'Мозамбик': {'en': 'Mozambique', 'zh': '莫桑比克', 'es': 'Mozambique'},
    'Намибия': {'en': 'Namibia', 'zh': '纳米比亚', 'es': 'Namibia'},
    'Нигер': {'en': 'Niger', 'zh': '尼日尔', 'es': 'Níger'},
    'Руанда': {'en': 'Rwanda', 'zh': '卢旺达', 'es': 'Ruanda'},
    'Сан-Томе и Принсипи': {'en': 'São Tomé and Príncipe', 'zh': '圣多美和普林西比', 'es': 'Santo Tomé y Príncipe'},
    'Сенегал': {'en': 'Senegal', 'zh': '塞内加尔', 'es': 'Senegal'},
    'Сейшелы': {'en': 'Seychelles', 'zh': '塞舌尔', 'es': 'Seychelles'},
    'Сьерра-Леоне': {'en': 'Sierra Leone', 'zh': '塞拉利昂', 'es': 'Sierra Leona'},
    'Сомали': {'en': 'Somalia', 'zh': '索马里', 'es': 'Somalia'},
    'Судан': {'en': 'Sudan', 'zh': '苏丹', 'es': 'Sudán'},
    'Танзания': {'en': 'Tanzania', 'zh': '坦桑尼亚', 'es': 'Tanzania'},
    'Того': {'en': 'Togo', 'zh': '多哥', 'es': 'Togo'},
    'Тунис': {'en': 'Tunisia', 'zh': '突尼斯', 'es': 'Túnez'},
    'Уганда': {'en': 'Uganda', 'zh': '乌干达', 'es': 'Uganda'},
    'Замбия': {'en': 'Zambia', 'zh': '赞比亚', 'es': 'Zambia'},
    'Зимбабве': {'en': 'Zimbabwe', 'zh': '津巴布韦', 'es': 'Zimbabue'},
    'Антигуа и Барбуда': {'en': 'Antigua and Barbuda', 'zh': '安提瓜和巴布达', 'es': 'Antigua y Barbuda'},
    'Багамы': {'en': 'Bahamas', 'zh': '巴哈马', 'es': 'Bahamas'},
    'Барбадос': {'en': 'Barbados', 'zh': '巴巴多斯', 'es': 'Barbados'},
    'Белиз': {'en': 'Belize', 'zh': '伯利兹', 'es': 'Belice'},
    'Боливия': {'en': 'Bolivia', 'zh': '玻利维亚', 'es': 'Bolivia'},
    'Коста-Рика': {'en': 'Costa Rica', 'zh': '哥斯达黎加', 'es': 'Costa Rica'},
    'Куба': {'en': 'Cuba', 'zh': '古巴', 'es': 'Cuba'},
    'Доминика': {'en': 'Dominica', 'zh': '多米尼克', 'es': 'Dominica'},
    'Доминиканская Республика': {'en': 'Dominican Republic', 'zh': '多米尼加共和国', 'es': 'República Dominicana'},
    'Эквадор': {'en': 'Ecuador', 'zh': '厄瓜多尔', 'es': 'Ecuador'},
    'Сальвадор': {'en': 'El Salvador', 'zh': '萨尔瓦多', 'es': 'El Salvador'},
    'Гренада': {'en': 'Grenada', 'zh': '格林纳达', 'es': 'Granada'},
    'Гватемала': {'en': 'Guatemala', 'zh': '危地马拉', 'es': 'Guatemala'},
    'Гайана': {'en': 'Guyana', 'zh': '圭亚那', 'es': 'Guyana'},
    'Гаити': {'en': 'Haiti', 'zh': '海地', 'es': 'Haití'},
    'Гондурас': {'en': 'Honduras', 'zh': '洪都拉斯', 'es': 'Honduras'},
    'Ямайка': {'en': 'Jamaica', 'zh': '牙买加', 'es': 'Jamaica'},
    'Никарагуа': {'en': 'Nicaragua', 'zh': '尼加拉瓜', 'es': 'Nicaragua'},
    'Панама': {'en': 'Panama', 'zh': '巴拿马', 'es': 'Panamá'},
    'Парагвай': {'en': 'Paraguay', 'zh': '巴拉圭', 'es': 'Paraguay'},
    'Сент-Китс и Невис': {'en': 'Saint Kitts and Nevis', 'zh': '圣基茨和尼维斯', 'es': 'San Cristóbal y Nieves'},
    'Сент-Люсия': {'en': 'Saint Lucia', 'zh': '圣卢西亚', 'es': 'Santa Lucía'},
    'Сент-Винсент и Гренадины': {'en': 'Saint Vincent and the Grenadines', 'zh': '圣文森特和格林纳丁斯', 'es': 'San Vicente y las Granadinas'},
    'Суринам': {'en': 'Suriname', 'zh': '苏里南', 'es': 'Surinam'},
    'Тринидад и Тобаго': {'en': 'Trinidad and Tobago', 'zh': '特立尼达和多巴哥', 'es': 'Trinidad y Tobago'},
    'Уругвай': {'en': 'Uruguay', 'zh': '乌拉圭', 'es': 'Uruguay'},
    'Венесуэла': {'en': 'Venezuela', 'zh': '委内瑞拉', 'es': 'Venezuela'},
    'Фиджи': {'en': 'Fiji', 'zh': '斐济', 'es': 'Fiyi'},
    'Папуа - Новая Гвинея': {'en': 'Papua New Guinea', 'zh': '巴布亚新几内亚', 'es': 'Papúa Nueva Guinea'},
    'Самоа': {'en': 'Samoa', 'zh': '萨摩亚', 'es': 'Samoa'},
    'Соломоновы Острова': {'en': 'Solomon Islands', 'zh': '所罗门群岛', 'es': 'Islas Salomón'},
    'Тонга': {'en': 'Tonga', 'zh': '汤加', 'es': 'Tonga'},
    'Вануату': {'en': 'Vanuatu', 'zh': '瓦努阿图', 'es': 'Vanuatu'},
    'Кирибати': {'en': 'Kiribati', 'zh': '基里巴斯', 'es': 'Kiribati'},
    'Маршалловы Острова': {'en': 'Marshall Islands', 'zh': '马绍尔群岛', 'es': 'Islas Marshall'},
    'Микронезия': {'en': 'Micronesia', 'zh': '密克罗尼西亚', 'es': 'Micronesia'},
    'Науру': {'en': 'Nauru', 'zh': '瑙鲁', 'es': 'Nauru'},
    'Палау': {'en': 'Palau', 'zh': '帕劳', 'es': 'Palaos'},
    'Тувалу': {'en': 'Tuvalu', 'zh': '图瓦卢', 'es': 'Tuvalu'},
    'Бахрейн': {'en': 'Bahrain', 'zh': '巴林', 'es': 'Baréin'},
    'Ирак': {'en': 'Iraq', 'zh': '伊拉克', 'es': 'Irak'},
    'Иордания': {'en': 'Jordan', 'zh': '约旦', 'es': 'Jordania'},
    'Кувейт': {'en': 'Kuwait', 'zh': '科威特', 'es': 'Kuwait'},
    'Ливан': {'en': 'Lebanon', 'zh': '黎巴嫩', 'es': 'Líbano'},
    'Оман': {'en': 'Oman', 'zh': '阿曼', 'es': 'Omán'},
    'Катар': {'en': 'Qatar', 'zh': '卡塔尔', 'es': 'Catar'},
    'Сирия': {'en': 'Syria', 'zh': '叙利亚', 'es': 'Siria'},
    'Йемен': {'en': 'Yemen', 'zh': '也门', 'es': 'Yemen'},
    'Лихтенштейн': {'en': 'Liechtenstein', 'zh': '列支敦士登', 'es': 'Liechtenstein'},
    'Сан-Марино': {'en': 'San Marino', 'zh': '圣马力诺', 'es': 'San Marino'},
    'Ватикан': {'en': 'Vatican', 'zh': '梵蒂冈', 'es': 'Vaticano'},
    'Кабо-Верде': {'en': 'Cape Verde', 'zh': '佛得角', 'es': 'Cabo Verde'},
    'Южный Судан': {'en': 'South Sudan', 'zh': '南苏丹', 'es': 'Sudán del Sur'},
}

def get_country_translation(country_ru, lang):
    """Получает перевод названия страны"""
    if country_ru in country_translations:
        return country_translations[country_ru].get(lang, country_ru)
    # Если перевода нет, используем транслитерацию или оригинал
    return country_ru

def generate_locations_file():
    """Генерирует полный файл locations.js"""
    print("Загрузка данных из countries_ru.json...")
    
    with open('countries_ru.json', 'r', encoding='utf-8') as f:
        countries_ru = json.load(f)
    
    print(f"Загружено стран: {len(countries_ru)}")
    
    # Создаем переводы для всех языков
    translations = {
        'ru': countries_ru,
        'en': {},
        'zh': {},
        'es': {}
    }
    
    for lang in ['en', 'zh', 'es']:
        print(f"Генерация переводов для {lang.upper()}...")
        for country_ru, country_data in countries_ru.items():
            country_translated = get_country_translation(country_ru, lang)
            translations[lang][country_translated] = {
                'coords': country_data['coords'],
                'regions': country_data['regions'].copy()  # Регионы пока оставляем на русском
            }
    
    # Генерируем файл
    print("Генерация файла locations.js...")
    
    output = "// Данные стран и регионов с координатами и влажностью\n"
    output += "const locationsData = {\n"
    
    for lang in ['ru', 'en', 'zh', 'es']:
        output += f"    '{lang}': {{\n"
        countries = translations[lang]
        
        for country_name in sorted(countries.keys()):
            country_data = countries[country_name]
            output += f"        '{country_name}': {{\n"
            output += f"            coords: [{country_data['coords']}],\n"
            output += "            regions: {\n"
            
            for region_name in sorted(country_data['regions'].keys()):
                region_data = country_data['regions'][region_name]
                humidity = region_data['humidity']
                coords = region_data['coords']
                output += f"                '{region_name}': {{ humidity: {humidity}, coords: [{coords}] }},\n"
            
            output += "            }\n"
            output += "        },\n"
        
        output += "    },\n"
    
    output += "};\n\n"
    output += """// Функция для получения данных локаций на текущем языке
function getLocationsData() {
    const lang = window.currentLang || 'ru';
    if (locationsData[lang]) {
        return locationsData[lang];
    }
    return locationsData['ru'];
}
"""
    
    # Сохраняем файл
    print("Сохранение файла...")
    with open('locations.js', 'w', encoding='utf-8') as f:
        f.write(output)
    
    print("\nГотово! Файл locations.js обновлен.")
    print("\nКоличество стран по языкам:")
    for lang in ['ru', 'en', 'zh', 'es']:
        print(f"  {lang.upper()}: {len(translations[lang])}")

if __name__ == '__main__':
    generate_locations_file()
