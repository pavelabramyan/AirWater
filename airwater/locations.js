// Данные стран и регионов с координатами и влажностью
const locationsData = {
    'ru': {
        'Австралия': {
            coords: [-25.2744, 133.7751],
            regions: {
            }
        },
        'Австрия': {
            coords: [47.5162, 14.5501],
            regions: {
            }
        },
        'Азербайджан': {
            coords: [40.1431, 47.5769],
            regions: {
            }
        },
        'Албания': {
            coords: [41.1533, 20.1683],
            regions: {
            }
        },
        'Алжир': {
            coords: [28.0339, 1.6596],
            regions: {
            }
        },
        'Ангола': {
            coords: [-11.2027, 17.8739],
            regions: {
            }
        },
        'Андорра': {
            coords: [42.5462, 1.6016],
            regions: {
            }
        },
        'Антигуа и Барбуда': {
            coords: [17.0608, -61.7964],
            regions: {
            }
        },
        'Аргентина': {
            coords: [-38.4161, -63.6167],
            regions: {
            }
        },
        'Армения': {
            coords: [40.0691, 45.0382],
            regions: {
            }
        },
        'Афганистан': {
            coords: [33.9391, 67.7100],
            regions: {
            }
        },
        'Багамы': {
            coords: [25.0343, -77.3963],
            regions: {
            }
        },
        'Бангладеш': {
            coords: [23.6850, 90.3563],
            regions: {
            }
        },
        'Барбадос': {
            coords: [13.1939, -59.5432],
            regions: {
            }
        },
        'Бахрейн': {
            coords: [26.0667, 50.5577],
            regions: {
            }
        },
        'Беларусь': {
            coords: [53.7098, 27.9534],
            regions: {
            }
        },
        'Белиз': {
            coords: [17.1899, -88.4976],
            regions: {
            }
        },
        'Бельгия': {
            coords: [50.5039, 4.4699],
            regions: {
            }
        },
        'Бенин': {
            coords: [9.3077, 2.3158],
            regions: {
            }
        },
        'Болгария': {
            coords: [42.7339, 25.4858],
            regions: {
            }
        },
        'Боливия': {
            coords: [-16.2902, -63.5887],
            regions: {
            }
        },
        'Босния и Герцеговина': {
            coords: [43.9159, 17.6791],
            regions: {
            }
        },
        'Ботсвана': {
            coords: [-22.3285, 24.6849],
            regions: {
            }
        },
        'Бразилия': {
            coords: [-14.2350, -51.9253],
            regions: {
            }
        },
        'Бруней': {
            coords: [4.5353, 114.7277],
            regions: {
            }
        },
        'Буркина-Фасо': {
            coords: [12.2383, -1.5616],
            regions: {
            }
        },
        'Бурунди': {
            coords: [-3.3731, 29.9189],
            regions: {
            }
        },
        'Бутан': {
            coords: [27.5142, 90.4336],
            regions: {
            }
        },
        'Вануату': {
            coords: [-15.3767, 166.9592],
            regions: {
            }
        },
        'Ватикан': {
            coords: [41.9029, 12.4534],
            regions: {
            }
        },
        'Великобритания': {
            coords: [55.3781, -3.4360],
            regions: {
            }
        },
        'Венгрия': {
            coords: [47.1625, 19.5033],
            regions: {
            }
        },
        'Венесуэла': {
            coords: [6.4238, -66.5897],
            regions: {
            }
        },
        'Вьетнам': {
            coords: [14.0583, 108.2772],
            regions: {
            }
        },
        'Габон': {
            coords: [-0.8037, 11.6094],
            regions: {
            }
        },
        'Гаити': {
            coords: [18.9712, -72.2852],
            regions: {
            }
        },
        'Гайана': {
            coords: [4.8604, -58.9302],
            regions: {
            }
        },
        'Гамбия': {
            coords: [13.4432, -15.3101],
            regions: {
            }
        },
        'Гана': {
            coords: [7.9465, -1.0232],
            regions: {
            }
        },
        'Гватемала': {
            coords: [15.7835, -90.2308],
            regions: {
            }
        },
        'Гвинея': {
            coords: [9.9456, -9.6966],
            regions: {
            }
        },
        'Гвинея-Бисау': {
            coords: [11.8037, -15.1804],
            regions: {
            }
        },
        'Германия': {
            coords: [51.1657, 10.4515],
            regions: {
            }
        },
        'Гондурас': {
            coords: [15.2000, -86.2419],
            regions: {
            }
        },
        'Гренада': {
            coords: [12.1165, -61.6790],
            regions: {
            }
        },
        'Греция': {
            coords: [39.0742, 21.8243],
            regions: {
            }
        },
        'Грузия': {
            coords: [42.3154, 43.3569],
            regions: {
            }
        },
        'ДР Конго': {
            coords: [-4.0383, 21.7587],
            regions: {
            }
        },
        'Дания': {
            coords: [56.2639, 9.5018],
            regions: {
            }
        },
        'Джибути': {
            coords: [11.8251, 42.5903],
            regions: {
            }
        },
        'Доминика': {
            coords: [15.4150, -61.3710],
            regions: {
            }
        },
        'Доминиканская Республика': {
            coords: [18.7357, -70.1627],
            regions: {
            }
        },
        'Египет': {
            coords: [26.8206, 30.8025],
            regions: {
            }
        },
        'Замбия': {
            coords: [-13.1339, 27.8493],
            regions: {
            }
        },
        'Зимбабве': {
            coords: [-19.0154, 29.1549],
            regions: {
            }
        },
        'Израиль': {
            coords: [31.0461, 34.8516],
            regions: {
            }
        },
        'Индия': {
            coords: [20.5937, 78.9629],
            regions: {
            }
        },
        'Индонезия': {
            coords: [-0.7893, 113.9213],
            regions: {
                'Джакарта': { humidity: 80, coords: [-6.2088, 106.8456], waterPriceUsd1L: 0.36 },
                'Западная Ява': { humidity: 78, coords: [-6.9175, 107.6191], waterPriceUsd1L: 0.30 },
                'Центральная Ява': { humidity: 78, coords: [-7.1510, 110.1403], waterPriceUsd1L: 0.27 },
                'Восточная Ява': { humidity: 76, coords: [-7.5361, 112.2384], waterPriceUsd1L: 0.30 },
                'Бантен': { humidity: 80, coords: [-6.4058, 106.0640], waterPriceUsd1L: 0.33 },
                'Джокьякарта': { humidity: 78, coords: [-7.7956, 110.3695], waterPriceUsd1L: 0.27 },
                'Бали': { humidity: 78, coords: [-8.4095, 115.1889], waterPriceUsd1L: 0.42 },
                'Западная Нуса-Тенгара': { humidity: 75, coords: [-8.6529, 117.3616], waterPriceUsd1L: 0.33 },
                'Восточная Нуса-Тенгара': { humidity: 70, coords: [-8.6574, 121.0794], waterPriceUsd1L: 0.36 },
                'Западный Калимантан': { humidity: 85, coords: [-0.2787, 111.4752], waterPriceUsd1L: 0.33 },
                'Центральный Калимантан': { humidity: 85, coords: [-1.6815, 113.3824], waterPriceUsd1L: 0.36 },
                'Южный Калимантан': { humidity: 82, coords: [-3.0926, 115.2838], waterPriceUsd1L: 0.33 },
                'Восточный Калимантан': { humidity: 82, coords: [0.5387, 116.4194], waterPriceUsd1L: 0.36 },
                'Северный Калимантан': { humidity: 85, coords: [3.0731, 116.0414], waterPriceUsd1L: 0.39 },
                'Северный Сулавеси': { humidity: 82, coords: [0.6247, 123.9750], waterPriceUsd1L: 0.36 },
                'Центральный Сулавеси': { humidity: 80, coords: [-1.4300, 121.4456], waterPriceUsd1L: 0.33 },
                'Южный Сулавеси': { humidity: 80, coords: [-3.6688, 119.9741], waterPriceUsd1L: 0.30 },
                'Юго-Восточный Сулавеси': { humidity: 82, coords: [-4.1449, 122.1746], waterPriceUsd1L: 0.33 },
                'Горонтало': { humidity: 80, coords: [0.6999, 122.4467], waterPriceUsd1L: 0.33 },
                'Западный Сулавеси': { humidity: 82, coords: [-2.8441, 119.2321], waterPriceUsd1L: 0.33 },
                'Малуку': { humidity: 85, coords: [-3.2385, 130.1453], waterPriceUsd1L: 0.39 },
                'Северное Малуку': { humidity: 85, coords: [1.5709, 127.8088], waterPriceUsd1L: 0.42 },
                'Папуа': { humidity: 85, coords: [-4.2699, 138.0804], waterPriceUsd1L: 0.45 },
                'Западное Папуа': { humidity: 85, coords: [-1.3361, 133.1747], waterPriceUsd1L: 0.45 },
                'Аче': { humidity: 82, coords: [4.6951, 96.7494], waterPriceUsd1L: 0.30 },
                'Северная Суматра': { humidity: 82, coords: [2.1154, 99.5451], waterPriceUsd1L: 0.30 },
                'Западная Суматра': { humidity: 82, coords: [-0.7399, 100.8000], waterPriceUsd1L: 0.30 },
                'Риау': { humidity: 85, coords: [0.2933, 101.7068], waterPriceUsd1L: 0.33 },
                'Острова Риау': { humidity: 85, coords: [3.9457, 108.1429], waterPriceUsd1L: 0.36 },
                'Джамби': { humidity: 82, coords: [-1.4852, 102.4381], waterPriceUsd1L: 0.30 },
                'Южная Суматра': { humidity: 82, coords: [-3.3194, 104.9147], waterPriceUsd1L: 0.30 },
                'Бангка-Белитунг': { humidity: 85, coords: [-2.7411, 106.4406], waterPriceUsd1L: 0.36 },
                'Бенкулу': { humidity: 82, coords: [-3.5778, 102.3464], waterPriceUsd1L: 0.30 },
                'Лампунг': { humidity: 80, coords: [-4.5586, 105.4068], waterPriceUsd1L: 0.30 },
            }
        },
        'Иордания': {
            coords: [30.5852, 36.2384],
            regions: {
            }
        },
        'Ирак': {
            coords: [33.2232, 43.6793],
            regions: {
            }
        },
        'Ирландия': {
            coords: [53.4129, -8.2439],
            regions: {
            }
        },
        'Исландия': {
            coords: [64.9631, -19.0208],
            regions: {
            }
        },
        'Испания': {
            coords: [40.4637, -3.7492],
            regions: {
            }
        },
        'Италия': {
            coords: [41.8719, 12.5674],
            regions: {
            }
        },
        'Йемен': {
            coords: [15.5527, 48.5164],
            regions: {
            }
        },
        'Кабо-Верде': {
            coords: [16.5388, -24.0132],
            regions: {
            }
        },
        'Казахстан': {
            coords: [48.0196, 66.9237],
            regions: {
            }
        },
        'Камбоджа': {
            coords: [12.5657, 104.9910],
            regions: {
            }
        },
        'Камерун': {
            coords: [7.3697, 12.3547],
            regions: {
            }
        },
        'Канада': {
            coords: [56.1304, -106.3468],
            regions: {
            }
        },
        'Катар': {
            coords: [25.3548, 51.1839],
            regions: {
            }
        },
        'Кения': {
            coords: [-0.0236, 37.9062],
            regions: {
            }
        },
        'Кипр': {
            coords: [35.1264, 33.4299],
            regions: {
            }
        },
        'Кирибати': {
            coords: [-3.3704, -168.7340],
            regions: {
            }
        },
        'Китай': {
            coords: [35.8617, 104.1954],
            regions: {
            }
        },
        'Колумбия': {
            coords: [4.5709, -74.2973],
            regions: {
            }
        },
        'Коморы': {
            coords: [-11.6455, 43.3333],
            regions: {
            }
        },
        'Конго': {
            coords: [-0.2280, 15.8277],
            regions: {
            }
        },
        'Коста-Рика': {
            coords: [9.7489, -83.7534],
            regions: {
            }
        },
        'Куба': {
            coords: [21.5218, -77.7812],
            regions: {
            }
        },
        'Кувейт': {
            coords: [29.3117, 47.4818],
            regions: {
            }
        },
        'Кыргызстан': {
            coords: [41.2044, 74.7661],
            regions: {
            }
        },
        'Лаос': {
            coords: [19.8563, 102.4955],
            regions: {
            }
        },
        'Латвия': {
            coords: [56.8796, 24.6032],
            regions: {
            }
        },
        'Лесото': {
            coords: [-29.6100, 28.2336],
            regions: {
            }
        },
        'Либерия': {
            coords: [6.4281, -9.4295],
            regions: {
            }
        },
        'Ливан': {
            coords: [33.8547, 35.8623],
            regions: {
            }
        },
        'Ливия': {
            coords: [26.3351, 17.2283],
            regions: {
            }
        },
        'Литва': {
            coords: [55.1694, 23.8813],
            regions: {
            }
        },
        'Лихтенштейн': {
            coords: [47.1660, 9.5554],
            regions: {
            }
        },
        'Люксембург': {
            coords: [49.8153, 6.1296],
            regions: {
            }
        },
        'Маврикий': {
            coords: [-20.3484, 57.5522],
            regions: {
            }
        },
        'Мавритания': {
            coords: [21.0079, -10.9408],
            regions: {
            }
        },
        'Мадагаскар': {
            coords: [-18.7669, 46.8691],
            regions: {
            }
        },
        'Малави': {
            coords: [-13.2543, 34.3015],
            regions: {
            }
        },
        'Малайзия': {
            coords: [4.2105, 101.9758],
            regions: {
            }
        },
        'Мали': {
            coords: [17.5707, -3.9962],
            regions: {
            }
        },
        'Мальдивы': {
            coords: [3.2028, 73.2207],
            regions: {
            }
        },
        'Мальта': {
            coords: [35.9375, 14.3754],
            regions: {
            }
        },
        'Марокко': {
            coords: [31.7917, -7.0926],
            regions: {
            }
        },
        'Маршалловы Острова': {
            coords: [7.1315, 171.1845],
            regions: {
            }
        },
        'Мексика': {
            coords: [23.6345, -102.5528],
            regions: {
            }
        },
        'Микронезия': {
            coords: [7.4256, 150.5508],
            regions: {
            }
        },
        'Мозамбик': {
            coords: [-18.6657, 35.5296],
            regions: {
            }
        },
        'Молдова': {
            coords: [47.4116, 28.3699],
            regions: {
            }
        },
        'Монако': {
            coords: [43.7384, 7.4246],
            regions: {
            }
        },
        'Монголия': {
            coords: [46.8625, 103.8467],
            regions: {
            }
        },
        'Мьянма': {
            coords: [21.9162, 95.9560],
            regions: {
            }
        },
        'Намибия': {
            coords: [-22.9576, 18.4904],
            regions: {
            }
        },
        'Науру': {
            coords: [-0.5228, 166.9315],
            regions: {
            }
        },
        'Непал': {
            coords: [28.3949, 84.1240],
            regions: {
            }
        },
        'Нигер': {
            coords: [17.6078, 8.0817],
            regions: {
            }
        },
        'Нигерия': {
            coords: [9.0820, 8.6753],
            regions: {
            }
        },
        'Нидерланды': {
            coords: [52.1326, 5.2913],
            regions: {
            }
        },
        'Никарагуа': {
            coords: [12.2650, -85.2072],
            regions: {
            }
        },
        'Новая Зеландия': {
            coords: [-40.9006, 174.8860],
            regions: {
            }
        },
        'Норвегия': {
            coords: [60.4720, 8.4689],
            regions: {
            }
        },
        'ОАЭ': {
            coords: [23.4241, 53.8478],
            regions: {
                'Абу-Даби': { humidity: 60, coords: [24.4539, 54.3773], waterPriceUsd1L: 0.35 },
                'Дубай': { humidity: 55, coords: [25.2048, 55.2708], waterPriceUsd1L: 0.40 },
                'Шарджа': { humidity: 55, coords: [25.3463, 55.4209], waterPriceUsd1L: 0.32 },
                'Аджман': { humidity: 55, coords: [25.4052, 55.5136], waterPriceUsd1L: 0.30 },
                'Умм-эль-Кувейн': { humidity: 50, coords: [25.5647, 55.5552], waterPriceUsd1L: 0.30 },
                'Рас-эль-Хайма': { humidity: 55, coords: [25.7895, 55.9432], waterPriceUsd1L: 0.30 },
                'Фуджейра': { humidity: 65, coords: [25.1288, 56.3264], waterPriceUsd1L: 0.32 }
            }
        },
        'Оман': {
            coords: [21.4735, 55.9754],
            regions: {
            }
        },
        'Пакистан': {
            coords: [30.3753, 69.3451],
            regions: {
            }
        },
        'Палау': {
            coords: [7.5150, 134.5825],
            regions: {
            }
        },
        'Панама': {
            coords: [8.5380, -80.7821],
            regions: {
            }
        },
        'Папуа - Новая Гвинея': {
            coords: [-6.3150, 143.9555],
            regions: {
            }
        },
        'Парагвай': {
            coords: [-23.4425, -58.4438],
            regions: {
            }
        },
        'Перу': {
            coords: [-9.1900, -75.0152],
            regions: {
            }
        },
        'Польша': {
            coords: [51.9194, 19.1451],
            regions: {
            }
        },
        'Португалия': {
            coords: [39.3999, -8.2245],
            regions: {
            }
        },
        'Россия': {
            coords: [61.5240, 105.3188],
            regions: {
                'Москва': { humidity: 70, coords: [55.7558, 37.6173], waterPriceUsd1L: 0.77 },
                'Московская область': { humidity: 70, coords: [55.5, 37.0], waterPriceUsd1L: 0.71 },
                'Санкт-Петербург': { humidity: 78, coords: [59.9311, 30.3609], waterPriceUsd1L: 0.71 },
                'Ленинградская область': { humidity: 78, coords: [59.5, 31.0], waterPriceUsd1L: 0.64 },
                'Севастополь': { humidity: 72, coords: [44.6167, 33.5254], waterPriceUsd1L: 0.64 },
                'Республика Крым': { humidity: 72, coords: [45.0, 34.0], waterPriceUsd1L: 0.64 },
                'Республика Адыгея': { humidity: 72, coords: [44.82, 40.18], waterPriceUsd1L: 0.58 },
                'Республика Алтай': { humidity: 60, coords: [50.71, 86.86], waterPriceUsd1L: 0.51 },
                'Республика Башкортостан': { humidity: 67, coords: [54.74, 55.96], waterPriceUsd1L: 0.51 },
                'Республика Бурятия': { humidity: 58, coords: [51.83, 107.58], waterPriceUsd1L: 0.51 },
                'Республика Дагестан': { humidity: 66, coords: [42.26, 47.10], waterPriceUsd1L: 0.51 },
                'Республика Ингушетия': { humidity: 66, coords: [43.17, 44.81], waterPriceUsd1L: 0.51 },
                'Кабардино-Балкарская Республика': { humidity: 66, coords: [43.39, 43.56], waterPriceUsd1L: 0.51 },
                'Республика Калмыкия': { humidity: 55, coords: [46.23, 45.33], waterPriceUsd1L: 0.51 },
                'Карачаево-Черкесская Республика': { humidity: 66, coords: [43.74, 41.73], waterPriceUsd1L: 0.51 },
                'Республика Карелия': { humidity: 78, coords: [63.56, 33.36], waterPriceUsd1L: 0.58 },
                'Республика Коми': { humidity: 78, coords: [64.0, 54.0], waterPriceUsd1L: 0.58 },
                'Республика Марий Эл': { humidity: 72, coords: [56.63, 47.87], waterPriceUsd1L: 0.51 },
                'Республика Мордовия': { humidity: 70, coords: [54.18, 45.17], waterPriceUsd1L: 0.51 },
                'Республика Саха (Якутия)': { humidity: 60, coords: [66.76, 124.12], waterPriceUsd1L: 0.77 },
                'Республика Северная Осетия — Алания': { humidity: 66, coords: [43.02, 44.68], waterPriceUsd1L: 0.51 },
                'Республика Татарстан': { humidity: 70, coords: [55.80, 49.11], waterPriceUsd1L: 0.58 },
                'Республика Тыва': { humidity: 55, coords: [51.72, 94.44], waterPriceUsd1L: 0.51 },
                'Удмуртская Республика': { humidity: 72, coords: [57.0, 53.0], waterPriceUsd1L: 0.51 },
                'Республика Хакасия': { humidity: 55, coords: [53.72, 91.44], waterPriceUsd1L: 0.51 },
                'Чеченская Республика': { humidity: 66, coords: [43.40, 45.70], waterPriceUsd1L: 0.51 },
                'Чувашская Республика': { humidity: 70, coords: [55.5, 47.0], waterPriceUsd1L: 0.51 },
                'Алтайский край': { humidity: 60, coords: [52.69, 82.69], waterPriceUsd1L: 0.51 },
                'Краснодарский край': { humidity: 75, coords: [45.0355, 38.9753], waterPriceUsd1L: 0.64 },
                'Красноярский край': { humidity: 60, coords: [64.25, 95.10], waterPriceUsd1L: 0.58 },
                'Приморский край': { humidity: 78, coords: [43.1155, 131.8855], waterPriceUsd1L: 0.64 },
                'Ставропольский край': { humidity: 68, coords: [44.67, 43.52], waterPriceUsd1L: 0.58 },
                'Хабаровский край': { humidity: 75, coords: [50.59, 135.0], waterPriceUsd1L: 0.64 },
                'Амурская область': { humidity: 65, coords: [52.8, 128.0], waterPriceUsd1L: 0.58 },
                'Архангельская область': { humidity: 78, coords: [63.0, 41.0], waterPriceUsd1L: 0.58 },
                'Астраханская область': { humidity: 55, coords: [46.35, 48.04], waterPriceUsd1L: 0.51 },
                'Белгородская область': { humidity: 68, coords: [50.60, 36.60], waterPriceUsd1L: 0.51 },
                'Брянская область': { humidity: 75, coords: [53.26, 34.37], waterPriceUsd1L: 0.51 },
                'Владимирская область': { humidity: 72, coords: [55.9, 40.4], waterPriceUsd1L: 0.58 },
                'Волгоградская область': { humidity: 60, coords: [49.6, 44.4], waterPriceUsd1L: 0.51 },
                'Вологодская область': { humidity: 78, coords: [59.22, 39.88], waterPriceUsd1L: 0.58 },
                'Воронежская область': { humidity: 65, coords: [51.67, 39.18], waterPriceUsd1L: 0.51 },
                'Ивановская область': { humidity: 75, coords: [57.0, 41.0], waterPriceUsd1L: 0.51 },
                'Иркутская область': { humidity: 60, coords: [56.0, 105.0], waterPriceUsd1L: 0.58 },
                'Калининградская область': { humidity: 80, coords: [54.7104, 20.4522], waterPriceUsd1L: 0.64 },
                'Калужская область': { humidity: 72, coords: [54.5, 35.5], waterPriceUsd1L: 0.58 },
                'Камчатский край': { humidity: 80, coords: [56.0, 159.0], waterPriceUsd1L: 0.90 },
                'Кемеровская область — Кузбасс': { humidity: 65, coords: [54.75, 87.14], waterPriceUsd1L: 0.51 },
                'Кировская область': { humidity: 72, coords: [58.5, 50.0], waterPriceUsd1L: 0.51 },
                'Костромская область': { humidity: 75, coords: [58.55, 43.95], waterPriceUsd1L: 0.51 },
                'Курганская область': { humidity: 65, coords: [55.45, 65.34], waterPriceUsd1L: 0.51 },
                'Курская область': { humidity: 68, coords: [51.74, 36.19], waterPriceUsd1L: 0.51 },
                'Липецкая область': { humidity: 68, coords: [52.60, 39.57], waterPriceUsd1L: 0.51 },
                'Магаданская область': { humidity: 78, coords: [62.0, 153.0], waterPriceUsd1L: 0.90 },
                'Мурманская область': { humidity: 80, coords: [68.96, 33.08], waterPriceUsd1L: 0.64 },
                'Нижегородская область': { humidity: 70, coords: [56.33, 44.01], waterPriceUsd1L: 0.58 },
                'Новгородская область': { humidity: 78, coords: [58.52, 31.28], waterPriceUsd1L: 0.58 },
                'Новосибирская область': { humidity: 60, coords: [55.0084, 82.9357], waterPriceUsd1L: 0.58 },
                'Омская область': { humidity: 60, coords: [54.99, 73.37], waterPriceUsd1L: 0.51 },
                'Оренбургская область': { humidity: 60, coords: [51.77, 55.10], waterPriceUsd1L: 0.51 },
                'Орловская область': { humidity: 72, coords: [52.97, 36.06], waterPriceUsd1L: 0.51 },
                'Пензенская область': { humidity: 68, coords: [53.19, 45.02], waterPriceUsd1L: 0.51 },
                'Пермский край': { humidity: 72, coords: [58.0, 56.32], waterPriceUsd1L: 0.58 },
                'Псковская область': { humidity: 78, coords: [57.82, 28.33], waterPriceUsd1L: 0.58 },
                'Ростовская область': { humidity: 60, coords: [47.2357, 39.7015], waterPriceUsd1L: 0.58 },
                'Рязанская область': { humidity: 72, coords: [54.63, 39.69], waterPriceUsd1L: 0.51 },
                'Самарская область': { humidity: 65, coords: [53.20, 50.16], waterPriceUsd1L: 0.58 },
                'Саратовская область': { humidity: 60, coords: [51.53, 46.03], waterPriceUsd1L: 0.51 },
                'Сахалинская область': { humidity: 85, coords: [50.69, 142.95], waterPriceUsd1L: 0.77 },
                'Свердловская область': { humidity: 65, coords: [56.8389, 60.6057], waterPriceUsd1L: 0.58 },
                'Смоленская область': { humidity: 75, coords: [54.78, 32.05], waterPriceUsd1L: 0.51 },
                'Тамбовская область': { humidity: 65, coords: [52.72, 41.45], waterPriceUsd1L: 0.51 },
                'Тверская область': { humidity: 75, coords: [56.86, 35.92], waterPriceUsd1L: 0.58 },
                'Томская область': { humidity: 70, coords: [58.60, 70.0], waterPriceUsd1L: 0.58 },
                'Тульская область': { humidity: 70, coords: [54.19, 37.62], waterPriceUsd1L: 0.58 },
                'Тюменская область': { humidity: 70, coords: [57.16, 68.43], waterPriceUsd1L: 0.58 },
                'Ульяновская область': { humidity: 65, coords: [54.32, 48.40], waterPriceUsd1L: 0.51 },
                'Челябинская область': { humidity: 65, coords: [55.16, 61.40], waterPriceUsd1L: 0.58 },
                'Забайкальский край': { humidity: 55, coords: [52.0, 115.0], waterPriceUsd1L: 0.58 },
                'Ярославская область': { humidity: 75, coords: [57.63, 39.88], waterPriceUsd1L: 0.58 },
                'Еврейская автономная область': { humidity: 70, coords: [48.8, 132.95], waterPriceUsd1L: 0.58 },
                'Ненецкий автономный округ': { humidity: 80, coords: [68.0, 53.0], waterPriceUsd1L: 0.77 },
                'Ханты-Мансийский автономный округ — Югра': { humidity: 75, coords: [61.0, 69.0], waterPriceUsd1L: 0.64 },
                'Чукотский автономный округ': { humidity: 78, coords: [66.0, 169.0], waterPriceUsd1L: 1.03 },
                'Ямало-Ненецкий автономный округ': { humidity: 78, coords: [66.5, 70.0], waterPriceUsd1L: 0.77 },
                'Донецкая Народная Республика': { humidity: 65, coords: [48.0, 37.8], waterPriceUsd1L: 0.51 },
                'Луганская Народная Республика': { humidity: 65, coords: [48.6, 39.3], waterPriceUsd1L: 0.51 },
                'Запорожская область': { humidity: 65, coords: [47.8, 35.2], waterPriceUsd1L: 0.51 },
                'Херсонская область': { humidity: 65, coords: [46.6, 33.6], waterPriceUsd1L: 0.51 },
            }
        },
        'Руанда': {
            coords: [-1.9403, 29.8739],
            regions: {
            }
        },
        'Румыния': {
            coords: [45.9432, 24.9668],
            regions: {
            }
        },
        'США': {
            coords: [37.0902, -95.7129],
            regions: {
            }
        },
        'Сальвадор': {
            coords: [13.7942, -88.8965],
            regions: {
            }
        },
        'Самоа': {
            coords: [-13.7590, -172.1046],
            regions: {
            }
        },
        'Сан-Марино': {
            coords: [43.9424, 12.4578],
            regions: {
            }
        },
        'Сан-Томе и Принсипи': {
            coords: [0.1864, 6.6131],
            regions: {
            }
        },
        'Саудовская Аравия': {
            coords: [23.8859, 45.0792],
            regions: {
                'Эр-Рияд': { humidity: 47, coords: [24.7136, 46.6753], waterPriceUsd1L: 0.40 },
                'Мекка': { humidity: 50, coords: [21.3891, 39.8579], waterPriceUsd1L: 0.45 },
                'Медина': { humidity: 40, coords: [24.5247, 39.5692], waterPriceUsd1L: 0.42 },
                'Восточная провинция': { humidity: 65, coords: [26.4207, 50.0888], waterPriceUsd1L: 0.38 },
                'Асир': { humidity: 55, coords: [18.2164, 42.5053], waterPriceUsd1L: 0.35 },
                'Джизан': { humidity: 70, coords: [16.8892, 42.5611], waterPriceUsd1L: 0.35 },
                'Наджран': { humidity: 35, coords: [17.4933, 44.1277], waterPriceUsd1L: 0.35 },
                'Аль-Баха': { humidity: 45, coords: [19.8614, 41.4414], waterPriceUsd1L: 0.35 },
                'Табук': { humidity: 35, coords: [28.3838, 36.5550], waterPriceUsd1L: 0.38 },
                'Аль-Джауф': { humidity: 35, coords: [29.7889, 39.8789], waterPriceUsd1L: 0.35 },
                'Северные границы': { humidity: 40, coords: [31.1728, 37.9888], waterPriceUsd1L: 0.35 },
                'Хаиль': { humidity: 35, coords: [27.5219, 41.6906], waterPriceUsd1L: 0.35 },
                'Аль-Касим': { humidity: 40, coords: [26.2076, 43.4839], waterPriceUsd1L: 0.35 }
            }
        },
        'Северная Корея': {
            coords: [40.3399, 127.5101],
            regions: {
            }
        },
        'Северная Македония': {
            coords: [41.6086, 21.7453],
            regions: {
            }
        },
        'Сейшелы': {
            coords: [-4.6796, 55.4920],
            regions: {
            }
        },
        'Сенегал': {
            coords: [14.4974, -14.4524],
            regions: {
            }
        },
        'Сент-Винсент и Гренадины': {
            coords: [12.9843, -61.2872],
            regions: {
            }
        },
        'Сент-Китс и Невис': {
            coords: [17.3578, -62.7830],
            regions: {
            }
        },
        'Сент-Люсия': {
            coords: [13.9094, -60.9789],
            regions: {
            }
        },
        'Сербия': {
            coords: [44.0165, 21.0059],
            regions: {
            }
        },
        'Сингапур': {
            coords: [1.3521, 103.8198],
            regions: {
            }
        },
        'Сирия': {
            coords: [34.8021, 38.9968],
            regions: {
            }
        },
        'Словакия': {
            coords: [48.6690, 19.6990],
            regions: {
            }
        },
        'Словения': {
            coords: [46.1512, 14.9955],
            regions: {
            }
        },
        'Соломоновы Острова': {
            coords: [-9.6457, 160.1562],
            regions: {
            }
        },
        'Сомали': {
            coords: [5.1521, 46.1996],
            regions: {
            }
        },
        'Судан': {
            coords: [12.8628, 30.2176],
            regions: {
            }
        },
        'Суринам': {
            coords: [3.9193, -56.0278],
            regions: {
            }
        },
        'Сьерра-Леоне': {
            coords: [8.4606, -11.7799],
            regions: {
            }
        },
        'Таджикистан': {
            coords: [38.8610, 71.2761],
            regions: {
            }
        },
        'Таиланд': {
            coords: [15.8700, 100.9925],
            regions: {
            }
        },
        'Танзания': {
            coords: [-6.3690, 34.8888],
            regions: {
            }
        },
        'Тимор-Лешти': {
            coords: [-8.8742, 125.7275],
            regions: {
            }
        },
        'Того': {
            coords: [8.6195, 0.8248],
            regions: {
            }
        },
        'Тонга': {
            coords: [-21.1789, -175.1982],
            regions: {
            }
        },
        'Тринидад и Тобаго': {
            coords: [10.6918, -61.2225],
            regions: {
            }
        },
        'Тувалу': {
            coords: [-7.1095, 177.6493],
            regions: {
            }
        },
        'Тунис': {
            coords: [33.8869, 9.5375],
            regions: {
            }
        },
        'Туркменистан': {
            coords: [38.9697, 59.5563],
            regions: {
            }
        },
        'Турция': {
            coords: [38.9637, 35.2433],
            regions: {
            }
        },
        'Уганда': {
            coords: [1.3733, 32.2903],
            regions: {
            }
        },
        'Узбекистан': {
            coords: [41.3775, 64.5853],
            regions: {
            }
        },
        'Украина': {
            coords: [48.3794, 31.1656],
            regions: {
            }
        },
        'Уругвай': {
            coords: [-32.5228, -55.7658],
            regions: {
            }
        },
        'Фиджи': {
            coords: [-16.7784, 178.0650],
            regions: {
            }
        },
        'Филиппины': {
            coords: [12.8797, 121.7740],
            regions: {
            }
        },
        'Финляндия': {
            coords: [61.9241, 25.7482],
            regions: {
            }
        },
        'Франция': {
            coords: [46.2276, 2.2137],
            regions: {
            }
        },
        'Хорватия': {
            coords: [45.1000, 15.2000],
            regions: {
            }
        },
        'ЦАР': {
            coords: [6.6111, 20.9394],
            regions: {
            }
        },
        'Чад': {
            coords: [15.4542, 18.7322],
            regions: {
            }
        },
        'Черногория': {
            coords: [42.7087, 19.3744],
            regions: {
            }
        },
        'Чехия': {
            coords: [49.8175, 15.4730],
            regions: {
            }
        },
        'Чили': {
            coords: [-35.6751, -71.5430],
            regions: {
            }
        },
        'Швейцария': {
            coords: [46.8182, 8.2275],
            regions: {
            }
        },
        'Швеция': {
            coords: [60.1282, 18.6435],
            regions: {
            }
        },
        'Шри-Ланка': {
            coords: [7.8731, 80.7718],
            regions: {
            }
        },
        'Эквадор': {
            coords: [-1.8312, -78.1834],
            regions: {
            }
        },
        'Экваториальная Гвинея': {
            coords: [1.6508, 10.2679],
            regions: {
            }
        },
        'Эритрея': {
            coords: [15.1794, 39.7823],
            regions: {
            }
        },
        'Эсватини': {
            coords: [-26.5225, 31.4659],
            regions: {
            }
        },
        'Эстония': {
            coords: [58.5953, 25.0136],
            regions: {
            }
        },
        'Эфиопия': {
            coords: [9.1450, 38.7667],
            regions: {
            }
        },
        'ЮАР': {
            coords: [-30.5595, 22.9375],
            regions: {
            }
        },
        'Южная Корея': {
            coords: [35.9078, 127.7669],
            regions: {
            }
        },
        'Южный Судан': {
            coords: [6.8770, 31.3070],
            regions: {
            }
        },
        'Ямайка': {
            coords: [18.1096, -77.2975],
            regions: {
            }
        },
        'Япония': {
            coords: [36.2048, 138.2529],
            regions: {
            }
        },
    },
    'en': {
        'Afghanistan': {
            coords: [33.9391, 67.7100],
            regions: {
            }
        },
        'Albania': {
            coords: [41.1533, 20.1683],
            regions: {
            }
        },
        'Algeria': {
            coords: [28.0339, 1.6596],
            regions: {
            }
        },
        'Andorra': {
            coords: [42.5462, 1.6016],
            regions: {
            }
        },
        'Angola': {
            coords: [-11.2027, 17.8739],
            regions: {
            }
        },
        'Antigua and Barbuda': {
            coords: [17.0608, -61.7964],
            regions: {
            }
        },
        'Argentina': {
            coords: [-38.4161, -63.6167],
            regions: {
            }
        },
        'Armenia': {
            coords: [40.0691, 45.0382],
            regions: {
            }
        },
        'Australia': {
            coords: [-25.2744, 133.7751],
            regions: {
            }
        },
        'Austria': {
            coords: [47.5162, 14.5501],
            regions: {
            }
        },
        'Azerbaijan': {
            coords: [40.1431, 47.5769],
            regions: {
            }
        },
        'Bahamas': {
            coords: [25.0343, -77.3963],
            regions: {
            }
        },
        'Bahrain': {
            coords: [26.0667, 50.5577],
            regions: {
            }
        },
        'Bangladesh': {
            coords: [23.6850, 90.3563],
            regions: {
            }
        },
        'Barbados': {
            coords: [13.1939, -59.5432],
            regions: {
            }
        },
        'Belarus': {
            coords: [53.7098, 27.9534],
            regions: {
            }
        },
        'Belgium': {
            coords: [50.5039, 4.4699],
            regions: {
            }
        },
        'Belize': {
            coords: [17.1899, -88.4976],
            regions: {
            }
        },
        'Benin': {
            coords: [9.3077, 2.3158],
            regions: {
            }
        },
        'Bhutan': {
            coords: [27.5142, 90.4336],
            regions: {
            }
        },
        'Bolivia': {
            coords: [-16.2902, -63.5887],
            regions: {
            }
        },
        'Bosnia and Herzegovina': {
            coords: [43.9159, 17.6791],
            regions: {
            }
        },
        'Botswana': {
            coords: [-22.3285, 24.6849],
            regions: {
            }
        },
        'Brazil': {
            coords: [-14.2350, -51.9253],
            regions: {
            }
        },
        'Brunei': {
            coords: [4.5353, 114.7277],
            regions: {
            }
        },
        'Bulgaria': {
            coords: [42.7339, 25.4858],
            regions: {
            }
        },
        'Burkina Faso': {
            coords: [12.2383, -1.5616],
            regions: {
            }
        },
        'Burundi': {
            coords: [-3.3731, 29.9189],
            regions: {
            }
        },
        'Cambodia': {
            coords: [12.5657, 104.9910],
            regions: {
            }
        },
        'Cameroon': {
            coords: [7.3697, 12.3547],
            regions: {
            }
        },
        'Canada': {
            coords: [56.1304, -106.3468],
            regions: {
            }
        },
        'Cape Verde': {
            coords: [16.5388, -24.0132],
            regions: {
            }
        },
        'Central African Republic': {
            coords: [6.6111, 20.9394],
            regions: {
            }
        },
        'Chad': {
            coords: [15.4542, 18.7322],
            regions: {
            }
        },
        'Chile': {
            coords: [-35.6751, -71.5430],
            regions: {
            }
        },
        'China': {
            coords: [35.8617, 104.1954],
            regions: {
            }
        },
        'Colombia': {
            coords: [4.5709, -74.2973],
            regions: {
            }
        },
        'Comoros': {
            coords: [-11.6455, 43.3333],
            regions: {
            }
        },
        'Congo': {
            coords: [-0.2280, 15.8277],
            regions: {
            }
        },
        'Costa Rica': {
            coords: [9.7489, -83.7534],
            regions: {
            }
        },
        'Croatia': {
            coords: [45.1000, 15.2000],
            regions: {
            }
        },
        'Cuba': {
            coords: [21.5218, -77.7812],
            regions: {
            }
        },
        'Cyprus': {
            coords: [35.1264, 33.4299],
            regions: {
            }
        },
        'Czech Republic': {
            coords: [49.8175, 15.4730],
            regions: {
            }
        },
        'DR Congo': {
            coords: [-4.0383, 21.7587],
            regions: {
            }
        },
        'Denmark': {
            coords: [56.2639, 9.5018],
            regions: {
            }
        },
        'Djibouti': {
            coords: [11.8251, 42.5903],
            regions: {
            }
        },
        'Dominica': {
            coords: [15.4150, -61.3710],
            regions: {
            }
        },
        'Dominican Republic': {
            coords: [18.7357, -70.1627],
            regions: {
            }
        },
        'East Timor': {
            coords: [-8.8742, 125.7275],
            regions: {
            }
        },
        'Ecuador': {
            coords: [-1.8312, -78.1834],
            regions: {
            }
        },
        'Egypt': {
            coords: [26.8206, 30.8025],
            regions: {
            }
        },
        'El Salvador': {
            coords: [13.7942, -88.8965],
            regions: {
            }
        },
        'Equatorial Guinea': {
            coords: [1.6508, 10.2679],
            regions: {
            }
        },
        'Eritrea': {
            coords: [15.1794, 39.7823],
            regions: {
            }
        },
        'Estonia': {
            coords: [58.5953, 25.0136],
            regions: {
            }
        },
        'Eswatini': {
            coords: [-26.5225, 31.4659],
            regions: {
            }
        },
        'Ethiopia': {
            coords: [9.1450, 38.7667],
            regions: {
            }
        },
        'Fiji': {
            coords: [-16.7784, 178.0650],
            regions: {
            }
        },
        'Finland': {
            coords: [61.9241, 25.7482],
            regions: {
            }
        },
        'France': {
            coords: [46.2276, 2.2137],
            regions: {
            }
        },
        'Gabon': {
            coords: [-0.8037, 11.6094],
            regions: {
            }
        },
        'Gambia': {
            coords: [13.4432, -15.3101],
            regions: {
            }
        },
        'Georgia': {
            coords: [42.3154, 43.3569],
            regions: {
            }
        },
        'Germany': {
            coords: [51.1657, 10.4515],
            regions: {
            }
        },
        'Ghana': {
            coords: [7.9465, -1.0232],
            regions: {
            }
        },
        'Greece': {
            coords: [39.0742, 21.8243],
            regions: {
            }
        },
        'Grenada': {
            coords: [12.1165, -61.6790],
            regions: {
            }
        },
        'Guatemala': {
            coords: [15.7835, -90.2308],
            regions: {
            }
        },
        'Guinea': {
            coords: [9.9456, -9.6966],
            regions: {
            }
        },
        'Guinea-Bissau': {
            coords: [11.8037, -15.1804],
            regions: {
            }
        },
        'Guyana': {
            coords: [4.8604, -58.9302],
            regions: {
            }
        },
        'Haiti': {
            coords: [18.9712, -72.2852],
            regions: {
            }
        },
        'Honduras': {
            coords: [15.2000, -86.2419],
            regions: {
            }
        },
        'Hungary': {
            coords: [47.1625, 19.5033],
            regions: {
            }
        },
        'Iceland': {
            coords: [64.9631, -19.0208],
            regions: {
            }
        },
        'India': {
            coords: [20.5937, 78.9629],
            regions: {
            }
        },
        'Indonesia': {
            coords: [-0.7893, 113.9213],
            regions: {
                'Jakarta': { humidity: 80, coords: [-6.2088, 106.8456], waterPriceUsd1L: 0.36 },
                'West Java': { humidity: 78, coords: [-6.9175, 107.6191], waterPriceUsd1L: 0.30 },
                'Central Java': { humidity: 78, coords: [-7.1510, 110.1403], waterPriceUsd1L: 0.27 },
                'East Java': { humidity: 76, coords: [-7.5361, 112.2384], waterPriceUsd1L: 0.30 },
                'Banten': { humidity: 80, coords: [-6.4058, 106.0640], waterPriceUsd1L: 0.33 },
                'Yogyakarta': { humidity: 78, coords: [-7.7956, 110.3695], waterPriceUsd1L: 0.27 },
                'Bali': { humidity: 78, coords: [-8.4095, 115.1889], waterPriceUsd1L: 0.42 },
                'West Nusa Tenggara': { humidity: 75, coords: [-8.6529, 117.3616], waterPriceUsd1L: 0.33 },
                'East Nusa Tenggara': { humidity: 70, coords: [-8.6574, 121.0794], waterPriceUsd1L: 0.36 },
                'West Kalimantan': { humidity: 85, coords: [-0.2787, 111.4752], waterPriceUsd1L: 0.33 },
                'Central Kalimantan': { humidity: 85, coords: [-1.6815, 113.3824], waterPriceUsd1L: 0.36 },
                'South Kalimantan': { humidity: 82, coords: [-3.0926, 115.2838], waterPriceUsd1L: 0.33 },
                'East Kalimantan': { humidity: 82, coords: [0.5387, 116.4194], waterPriceUsd1L: 0.36 },
                'North Kalimantan': { humidity: 85, coords: [3.0731, 116.0414], waterPriceUsd1L: 0.39 },
                'North Sulawesi': { humidity: 82, coords: [0.6247, 123.9750], waterPriceUsd1L: 0.36 },
                'Central Sulawesi': { humidity: 80, coords: [-1.4300, 121.4456], waterPriceUsd1L: 0.33 },
                'South Sulawesi': { humidity: 80, coords: [-3.6688, 119.9741], waterPriceUsd1L: 0.30 },
                'Southeast Sulawesi': { humidity: 82, coords: [-4.1449, 122.1746], waterPriceUsd1L: 0.33 },
                'Gorontalo': { humidity: 80, coords: [0.6999, 122.4467], waterPriceUsd1L: 0.33 },
                'West Sulawesi': { humidity: 82, coords: [-2.8441, 119.2321], waterPriceUsd1L: 0.33 },
                'Maluku': { humidity: 85, coords: [-3.2385, 130.1453], waterPriceUsd1L: 0.39 },
                'North Maluku': { humidity: 85, coords: [1.5709, 127.8088], waterPriceUsd1L: 0.42 },
                'Papua': { humidity: 85, coords: [-4.2699, 138.0804], waterPriceUsd1L: 0.45 },
                'West Papua': { humidity: 85, coords: [-1.3361, 133.1747], waterPriceUsd1L: 0.45 },
                'Aceh': { humidity: 82, coords: [4.6951, 96.7494], waterPriceUsd1L: 0.30 },
                'North Sumatra': { humidity: 82, coords: [2.1154, 99.5451], waterPriceUsd1L: 0.30 },
                'West Sumatra': { humidity: 82, coords: [-0.7399, 100.8000], waterPriceUsd1L: 0.30 },
                'Riau': { humidity: 85, coords: [0.2933, 101.7068], waterPriceUsd1L: 0.33 },
                'Riau Islands': { humidity: 85, coords: [3.9457, 108.1429], waterPriceUsd1L: 0.36 },
                'Jambi': { humidity: 82, coords: [-1.4852, 102.4381], waterPriceUsd1L: 0.30 },
                'South Sumatra': { humidity: 82, coords: [-3.3194, 104.9147], waterPriceUsd1L: 0.30 },
                'Bangka Belitung Islands': { humidity: 85, coords: [-2.7411, 106.4406], waterPriceUsd1L: 0.36 },
                'Bengkulu': { humidity: 82, coords: [-3.5778, 102.3464], waterPriceUsd1L: 0.30 },
                'Lampung': { humidity: 80, coords: [-4.5586, 105.4068], waterPriceUsd1L: 0.30 },
            }
        },
        'Iraq': {
            coords: [33.2232, 43.6793],
            regions: {
            }
        },
        'Ireland': {
            coords: [53.4129, -8.2439],
            regions: {
            }
        },
        'Israel': {
            coords: [31.0461, 34.8516],
            regions: {
            }
        },
        'Italy': {
            coords: [41.8719, 12.5674],
            regions: {
            }
        },
        'Jamaica': {
            coords: [18.1096, -77.2975],
            regions: {
            }
        },
        'Japan': {
            coords: [36.2048, 138.2529],
            regions: {
            }
        },
        'Jordan': {
            coords: [30.5852, 36.2384],
            regions: {
            }
        },
        'Kazakhstan': {
            coords: [48.0196, 66.9237],
            regions: {
            }
        },
        'Kenya': {
            coords: [-0.0236, 37.9062],
            regions: {
            }
        },
        'Kiribati': {
            coords: [-3.3704, -168.7340],
            regions: {
            }
        },
        'Kuwait': {
            coords: [29.3117, 47.4818],
            regions: {
            }
        },
        'Kyrgyzstan': {
            coords: [41.2044, 74.7661],
            regions: {
            }
        },
        'Laos': {
            coords: [19.8563, 102.4955],
            regions: {
            }
        },
        'Latvia': {
            coords: [56.8796, 24.6032],
            regions: {
            }
        },
        'Lebanon': {
            coords: [33.8547, 35.8623],
            regions: {
            }
        },
        'Lesotho': {
            coords: [-29.6100, 28.2336],
            regions: {
            }
        },
        'Liberia': {
            coords: [6.4281, -9.4295],
            regions: {
            }
        },
        'Libya': {
            coords: [26.3351, 17.2283],
            regions: {
            }
        },
        'Liechtenstein': {
            coords: [47.1660, 9.5554],
            regions: {
            }
        },
        'Lithuania': {
            coords: [55.1694, 23.8813],
            regions: {
            }
        },
        'Luxembourg': {
            coords: [49.8153, 6.1296],
            regions: {
            }
        },
        'Madagascar': {
            coords: [-18.7669, 46.8691],
            regions: {
            }
        },
        'Malawi': {
            coords: [-13.2543, 34.3015],
            regions: {
            }
        },
        'Malaysia': {
            coords: [4.2105, 101.9758],
            regions: {
            }
        },
        'Maldives': {
            coords: [3.2028, 73.2207],
            regions: {
            }
        },
        'Mali': {
            coords: [17.5707, -3.9962],
            regions: {
            }
        },
        'Malta': {
            coords: [35.9375, 14.3754],
            regions: {
            }
        },
        'Marshall Islands': {
            coords: [7.1315, 171.1845],
            regions: {
            }
        },
        'Mauritania': {
            coords: [21.0079, -10.9408],
            regions: {
            }
        },
        'Mauritius': {
            coords: [-20.3484, 57.5522],
            regions: {
            }
        },
        'Mexico': {
            coords: [23.6345, -102.5528],
            regions: {
            }
        },
        'Micronesia': {
            coords: [7.4256, 150.5508],
            regions: {
            }
        },
        'Moldova': {
            coords: [47.4116, 28.3699],
            regions: {
            }
        },
        'Monaco': {
            coords: [43.7384, 7.4246],
            regions: {
            }
        },
        'Mongolia': {
            coords: [46.8625, 103.8467],
            regions: {
            }
        },
        'Montenegro': {
            coords: [42.7087, 19.3744],
            regions: {
            }
        },
        'Morocco': {
            coords: [31.7917, -7.0926],
            regions: {
            }
        },
        'Mozambique': {
            coords: [-18.6657, 35.5296],
            regions: {
            }
        },
        'Myanmar': {
            coords: [21.9162, 95.9560],
            regions: {
            }
        },
        'Namibia': {
            coords: [-22.9576, 18.4904],
            regions: {
            }
        },
        'Nauru': {
            coords: [-0.5228, 166.9315],
            regions: {
            }
        },
        'Nepal': {
            coords: [28.3949, 84.1240],
            regions: {
            }
        },
        'Netherlands': {
            coords: [52.1326, 5.2913],
            regions: {
            }
        },
        'New Zealand': {
            coords: [-40.9006, 174.8860],
            regions: {
            }
        },
        'Nicaragua': {
            coords: [12.2650, -85.2072],
            regions: {
            }
        },
        'Niger': {
            coords: [17.6078, 8.0817],
            regions: {
            }
        },
        'Nigeria': {
            coords: [9.0820, 8.6753],
            regions: {
            }
        },
        'North Korea': {
            coords: [40.3399, 127.5101],
            regions: {
            }
        },
        'North Macedonia': {
            coords: [41.6086, 21.7453],
            regions: {
            }
        },
        'Norway': {
            coords: [60.4720, 8.4689],
            regions: {
            }
        },
        'Oman': {
            coords: [21.4735, 55.9754],
            regions: {
            }
        },
        'Pakistan': {
            coords: [30.3753, 69.3451],
            regions: {
            }
        },
        'Palau': {
            coords: [7.5150, 134.5825],
            regions: {
            }
        },
        'Panama': {
            coords: [8.5380, -80.7821],
            regions: {
            }
        },
        'Papua New Guinea': {
            coords: [-6.3150, 143.9555],
            regions: {
            }
        },
        'Paraguay': {
            coords: [-23.4425, -58.4438],
            regions: {
            }
        },
        'Peru': {
            coords: [-9.1900, -75.0152],
            regions: {
            }
        },
        'Philippines': {
            coords: [12.8797, 121.7740],
            regions: {
            }
        },
        'Poland': {
            coords: [51.9194, 19.1451],
            regions: {
            }
        },
        'Portugal': {
            coords: [39.3999, -8.2245],
            regions: {
            }
        },
        'Qatar': {
            coords: [25.3548, 51.1839],
            regions: {
            }
        },
        'Romania': {
            coords: [45.9432, 24.9668],
            regions: {
            }
        },
        'Russia': {
            coords: [61.5240, 105.3188],
            regions: {
                'Moscow': { humidity: 70, coords: [55.7558, 37.6173], waterPriceUsd1L: 0.77 },
                'Moscow Oblast': { humidity: 70, coords: [55.5, 37.0], waterPriceUsd1L: 0.71 },
                'Saint Petersburg': { humidity: 78, coords: [59.9311, 30.3609], waterPriceUsd1L: 0.71 },
                'Leningrad Oblast': { humidity: 78, coords: [59.5, 31.0], waterPriceUsd1L: 0.64 },
                'Sevastopol': { humidity: 72, coords: [44.6167, 33.5254], waterPriceUsd1L: 0.64 },
                'Republic of Crimea': { humidity: 72, coords: [45.0, 34.0], waterPriceUsd1L: 0.64 },
                'Republic of Adygea': { humidity: 72, coords: [44.82, 40.18], waterPriceUsd1L: 0.58 },
                'Altai Republic': { humidity: 60, coords: [50.71, 86.86], waterPriceUsd1L: 0.51 },
                'Republic of Bashkortostan': { humidity: 67, coords: [54.74, 55.96], waterPriceUsd1L: 0.51 },
                'Republic of Buryatia': { humidity: 58, coords: [51.83, 107.58], waterPriceUsd1L: 0.51 },
                'Republic of Dagestan': { humidity: 66, coords: [42.26, 47.10], waterPriceUsd1L: 0.51 },
                'Republic of Ingushetia': { humidity: 66, coords: [43.17, 44.81], waterPriceUsd1L: 0.51 },
                'Kabardino-Balkarian Republic': { humidity: 66, coords: [43.39, 43.56], waterPriceUsd1L: 0.51 },
                'Republic of Kalmykia': { humidity: 55, coords: [46.23, 45.33], waterPriceUsd1L: 0.51 },
                'Karachay-Cherkess Republic': { humidity: 66, coords: [43.74, 41.73], waterPriceUsd1L: 0.51 },
                'Republic of Karelia': { humidity: 78, coords: [63.56, 33.36], waterPriceUsd1L: 0.58 },
                'Komi Republic': { humidity: 78, coords: [64.0, 54.0], waterPriceUsd1L: 0.58 },
                'Mari El Republic': { humidity: 72, coords: [56.63, 47.87], waterPriceUsd1L: 0.51 },
                'Republic of Mordovia': { humidity: 70, coords: [54.18, 45.17], waterPriceUsd1L: 0.51 },
                'Sakha Republic (Yakutia)': { humidity: 60, coords: [66.76, 124.12], waterPriceUsd1L: 0.77 },
                'Republic of North Ossetia–Alania': { humidity: 66, coords: [43.02, 44.68], waterPriceUsd1L: 0.51 },
                'Republic of Tatarstan': { humidity: 70, coords: [55.80, 49.11], waterPriceUsd1L: 0.58 },
                'Tuva Republic': { humidity: 55, coords: [51.72, 94.44], waterPriceUsd1L: 0.51 },
                'Udmurt Republic': { humidity: 72, coords: [57.0, 53.0], waterPriceUsd1L: 0.51 },
                'Republic of Khakassia': { humidity: 55, coords: [53.72, 91.44], waterPriceUsd1L: 0.51 },
                'Chechen Republic': { humidity: 66, coords: [43.40, 45.70], waterPriceUsd1L: 0.51 },
                'Chuvash Republic': { humidity: 70, coords: [55.5, 47.0], waterPriceUsd1L: 0.51 },
                'Altai Krai': { humidity: 60, coords: [52.69, 82.69], waterPriceUsd1L: 0.51 },
                'Krasnodar Krai': { humidity: 75, coords: [45.0355, 38.9753], waterPriceUsd1L: 0.64 },
                'Krasnoyarsk Krai': { humidity: 60, coords: [64.25, 95.10], waterPriceUsd1L: 0.58 },
                'Primorsky Krai': { humidity: 78, coords: [43.1155, 131.8855], waterPriceUsd1L: 0.64 },
                'Stavropol Krai': { humidity: 68, coords: [44.67, 43.52], waterPriceUsd1L: 0.58 },
                'Khabarovsk Krai': { humidity: 75, coords: [50.59, 135.0], waterPriceUsd1L: 0.64 },
                'Amur Oblast': { humidity: 65, coords: [52.8, 128.0], waterPriceUsd1L: 0.58 },
                'Arkhangelsk Oblast': { humidity: 78, coords: [63.0, 41.0], waterPriceUsd1L: 0.58 },
                'Astrakhan Oblast': { humidity: 55, coords: [46.35, 48.04], waterPriceUsd1L: 0.51 },
                'Belgorod Oblast': { humidity: 68, coords: [50.60, 36.60], waterPriceUsd1L: 0.51 },
                'Bryansk Oblast': { humidity: 75, coords: [53.26, 34.37], waterPriceUsd1L: 0.51 },
                'Vladimir Oblast': { humidity: 72, coords: [55.9, 40.4], waterPriceUsd1L: 0.58 },
                'Volgograd Oblast': { humidity: 60, coords: [49.6, 44.4], waterPriceUsd1L: 0.51 },
                'Vologda Oblast': { humidity: 78, coords: [59.22, 39.88], waterPriceUsd1L: 0.58 },
                'Voronezh Oblast': { humidity: 65, coords: [51.67, 39.18], waterPriceUsd1L: 0.51 },
                'Ivanovo Oblast': { humidity: 75, coords: [57.0, 41.0], waterPriceUsd1L: 0.51 },
                'Irkutsk Oblast': { humidity: 60, coords: [56.0, 105.0], waterPriceUsd1L: 0.58 },
                'Kaliningrad Oblast': { humidity: 80, coords: [54.7104, 20.4522], waterPriceUsd1L: 0.64 },
                'Kaluga Oblast': { humidity: 72, coords: [54.5, 35.5], waterPriceUsd1L: 0.58 },
                'Kamchatka Krai': { humidity: 80, coords: [56.0, 159.0], waterPriceUsd1L: 0.90 },
                'Kemerovo Oblast': { humidity: 65, coords: [54.75, 87.14], waterPriceUsd1L: 0.51 },
                'Kirov Oblast': { humidity: 72, coords: [58.5, 50.0], waterPriceUsd1L: 0.51 },
                'Kostroma Oblast': { humidity: 75, coords: [58.55, 43.95], waterPriceUsd1L: 0.51 },
                'Kurgan Oblast': { humidity: 65, coords: [55.45, 65.34], waterPriceUsd1L: 0.51 },
                'Kursk Oblast': { humidity: 68, coords: [51.74, 36.19], waterPriceUsd1L: 0.51 },
                'Lipetsk Oblast': { humidity: 68, coords: [52.60, 39.57], waterPriceUsd1L: 0.51 },
                'Magadan Oblast': { humidity: 78, coords: [62.0, 153.0], waterPriceUsd1L: 0.90 },
                'Murmansk Oblast': { humidity: 80, coords: [68.96, 33.08], waterPriceUsd1L: 0.64 },
                'Nizhny Novgorod Oblast': { humidity: 70, coords: [56.33, 44.01], waterPriceUsd1L: 0.58 },
                'Novgorod Oblast': { humidity: 78, coords: [58.52, 31.28], waterPriceUsd1L: 0.58 },
                'Novosibirsk Oblast': { humidity: 60, coords: [55.0084, 82.9357], waterPriceUsd1L: 0.58 },
                'Omsk Oblast': { humidity: 60, coords: [54.99, 73.37], waterPriceUsd1L: 0.51 },
                'Orenburg Oblast': { humidity: 60, coords: [51.77, 55.10], waterPriceUsd1L: 0.51 },
                'Oryol Oblast': { humidity: 72, coords: [52.97, 36.06], waterPriceUsd1L: 0.51 },
                'Penza Oblast': { humidity: 68, coords: [53.19, 45.02], waterPriceUsd1L: 0.51 },
                'Perm Krai': { humidity: 72, coords: [58.0, 56.32], waterPriceUsd1L: 0.58 },
                'Pskov Oblast': { humidity: 78, coords: [57.82, 28.33], waterPriceUsd1L: 0.58 },
                'Rostov Oblast': { humidity: 60, coords: [47.2357, 39.7015], waterPriceUsd1L: 0.58 },
                'Ryazan Oblast': { humidity: 72, coords: [54.63, 39.69], waterPriceUsd1L: 0.51 },
                'Samara Oblast': { humidity: 65, coords: [53.20, 50.16], waterPriceUsd1L: 0.58 },
                'Saratov Oblast': { humidity: 60, coords: [51.53, 46.03], waterPriceUsd1L: 0.51 },
                'Sakhalin Oblast': { humidity: 85, coords: [50.69, 142.95], waterPriceUsd1L: 0.77 },
                'Sverdlovsk Oblast': { humidity: 65, coords: [56.8389, 60.6057], waterPriceUsd1L: 0.58 },
                'Smolensk Oblast': { humidity: 75, coords: [54.78, 32.05], waterPriceUsd1L: 0.51 },
                'Tambov Oblast': { humidity: 65, coords: [52.72, 41.45], waterPriceUsd1L: 0.51 },
                'Tver Oblast': { humidity: 75, coords: [56.86, 35.92], waterPriceUsd1L: 0.58 },
                'Tomsk Oblast': { humidity: 70, coords: [58.60, 70.0], waterPriceUsd1L: 0.58 },
                'Tula Oblast': { humidity: 70, coords: [54.19, 37.62], waterPriceUsd1L: 0.58 },
                'Tyumen Oblast': { humidity: 70, coords: [57.16, 68.43], waterPriceUsd1L: 0.58 },
                'Ulyanovsk Oblast': { humidity: 65, coords: [54.32, 48.40], waterPriceUsd1L: 0.51 },
                'Chelyabinsk Oblast': { humidity: 65, coords: [55.16, 61.40], waterPriceUsd1L: 0.58 },
                'Zabaykalsky Krai': { humidity: 55, coords: [52.0, 115.0], waterPriceUsd1L: 0.58 },
                'Yaroslavl Oblast': { humidity: 75, coords: [57.63, 39.88], waterPriceUsd1L: 0.58 },
                'Jewish Autonomous Oblast': { humidity: 70, coords: [48.8, 132.95], waterPriceUsd1L: 0.58 },
                'Nenets Autonomous Okrug': { humidity: 80, coords: [68.0, 53.0], waterPriceUsd1L: 0.77 },
                'Khanty-Mansi Autonomous Okrug': { humidity: 75, coords: [61.0, 69.0], waterPriceUsd1L: 0.64 },
                'Chukotka Autonomous Okrug': { humidity: 78, coords: [66.0, 169.0], waterPriceUsd1L: 1.03 },
                'Yamalo-Nenets Autonomous Okrug': { humidity: 78, coords: [66.5, 70.0], waterPriceUsd1L: 0.77 },
            }
        },
        'Rwanda': {
            coords: [-1.9403, 29.8739],
            regions: {
            }
        },
        'Saint Kitts and Nevis': {
            coords: [17.3578, -62.7830],
            regions: {
            }
        },
        'Saint Lucia': {
            coords: [13.9094, -60.9789],
            regions: {
            }
        },
        'Saint Vincent and the Grenadines': {
            coords: [12.9843, -61.2872],
            regions: {
            }
        },
        'Samoa': {
            coords: [-13.7590, -172.1046],
            regions: {
            }
        },
        'San Marino': {
            coords: [43.9424, 12.4578],
            regions: {
            }
        },
        'Saudi Arabia': {
            coords: [23.8859, 45.0792],
            regions: {
                'Riyadh': { humidity: 47, coords: [24.7136, 46.6753], waterPriceUsd1L: 0.40 },
                'Mecca': { humidity: 50, coords: [21.3891, 39.8579], waterPriceUsd1L: 0.45 },
                'Medina': { humidity: 40, coords: [24.5247, 39.5692], waterPriceUsd1L: 0.42 },
                'Eastern Province': { humidity: 65, coords: [26.4207, 50.0888], waterPriceUsd1L: 0.38 },
                'Asir': { humidity: 55, coords: [18.2164, 42.5053], waterPriceUsd1L: 0.35 },
                'Jazan': { humidity: 70, coords: [16.8892, 42.5611], waterPriceUsd1L: 0.35 },
                'Najran': { humidity: 35, coords: [17.4933, 44.1277], waterPriceUsd1L: 0.35 },
                'Al Bahah': { humidity: 45, coords: [19.8614, 41.4414], waterPriceUsd1L: 0.35 },
                'Tabuk': { humidity: 35, coords: [28.3838, 36.5550], waterPriceUsd1L: 0.38 },
                'Al Jawf': { humidity: 35, coords: [29.7889, 39.8789], waterPriceUsd1L: 0.35 },
                'Northern Borders': { humidity: 40, coords: [31.1728, 37.9888], waterPriceUsd1L: 0.35 },
                'Hail': { humidity: 35, coords: [27.5219, 41.6906], waterPriceUsd1L: 0.35 },
                'Al Qassim': { humidity: 40, coords: [26.2076, 43.4839], waterPriceUsd1L: 0.35 }
            }
        },
        'Senegal': {
            coords: [14.4974, -14.4524],
            regions: {
            }
        },
        'Serbia': {
            coords: [44.0165, 21.0059],
            regions: {
            }
        },
        'Seychelles': {
            coords: [-4.6796, 55.4920],
            regions: {
            }
        },
        'Sierra Leone': {
            coords: [8.4606, -11.7799],
            regions: {
            }
        },
        'Singapore': {
            coords: [1.3521, 103.8198],
            regions: {
            }
        },
        'Slovakia': {
            coords: [48.6690, 19.6990],
            regions: {
            }
        },
        'Slovenia': {
            coords: [46.1512, 14.9955],
            regions: {
            }
        },
        'Solomon Islands': {
            coords: [-9.6457, 160.1562],
            regions: {
            }
        },
        'Somalia': {
            coords: [5.1521, 46.1996],
            regions: {
            }
        },
        'South Africa': {
            coords: [-30.5595, 22.9375],
            regions: {
            }
        },
        'South Korea': {
            coords: [35.9078, 127.7669],
            regions: {
            }
        },
        'South Sudan': {
            coords: [6.8770, 31.3070],
            regions: {
            }
        },
        'Spain': {
            coords: [40.4637, -3.7492],
            regions: {
            }
        },
        'Sri Lanka': {
            coords: [7.8731, 80.7718],
            regions: {
            }
        },
        'Sudan': {
            coords: [12.8628, 30.2176],
            regions: {
            }
        },
        'Suriname': {
            coords: [3.9193, -56.0278],
            regions: {
            }
        },
        'Sweden': {
            coords: [60.1282, 18.6435],
            regions: {
            }
        },
        'Switzerland': {
            coords: [46.8182, 8.2275],
            regions: {
            }
        },
        'Syria': {
            coords: [34.8021, 38.9968],
            regions: {
            }
        },
        'São Tomé and Príncipe': {
            coords: [0.1864, 6.6131],
            regions: {
            }
        },
        'Tajikistan': {
            coords: [38.8610, 71.2761],
            regions: {
            }
        },
        'Tanzania': {
            coords: [-6.3690, 34.8888],
            regions: {
            }
        },
        'Thailand': {
            coords: [15.8700, 100.9925],
            regions: {
            }
        },
        'Togo': {
            coords: [8.6195, 0.8248],
            regions: {
            }
        },
        'Tonga': {
            coords: [-21.1789, -175.1982],
            regions: {
            }
        },
        'Trinidad and Tobago': {
            coords: [10.6918, -61.2225],
            regions: {
            }
        },
        'Tunisia': {
            coords: [33.8869, 9.5375],
            regions: {
            }
        },
        'Turkey': {
            coords: [38.9637, 35.2433],
            regions: {
            }
        },
        'Turkmenistan': {
            coords: [38.9697, 59.5563],
            regions: {
            }
        },
        'Tuvalu': {
            coords: [-7.1095, 177.6493],
            regions: {
            }
        },
        'Uganda': {
            coords: [1.3733, 32.2903],
            regions: {
            }
        },
        'Ukraine': {
            coords: [48.3794, 31.1656],
            regions: {
            }
        },
        'United Arab Emirates': {
            coords: [23.4241, 53.8478],
            regions: {
                'Abu Dhabi': { humidity: 60, coords: [24.4539, 54.3773], waterPriceUsd1L: 0.35 },
                'Dubai': { humidity: 55, coords: [25.2048, 55.2708], waterPriceUsd1L: 0.40 },
                'Sharjah': { humidity: 55, coords: [25.3463, 55.4209], waterPriceUsd1L: 0.32 },
                'Ajman': { humidity: 55, coords: [25.4052, 55.5136], waterPriceUsd1L: 0.30 },
                'Umm Al Quwain': { humidity: 50, coords: [25.5647, 55.5552], waterPriceUsd1L: 0.30 },
                'Ras Al Khaimah': { humidity: 55, coords: [25.7895, 55.9432], waterPriceUsd1L: 0.30 },
                'Fujairah': { humidity: 65, coords: [25.1288, 56.3264], waterPriceUsd1L: 0.32 }
            }
        },
        'United Kingdom': {
            coords: [55.3781, -3.4360],
            regions: {
            }
        },
        'United States': {
            coords: [37.0902, -95.7129],
            regions: {
            }
        },
        'Uruguay': {
            coords: [-32.5228, -55.7658],
            regions: {
            }
        },
        'Uzbekistan': {
            coords: [41.3775, 64.5853],
            regions: {
            }
        },
        'Vanuatu': {
            coords: [-15.3767, 166.9592],
            regions: {
            }
        },
        'Vatican': {
            coords: [41.9029, 12.4534],
            regions: {
            }
        },
        'Venezuela': {
            coords: [6.4238, -66.5897],
            regions: {
            }
        },
        'Vietnam': {
            coords: [14.0583, 108.2772],
            regions: {
            }
        },
        'Yemen': {
            coords: [15.5527, 48.5164],
            regions: {
            }
        },
        'Zambia': {
            coords: [-13.1339, 27.8493],
            regions: {
            }
        },
        'Zimbabwe': {
            coords: [-19.0154, 29.1549],
            regions: {
            }
        },
    },
    'zh': {
        '不丹': {
            coords: [27.5142, 90.4336],
            regions: {
            }
        },
        '东帝汶': {
            coords: [-8.8742, 125.7275],
            regions: {
            }
        },
        '中国': {
            coords: [35.8617, 104.1954],
            regions: {
            }
        },
        '中非': {
            coords: [6.6111, 20.9394],
            regions: {
            }
        },
        '丹麦': {
            coords: [56.2639, 9.5018],
            regions: {
            }
        },
        '乌克兰': {
            coords: [48.3794, 31.1656],
            regions: {
            }
        },
        '乌兹别克斯坦': {
            coords: [41.3775, 64.5853],
            regions: {
            }
        },
        '乌干达': {
            coords: [1.3733, 32.2903],
            regions: {
            }
        },
        '乌拉圭': {
            coords: [-32.5228, -55.7658],
            regions: {
            }
        },
        '乍得': {
            coords: [15.4542, 18.7322],
            regions: {
            }
        },
        '也门': {
            coords: [15.5527, 48.5164],
            regions: {
            }
        },
        '亚美尼亚': {
            coords: [40.0691, 45.0382],
            regions: {
            }
        },
        '以色列': {
            coords: [31.0461, 34.8516],
            regions: {
            }
        },
        '伊拉克': {
            coords: [33.2232, 43.6793],
            regions: {
            }
        },
        '伯利兹': {
            coords: [17.1899, -88.4976],
            regions: {
            }
        },
        '佛得角': {
            coords: [16.5388, -24.0132],
            regions: {
            }
        },
        '俄罗斯': {
            coords: [61.5240, 105.3188],
            regions: {
                '莫斯科': { humidity: 70, coords: [55.7558, 37.6173], waterPriceUsd1L: 0.77 },
                '莫斯科州': { humidity: 70, coords: [55.5, 37.0], waterPriceUsd1L: 0.71 },
                '圣彼得堡': { humidity: 78, coords: [59.9311, 30.3609], waterPriceUsd1L: 0.71 },
                '列宁格勒州': { humidity: 78, coords: [59.5, 31.0], waterPriceUsd1L: 0.64 },
                '塞瓦斯托波尔': { humidity: 72, coords: [44.6167, 33.5254], waterPriceUsd1L: 0.64 },
                '克里米亚共和国': { humidity: 72, coords: [45.0, 34.0], waterPriceUsd1L: 0.64 },
                '阿迪格共和国': { humidity: 72, coords: [44.82, 40.18], waterPriceUsd1L: 0.58 },
                '阿尔泰共和国': { humidity: 60, coords: [50.71, 86.86], waterPriceUsd1L: 0.51 },
                '巴什科尔托斯坦共和国': { humidity: 67, coords: [54.74, 55.96], waterPriceUsd1L: 0.51 },
                '布里亚特共和国': { humidity: 58, coords: [51.83, 107.58], waterPriceUsd1L: 0.51 },
                '达吉斯坦共和国': { humidity: 66, coords: [42.26, 47.10], waterPriceUsd1L: 0.51 },
                '印古什共和国': { humidity: 66, coords: [43.17, 44.81], waterPriceUsd1L: 0.51 },
                '卡巴尔达-巴尔卡尔共和国': { humidity: 66, coords: [43.39, 43.56], waterPriceUsd1L: 0.51 },
                '卡尔梅克共和国': { humidity: 55, coords: [46.23, 45.33], waterPriceUsd1L: 0.51 },
                '卡拉恰伊-切尔克斯共和国': { humidity: 66, coords: [43.74, 41.73], waterPriceUsd1L: 0.51 },
                '卡累利阿共和国': { humidity: 78, coords: [63.56, 33.36], waterPriceUsd1L: 0.58 },
                '科米共和国': { humidity: 78, coords: [64.0, 54.0], waterPriceUsd1L: 0.58 },
                '马里埃尔共和国': { humidity: 72, coords: [56.63, 47.87], waterPriceUsd1L: 0.51 },
                '莫尔多瓦共和国': { humidity: 70, coords: [54.18, 45.17], waterPriceUsd1L: 0.51 },
                '萨哈共和国': { humidity: 60, coords: [66.76, 124.12], waterPriceUsd1L: 0.77 },
                '北奥塞梯-阿兰共和国': { humidity: 66, coords: [43.02, 44.68], waterPriceUsd1L: 0.51 },
                '鞑靼斯坦共和国': { humidity: 70, coords: [55.80, 49.11], waterPriceUsd1L: 0.58 },
                '图瓦共和国': { humidity: 55, coords: [51.72, 94.44], waterPriceUsd1L: 0.51 },
                '乌德穆尔特共和国': { humidity: 72, coords: [57.0, 53.0], waterPriceUsd1L: 0.51 },
                '哈卡斯共和国': { humidity: 55, coords: [53.72, 91.44], waterPriceUsd1L: 0.51 },
                '车臣共和国': { humidity: 66, coords: [43.40, 45.70], waterPriceUsd1L: 0.51 },
                '楚瓦什共和国': { humidity: 70, coords: [55.5, 47.0], waterPriceUsd1L: 0.51 },
                '阿尔泰边疆区': { humidity: 60, coords: [52.69, 82.69], waterPriceUsd1L: 0.51 },
                '克拉斯诺达尔边疆区': { humidity: 75, coords: [45.0355, 38.9753], waterPriceUsd1L: 0.64 },
                '克拉斯诺亚尔斯克边疆区': { humidity: 60, coords: [64.25, 95.10], waterPriceUsd1L: 0.58 },
                '滨海边疆区': { humidity: 78, coords: [43.1155, 131.8855], waterPriceUsd1L: 0.64 },
                '斯塔夫罗波尔边疆区': { humidity: 68, coords: [44.67, 43.52], waterPriceUsd1L: 0.58 },
                '哈巴罗夫斯克边疆区': { humidity: 75, coords: [50.59, 135.0], waterPriceUsd1L: 0.64 },
                '阿穆尔州': { humidity: 65, coords: [52.8, 128.0], waterPriceUsd1L: 0.58 },
                '阿尔汉格尔斯克州': { humidity: 78, coords: [63.0, 41.0], waterPriceUsd1L: 0.58 },
                '阿斯特拉罕州': { humidity: 55, coords: [46.35, 48.04], waterPriceUsd1L: 0.51 },
                '别尔哥罗德州': { humidity: 68, coords: [50.60, 36.60], waterPriceUsd1L: 0.51 },
                '布良斯克州': { humidity: 75, coords: [53.26, 34.37], waterPriceUsd1L: 0.51 },
                '弗拉基米尔州': { humidity: 72, coords: [55.9, 40.4], waterPriceUsd1L: 0.58 },
                '伏尔加格勒州': { humidity: 60, coords: [49.6, 44.4], waterPriceUsd1L: 0.51 },
                '沃洛格达州': { humidity: 78, coords: [59.22, 39.88], waterPriceUsd1L: 0.58 },
                '沃罗涅日州': { humidity: 65, coords: [51.67, 39.18], waterPriceUsd1L: 0.51 },
                '伊万诺沃州': { humidity: 75, coords: [57.0, 41.0], waterPriceUsd1L: 0.51 },
                '伊尔库茨克州': { humidity: 60, coords: [56.0, 105.0], waterPriceUsd1L: 0.58 },
                '加里宁格勒州': { humidity: 80, coords: [54.7104, 20.4522], waterPriceUsd1L: 0.64 },
                '卡卢加州': { humidity: 72, coords: [54.5, 35.5], waterPriceUsd1L: 0.58 },
                '堪察加边疆区': { humidity: 80, coords: [56.0, 159.0], waterPriceUsd1L: 0.90 },
                '克麦罗沃州': { humidity: 65, coords: [54.75, 87.14], waterPriceUsd1L: 0.51 },
                '基洛夫州': { humidity: 72, coords: [58.5, 50.0], waterPriceUsd1L: 0.51 },
                '科斯特罗马州': { humidity: 75, coords: [58.55, 43.95], waterPriceUsd1L: 0.51 },
                '库尔干州': { humidity: 65, coords: [55.45, 65.34], waterPriceUsd1L: 0.51 },
                '库尔斯克州': { humidity: 68, coords: [51.74, 36.19], waterPriceUsd1L: 0.51 },
                '利佩茨克州': { humidity: 68, coords: [52.60, 39.57], waterPriceUsd1L: 0.51 },
                '马加丹州': { humidity: 78, coords: [62.0, 153.0], waterPriceUsd1L: 0.90 },
                '摩尔曼斯克州': { humidity: 80, coords: [68.96, 33.08], waterPriceUsd1L: 0.64 },
                '下诺夫哥罗德州': { humidity: 70, coords: [56.33, 44.01], waterPriceUsd1L: 0.58 },
                '诺夫哥罗德州': { humidity: 78, coords: [58.52, 31.28], waterPriceUsd1L: 0.58 },
                '新西伯利亚州': { humidity: 60, coords: [55.0084, 82.9357], waterPriceUsd1L: 0.58 },
                '鄂木斯克州': { humidity: 60, coords: [54.99, 73.37], waterPriceUsd1L: 0.51 },
                '奥伦堡州': { humidity: 60, coords: [51.77, 55.10], waterPriceUsd1L: 0.51 },
                '奥廖尔州': { humidity: 72, coords: [52.97, 36.06], waterPriceUsd1L: 0.51 },
                '奔萨州': { humidity: 68, coords: [53.19, 45.02], waterPriceUsd1L: 0.51 },
                '彼尔姆边疆区': { humidity: 72, coords: [58.0, 56.32], waterPriceUsd1L: 0.58 },
                '普斯科夫州': { humidity: 78, coords: [57.82, 28.33], waterPriceUsd1L: 0.58 },
                '罗斯托夫州': { humidity: 60, coords: [47.2357, 39.7015], waterPriceUsd1L: 0.58 },
                '梁赞州': { humidity: 72, coords: [54.63, 39.69], waterPriceUsd1L: 0.51 },
                '萨马拉州': { humidity: 65, coords: [53.20, 50.16], waterPriceUsd1L: 0.58 },
                '萨拉托夫州': { humidity: 60, coords: [51.53, 46.03], waterPriceUsd1L: 0.51 },
                '萨哈林州': { humidity: 85, coords: [50.69, 142.95], waterPriceUsd1L: 0.77 },
                '斯维尔德洛夫斯克州': { humidity: 65, coords: [56.8389, 60.6057], waterPriceUsd1L: 0.58 },
                '斯摩棱斯克州': { humidity: 75, coords: [54.78, 32.05], waterPriceUsd1L: 0.51 },
                '坦波夫州': { humidity: 65, coords: [52.72, 41.45], waterPriceUsd1L: 0.51 },
                '特维尔州': { humidity: 75, coords: [56.86, 35.92], waterPriceUsd1L: 0.58 },
                '托木斯克州': { humidity: 70, coords: [58.60, 70.0], waterPriceUsd1L: 0.58 },
                '图拉州': { humidity: 70, coords: [54.19, 37.62], waterPriceUsd1L: 0.58 },
                '秋明州': { humidity: 70, coords: [57.16, 68.43], waterPriceUsd1L: 0.58 },
                '乌里扬诺夫斯克州': { humidity: 65, coords: [54.32, 48.40], waterPriceUsd1L: 0.51 },
                '车里雅宾斯克州': { humidity: 65, coords: [55.16, 61.40], waterPriceUsd1L: 0.58 },
                '外贝加尔边疆区': { humidity: 55, coords: [52.0, 115.0], waterPriceUsd1L: 0.58 },
                '雅罗斯拉夫尔州': { humidity: 75, coords: [57.63, 39.88], waterPriceUsd1L: 0.58 },
                '犹太自治州': { humidity: 70, coords: [48.8, 132.95], waterPriceUsd1L: 0.58 },
                '涅涅茨自治区': { humidity: 80, coords: [68.0, 53.0], waterPriceUsd1L: 0.77 },
                '汉特-曼西自治区': { humidity: 75, coords: [61.0, 69.0], waterPriceUsd1L: 0.64 },
                '楚科奇自治区': { humidity: 78, coords: [66.0, 169.0], waterPriceUsd1L: 1.03 },
                '亚马尔-涅涅茨自治区': { humidity: 78, coords: [66.5, 70.0], waterPriceUsd1L: 0.77 },
            }
        },
        '保加利亚': {
            coords: [42.7339, 25.4858],
            regions: {
            }
        },
        '克罗地亚': {
            coords: [45.1000, 15.2000],
            regions: {
            }
        },
        '冈比亚': {
            coords: [13.4432, -15.3101],
            regions: {
            }
        },
        '冰岛': {
            coords: [64.9631, -19.0208],
            regions: {
            }
        },
        '几内亚': {
            coords: [9.9456, -9.6966],
            regions: {
            }
        },
        '几内亚比绍': {
            coords: [11.8037, -15.1804],
            regions: {
            }
        },
        '列支敦士登': {
            coords: [47.1660, 9.5554],
            regions: {
            }
        },
        '刚果': {
            coords: [-0.2280, 15.8277],
            regions: {
            }
        },
        '刚果民主共和国': {
            coords: [-4.0383, 21.7587],
            regions: {
            }
        },
        '利比亚': {
            coords: [26.3351, 17.2283],
            regions: {
            }
        },
        '利比里亚': {
            coords: [6.4281, -9.4295],
            regions: {
            }
        },
        '加拿大': {
            coords: [56.1304, -106.3468],
            regions: {
            }
        },
        '加纳': {
            coords: [7.9465, -1.0232],
            regions: {
            }
        },
        '加蓬': {
            coords: [-0.8037, 11.6094],
            regions: {
            }
        },
        '匈牙利': {
            coords: [47.1625, 19.5033],
            regions: {
            }
        },
        '北马其顿': {
            coords: [41.6086, 21.7453],
            regions: {
            }
        },
        '南苏丹': {
            coords: [6.8770, 31.3070],
            regions: {
            }
        },
        '南非': {
            coords: [-30.5595, 22.9375],
            regions: {
            }
        },
        '博茨瓦纳': {
            coords: [-22.3285, 24.6849],
            regions: {
            }
        },
        '卡塔尔': {
            coords: [25.3548, 51.1839],
            regions: {
            }
        },
        '卢旺达': {
            coords: [-1.9403, 29.8739],
            regions: {
            }
        },
        '卢森堡': {
            coords: [49.8153, 6.1296],
            regions: {
            }
        },
        '印度': {
            coords: [20.5937, 78.9629],
            regions: {
            }
        },
        '印度尼西亚': {
            coords: [-0.7893, 113.9213],
            regions: {
                '雅加达': { humidity: 80, coords: [-6.2088, 106.8456], waterPriceUsd1L: 0.36 },
                '西爪哇': { humidity: 78, coords: [-6.9175, 107.6191], waterPriceUsd1L: 0.30 },
                '中爪哇': { humidity: 78, coords: [-7.1510, 110.1403], waterPriceUsd1L: 0.27 },
                '东爪哇': { humidity: 76, coords: [-7.5361, 112.2384], waterPriceUsd1L: 0.30 },
                '万丹': { humidity: 80, coords: [-6.4058, 106.0640], waterPriceUsd1L: 0.33 },
                '日惹': { humidity: 78, coords: [-7.7956, 110.3695], waterPriceUsd1L: 0.27 },
                '巴厘岛': { humidity: 78, coords: [-8.4095, 115.1889], waterPriceUsd1L: 0.42 },
                '西努沙登加拉': { humidity: 75, coords: [-8.6529, 117.3616], waterPriceUsd1L: 0.33 },
                '东努沙登加拉': { humidity: 70, coords: [-8.6574, 121.0794], waterPriceUsd1L: 0.36 },
                '西加里曼丹': { humidity: 85, coords: [-0.2787, 111.4752], waterPriceUsd1L: 0.33 },
                '中加里曼丹': { humidity: 85, coords: [-1.6815, 113.3824], waterPriceUsd1L: 0.36 },
                '南加里曼丹': { humidity: 82, coords: [-3.0926, 115.2838], waterPriceUsd1L: 0.33 },
                '东加里曼丹': { humidity: 82, coords: [0.5387, 116.4194], waterPriceUsd1L: 0.36 },
                '北加里曼丹': { humidity: 85, coords: [3.0731, 116.0414], waterPriceUsd1L: 0.39 },
                '北苏拉威西': { humidity: 82, coords: [0.6247, 123.9750], waterPriceUsd1L: 0.36 },
                '中苏拉威西': { humidity: 80, coords: [-1.4300, 121.4456], waterPriceUsd1L: 0.33 },
                '南苏拉威西': { humidity: 80, coords: [-3.6688, 119.9741], waterPriceUsd1L: 0.30 },
                '东南苏拉威西': { humidity: 82, coords: [-4.1449, 122.1746], waterPriceUsd1L: 0.33 },
                '哥伦打洛': { humidity: 80, coords: [0.6999, 122.4467], waterPriceUsd1L: 0.33 },
                '西苏拉威西': { humidity: 82, coords: [-2.8441, 119.2321], waterPriceUsd1L: 0.33 },
                '马鲁古': { humidity: 85, coords: [-3.2385, 130.1453], waterPriceUsd1L: 0.39 },
                '北马鲁古': { humidity: 85, coords: [1.5709, 127.8088], waterPriceUsd1L: 0.42 },
                '巴布亚': { humidity: 85, coords: [-4.2699, 138.0804], waterPriceUsd1L: 0.45 },
                '西巴布亚': { humidity: 85, coords: [-1.3361, 133.1747], waterPriceUsd1L: 0.45 },
                '亚齐': { humidity: 82, coords: [4.6951, 96.7494], waterPriceUsd1L: 0.30 },
                '北苏门答腊': { humidity: 82, coords: [2.1154, 99.5451], waterPriceUsd1L: 0.30 },
                '西苏门答腊': { humidity: 82, coords: [-0.7399, 100.8000], waterPriceUsd1L: 0.30 },
                '廖内': { humidity: 85, coords: [0.2933, 101.7068], waterPriceUsd1L: 0.33 },
                '廖内群岛': { humidity: 85, coords: [3.9457, 108.1429], waterPriceUsd1L: 0.36 },
                '占碑': { humidity: 82, coords: [-1.4852, 102.4381], waterPriceUsd1L: 0.30 },
                '南苏门答腊': { humidity: 82, coords: [-3.3194, 104.9147], waterPriceUsd1L: 0.30 },
                '邦加-勿里洞群岛': { humidity: 85, coords: [-2.7411, 106.4406], waterPriceUsd1L: 0.36 },
                '明古鲁': { humidity: 82, coords: [-3.5778, 102.3464], waterPriceUsd1L: 0.30 },
                '楠榜': { humidity: 80, coords: [-4.5586, 105.4068], waterPriceUsd1L: 0.30 },
            }
        },
        '危地马拉': {
            coords: [15.7835, -90.2308],
            regions: {
            }
        },
        '厄瓜多尔': {
            coords: [-1.8312, -78.1834],
            regions: {
            }
        },
        '厄立特里亚': {
            coords: [15.1794, 39.7823],
            regions: {
            }
        },
        '叙利亚': {
            coords: [34.8021, 38.9968],
            regions: {
            }
        },
        '古巴': {
            coords: [21.5218, -77.7812],
            regions: {
            }
        },
        '吉尔吉斯斯坦': {
            coords: [41.2044, 74.7661],
            regions: {
            }
        },
        '吉布提': {
            coords: [11.8251, 42.5903],
            regions: {
            }
        },
        '哈萨克斯坦': {
            coords: [48.0196, 66.9237],
            regions: {
            }
        },
        '哥伦比亚': {
            coords: [4.5709, -74.2973],
            regions: {
            }
        },
        '哥斯达黎加': {
            coords: [9.7489, -83.7534],
            regions: {
            }
        },
        '喀麦隆': {
            coords: [7.3697, 12.3547],
            regions: {
            }
        },
        '图瓦卢': {
            coords: [-7.1095, 177.6493],
            regions: {
            }
        },
        '土库曼斯坦': {
            coords: [38.9697, 59.5563],
            regions: {
            }
        },
        '土耳其': {
            coords: [38.9637, 35.2433],
            regions: {
            }
        },
        '圣卢西亚': {
            coords: [13.9094, -60.9789],
            regions: {
            }
        },
        '圣基茨和尼维斯': {
            coords: [17.3578, -62.7830],
            regions: {
            }
        },
        '圣多美和普林西比': {
            coords: [0.1864, 6.6131],
            regions: {
            }
        },
        '圣文森特和格林纳丁斯': {
            coords: [12.9843, -61.2872],
            regions: {
            }
        },
        '圣马力诺': {
            coords: [43.9424, 12.4578],
            regions: {
            }
        },
        '圭亚那': {
            coords: [4.8604, -58.9302],
            regions: {
            }
        },
        '坦桑尼亚': {
            coords: [-6.3690, 34.8888],
            regions: {
            }
        },
        '埃及': {
            coords: [26.8206, 30.8025],
            regions: {
            }
        },
        '埃塞俄比亚': {
            coords: [9.1450, 38.7667],
            regions: {
            }
        },
        '基里巴斯': {
            coords: [-3.3704, -168.7340],
            regions: {
            }
        },
        '塔吉克斯坦': {
            coords: [38.8610, 71.2761],
            regions: {
            }
        },
        '塞内加尔': {
            coords: [14.4974, -14.4524],
            regions: {
            }
        },
        '塞尔维亚': {
            coords: [44.0165, 21.0059],
            regions: {
            }
        },
        '塞拉利昂': {
            coords: [8.4606, -11.7799],
            regions: {
            }
        },
        '塞浦路斯': {
            coords: [35.1264, 33.4299],
            regions: {
            }
        },
        '塞舌尔': {
            coords: [-4.6796, 55.4920],
            regions: {
            }
        },
        '墨西哥': {
            coords: [23.6345, -102.5528],
            regions: {
            }
        },
        '多哥': {
            coords: [8.6195, 0.8248],
            regions: {
            }
        },
        '多米尼克': {
            coords: [15.4150, -61.3710],
            regions: {
            }
        },
        '多米尼加共和国': {
            coords: [18.7357, -70.1627],
            regions: {
            }
        },
        '奥地利': {
            coords: [47.5162, 14.5501],
            regions: {
            }
        },
        '委内瑞拉': {
            coords: [6.4238, -66.5897],
            regions: {
            }
        },
        '孟加拉国': {
            coords: [23.6850, 90.3563],
            regions: {
            }
        },
        '安哥拉': {
            coords: [-11.2027, 17.8739],
            regions: {
            }
        },
        '安提瓜和巴布达': {
            coords: [17.0608, -61.7964],
            regions: {
            }
        },
        '安道尔': {
            coords: [42.5462, 1.6016],
            regions: {
            }
        },
        '密克罗尼西亚': {
            coords: [7.4256, 150.5508],
            regions: {
            }
        },
        '尼加拉瓜': {
            coords: [12.2650, -85.2072],
            regions: {
            }
        },
        '尼日利亚': {
            coords: [9.0820, 8.6753],
            regions: {
            }
        },
        '尼日尔': {
            coords: [17.6078, 8.0817],
            regions: {
            }
        },
        '尼泊尔': {
            coords: [28.3949, 84.1240],
            regions: {
            }
        },
        '巴哈马': {
            coords: [25.0343, -77.3963],
            regions: {
            }
        },
        '巴基斯坦': {
            coords: [30.3753, 69.3451],
            regions: {
            }
        },
        '巴巴多斯': {
            coords: [13.1939, -59.5432],
            regions: {
            }
        },
        '巴布亚新几内亚': {
            coords: [-6.3150, 143.9555],
            regions: {
            }
        },
        '巴拉圭': {
            coords: [-23.4425, -58.4438],
            regions: {
            }
        },
        '巴拿马': {
            coords: [8.5380, -80.7821],
            regions: {
            }
        },
        '巴林': {
            coords: [26.0667, 50.5577],
            regions: {
            }
        },
        '巴西': {
            coords: [-14.2350, -51.9253],
            regions: {
            }
        },
        '布基纳法索': {
            coords: [12.2383, -1.5616],
            regions: {
            }
        },
        '布隆迪': {
            coords: [-3.3731, 29.9189],
            regions: {
            }
        },
        '希腊': {
            coords: [39.0742, 21.8243],
            regions: {
            }
        },
        '帕劳': {
            coords: [7.5150, 134.5825],
            regions: {
            }
        },
        '德国': {
            coords: [51.1657, 10.4515],
            regions: {
            }
        },
        '意大利': {
            coords: [41.8719, 12.5674],
            regions: {
            }
        },
        '所罗门群岛': {
            coords: [-9.6457, 160.1562],
            regions: {
            }
        },
        '拉脱维亚': {
            coords: [56.8796, 24.6032],
            regions: {
            }
        },
        '挪威': {
            coords: [60.4720, 8.4689],
            regions: {
            }
        },
        '捷克': {
            coords: [49.8175, 15.4730],
            regions: {
            }
        },
        '摩尔多瓦': {
            coords: [47.4116, 28.3699],
            regions: {
            }
        },
        '摩洛哥': {
            coords: [31.7917, -7.0926],
            regions: {
            }
        },
        '摩纳哥': {
            coords: [43.7384, 7.4246],
            regions: {
            }
        },
        '文莱': {
            coords: [4.5353, 114.7277],
            regions: {
            }
        },
        '斐济': {
            coords: [-16.7784, 178.0650],
            regions: {
            }
        },
        '斯威士兰': {
            coords: [-26.5225, 31.4659],
            regions: {
            }
        },
        '斯洛伐克': {
            coords: [48.6690, 19.6990],
            regions: {
            }
        },
        '斯洛文尼亚': {
            coords: [46.1512, 14.9955],
            regions: {
            }
        },
        '斯里兰卡': {
            coords: [7.8731, 80.7718],
            regions: {
            }
        },
        '新加坡': {
            coords: [1.3521, 103.8198],
            regions: {
            }
        },
        '新西兰': {
            coords: [-40.9006, 174.8860],
            regions: {
            }
        },
        '日本': {
            coords: [36.2048, 138.2529],
            regions: {
            }
        },
        '智利': {
            coords: [-35.6751, -71.5430],
            regions: {
            }
        },
        '朝鲜': {
            coords: [40.3399, 127.5101],
            regions: {
            }
        },
        '柬埔寨': {
            coords: [12.5657, 104.9910],
            regions: {
            }
        },
        '格林纳达': {
            coords: [12.1165, -61.6790],
            regions: {
            }
        },
        '格鲁吉亚': {
            coords: [42.3154, 43.3569],
            regions: {
            }
        },
        '梵蒂冈': {
            coords: [41.9029, 12.4534],
            regions: {
            }
        },
        '比利时': {
            coords: [50.5039, 4.4699],
            regions: {
            }
        },
        '毛里塔尼亚': {
            coords: [21.0079, -10.9408],
            regions: {
            }
        },
        '毛里求斯': {
            coords: [-20.3484, 57.5522],
            regions: {
            }
        },
        '汤加': {
            coords: [-21.1789, -175.1982],
            regions: {
            }
        },
        '沙特阿拉伯': {
            coords: [23.8859, 45.0792],
            regions: {
                '利雅得': { humidity: 47, coords: [24.7136, 46.6753], waterPriceUsd1L: 0.40 },
                '麦加': { humidity: 50, coords: [21.3891, 39.8579], waterPriceUsd1L: 0.45 },
                '麦地那': { humidity: 40, coords: [24.5247, 39.5692], waterPriceUsd1L: 0.42 },
                '东部省': { humidity: 65, coords: [26.4207, 50.0888], waterPriceUsd1L: 0.38 },
                '阿西尔': { humidity: 55, coords: [18.2164, 42.5053], waterPriceUsd1L: 0.35 },
                '吉赞': { humidity: 70, coords: [16.8892, 42.5611], waterPriceUsd1L: 0.35 },
                '奈季兰': { humidity: 35, coords: [17.4933, 44.1277], waterPriceUsd1L: 0.35 },
                '巴哈': { humidity: 45, coords: [19.8614, 41.4414], waterPriceUsd1L: 0.35 },
                '塔布克': { humidity: 35, coords: [28.3838, 36.5550], waterPriceUsd1L: 0.38 },
                '焦夫': { humidity: 35, coords: [29.7889, 39.8789], waterPriceUsd1L: 0.35 },
                '北部边疆': { humidity: 40, coords: [31.1728, 37.9888], waterPriceUsd1L: 0.35 },
                '哈伊勒': { humidity: 35, coords: [27.5219, 41.6906], waterPriceUsd1L: 0.35 },
                '卡西姆': { humidity: 40, coords: [26.2076, 43.4839], waterPriceUsd1L: 0.35 }
            }
        },
        '法国': {
            coords: [46.2276, 2.2137],
            regions: {
            }
        },
        '波兰': {
            coords: [51.9194, 19.1451],
            regions: {
            }
        },
        '波黑': {
            coords: [43.9159, 17.6791],
            regions: {
            }
        },
        '泰国': {
            coords: [15.8700, 100.9925],
            regions: {
            }
        },
        '津巴布韦': {
            coords: [-19.0154, 29.1549],
            regions: {
            }
        },
        '洪都拉斯': {
            coords: [15.2000, -86.2419],
            regions: {
            }
        },
        '海地': {
            coords: [18.9712, -72.2852],
            regions: {
            }
        },
        '澳大利亚': {
            coords: [-25.2744, 133.7751],
            regions: {
            }
        },
        '爱尔兰': {
            coords: [53.4129, -8.2439],
            regions: {
            }
        },
        '爱沙尼亚': {
            coords: [58.5953, 25.0136],
            regions: {
            }
        },
        '牙买加': {
            coords: [18.1096, -77.2975],
            regions: {
            }
        },
        '特立尼达和多巴哥': {
            coords: [10.6918, -61.2225],
            regions: {
            }
        },
        '玻利维亚': {
            coords: [-16.2902, -63.5887],
            regions: {
            }
        },
        '瑙鲁': {
            coords: [-0.5228, 166.9315],
            regions: {
            }
        },
        '瑞典': {
            coords: [60.1282, 18.6435],
            regions: {
            }
        },
        '瑞士': {
            coords: [46.8182, 8.2275],
            regions: {
            }
        },
        '瓦努阿图': {
            coords: [-15.3767, 166.9592],
            regions: {
            }
        },
        '白俄罗斯': {
            coords: [53.7098, 27.9534],
            regions: {
            }
        },
        '科威特': {
            coords: [29.3117, 47.4818],
            regions: {
            }
        },
        '科摩罗': {
            coords: [-11.6455, 43.3333],
            regions: {
            }
        },
        '秘鲁': {
            coords: [-9.1900, -75.0152],
            regions: {
            }
        },
        '突尼斯': {
            coords: [33.8869, 9.5375],
            regions: {
            }
        },
        '立陶宛': {
            coords: [55.1694, 23.8813],
            regions: {
            }
        },
        '索马里': {
            coords: [5.1521, 46.1996],
            regions: {
            }
        },
        '约旦': {
            coords: [30.5852, 36.2384],
            regions: {
            }
        },
        '纳米比亚': {
            coords: [-22.9576, 18.4904],
            regions: {
            }
        },
        '缅甸': {
            coords: [21.9162, 95.9560],
            regions: {
            }
        },
        '罗马尼亚': {
            coords: [45.9432, 24.9668],
            regions: {
            }
        },
        '美国': {
            coords: [37.0902, -95.7129],
            regions: {
            }
        },
        '老挝': {
            coords: [19.8563, 102.4955],
            regions: {
            }
        },
        '肯尼亚': {
            coords: [-0.0236, 37.9062],
            regions: {
            }
        },
        '芬兰': {
            coords: [61.9241, 25.7482],
            regions: {
            }
        },
        '苏丹': {
            coords: [12.8628, 30.2176],
            regions: {
            }
        },
        '苏里南': {
            coords: [3.9193, -56.0278],
            regions: {
            }
        },
        '英国': {
            coords: [55.3781, -3.4360],
            regions: {
            }
        },
        '荷兰': {
            coords: [52.1326, 5.2913],
            regions: {
            }
        },
        '莫桑比克': {
            coords: [-18.6657, 35.5296],
            regions: {
            }
        },
        '莱索托': {
            coords: [-29.6100, 28.2336],
            regions: {
            }
        },
        '菲律宾': {
            coords: [12.8797, 121.7740],
            regions: {
            }
        },
        '萨尔瓦多': {
            coords: [13.7942, -88.8965],
            regions: {
            }
        },
        '萨摩亚': {
            coords: [-13.7590, -172.1046],
            regions: {
            }
        },
        '葡萄牙': {
            coords: [39.3999, -8.2245],
            regions: {
            }
        },
        '蒙古': {
            coords: [46.8625, 103.8467],
            regions: {
            }
        },
        '西班牙': {
            coords: [40.4637, -3.7492],
            regions: {
            }
        },
        '贝宁': {
            coords: [9.3077, 2.3158],
            regions: {
            }
        },
        '赞比亚': {
            coords: [-13.1339, 27.8493],
            regions: {
            }
        },
        '赤道几内亚': {
            coords: [1.6508, 10.2679],
            regions: {
            }
        },
        '越南': {
            coords: [14.0583, 108.2772],
            regions: {
            }
        },
        '阿塞拜疆': {
            coords: [40.1431, 47.5769],
            regions: {
            }
        },
        '阿富汗': {
            coords: [33.9391, 67.7100],
            regions: {
            }
        },
        '阿尔及利亚': {
            coords: [28.0339, 1.6596],
            regions: {
            }
        },
        '阿尔巴尼亚': {
            coords: [41.1533, 20.1683],
            regions: {
            }
        },
        '阿曼': {
            coords: [21.4735, 55.9754],
            regions: {
            }
        },
        '阿根廷': {
            coords: [-38.4161, -63.6167],
            regions: {
            }
        },
        '阿联酋': {
            coords: [23.4241, 53.8478],
            regions: {
                '阿布扎比': { humidity: 60, coords: [24.4539, 54.3773], waterPriceUsd1L: 0.35 },
                '迪拜': { humidity: 55, coords: [25.2048, 55.2708], waterPriceUsd1L: 0.40 },
                '沙迦': { humidity: 55, coords: [25.3463, 55.4209], waterPriceUsd1L: 0.32 },
                '阿治曼': { humidity: 55, coords: [25.4052, 55.5136], waterPriceUsd1L: 0.30 },
                '乌姆盖万': { humidity: 50, coords: [25.5647, 55.5552], waterPriceUsd1L: 0.30 },
                '哈伊马角': { humidity: 55, coords: [25.7895, 55.9432], waterPriceUsd1L: 0.30 },
                '富查伊拉': { humidity: 65, coords: [25.1288, 56.3264], waterPriceUsd1L: 0.32 }
            }
        },
        '韩国': {
            coords: [35.9078, 127.7669],
            regions: {
            }
        },
        '马尔代夫': {
            coords: [3.2028, 73.2207],
            regions: {
            }
        },
        '马拉维': {
            coords: [-13.2543, 34.3015],
            regions: {
            }
        },
        '马来西亚': {
            coords: [4.2105, 101.9758],
            regions: {
            }
        },
        '马绍尔群岛': {
            coords: [7.1315, 171.1845],
            regions: {
            }
        },
        '马耳他': {
            coords: [35.9375, 14.3754],
            regions: {
            }
        },
        '马达加斯加': {
            coords: [-18.7669, 46.8691],
            regions: {
            }
        },
        '马里': {
            coords: [17.5707, -3.9962],
            regions: {
            }
        },
        '黎巴嫩': {
            coords: [33.8547, 35.8623],
            regions: {
            }
        },
        '黑山': {
            coords: [42.7087, 19.3744],
            regions: {
            }
        },
    },
    'es': {
        'Afganistán': {
            coords: [33.9391, 67.7100],
            regions: {
            }
        },
        'Albania': {
            coords: [41.1533, 20.1683],
            regions: {
            }
        },
        'Alemania': {
            coords: [51.1657, 10.4515],
            regions: {
            }
        },
        'Andorra': {
            coords: [42.5462, 1.6016],
            regions: {
            }
        },
        'Angola': {
            coords: [-11.2027, 17.8739],
            regions: {
            }
        },
        'Antigua y Barbuda': {
            coords: [17.0608, -61.7964],
            regions: {
            }
        },
        'Arabia Saudí': {
            coords: [23.8859, 45.0792],
            regions: {
                'Riad': { humidity: 47, coords: [24.7136, 46.6753], waterPriceUsd1L: 0.40 },
                'La Meca': { humidity: 50, coords: [21.3891, 39.8579], waterPriceUsd1L: 0.45 },
                'Medina': { humidity: 40, coords: [24.5247, 39.5692], waterPriceUsd1L: 0.42 },
                'Provincia Oriental': { humidity: 65, coords: [26.4207, 50.0888], waterPriceUsd1L: 0.38 },
                'Asir': { humidity: 55, coords: [18.2164, 42.5053], waterPriceUsd1L: 0.35 },
                'Jizan': { humidity: 70, coords: [16.8892, 42.5611], waterPriceUsd1L: 0.35 },
                'Najrán': { humidity: 35, coords: [17.4933, 44.1277], waterPriceUsd1L: 0.35 },
                'Al Bahah': { humidity: 45, coords: [19.8614, 41.4414], waterPriceUsd1L: 0.35 },
                'Tabuk': { humidity: 35, coords: [28.3838, 36.5550], waterPriceUsd1L: 0.38 },
                'Al Yauf': { humidity: 35, coords: [29.7889, 39.8789], waterPriceUsd1L: 0.35 },
                'Fronteras del Norte': { humidity: 40, coords: [31.1728, 37.9888], waterPriceUsd1L: 0.35 },
                'Hail': { humidity: 35, coords: [27.5219, 41.6906], waterPriceUsd1L: 0.35 },
                'Al Qasim': { humidity: 40, coords: [26.2076, 43.4839], waterPriceUsd1L: 0.35 }
            }
        },
        'Argelia': {
            coords: [28.0339, 1.6596],
            regions: {
            }
        },
        'Argentina': {
            coords: [-38.4161, -63.6167],
            regions: {
            }
        },
        'Armenia': {
            coords: [40.0691, 45.0382],
            regions: {
            }
        },
        'Australia': {
            coords: [-25.2744, 133.7751],
            regions: {
            }
        },
        'Austria': {
            coords: [47.5162, 14.5501],
            regions: {
            }
        },
        'Azerbaiyán': {
            coords: [40.1431, 47.5769],
            regions: {
            }
        },
        'Bahamas': {
            coords: [25.0343, -77.3963],
            regions: {
            }
        },
        'Bangladesh': {
            coords: [23.6850, 90.3563],
            regions: {
            }
        },
        'Barbados': {
            coords: [13.1939, -59.5432],
            regions: {
            }
        },
        'Baréin': {
            coords: [26.0667, 50.5577],
            regions: {
            }
        },
        'Belice': {
            coords: [17.1899, -88.4976],
            regions: {
            }
        },
        'Benín': {
            coords: [9.3077, 2.3158],
            regions: {
            }
        },
        'Bielorrusia': {
            coords: [53.7098, 27.9534],
            regions: {
            }
        },
        'Bolivia': {
            coords: [-16.2902, -63.5887],
            regions: {
            }
        },
        'Bosnia y Herzegovina': {
            coords: [43.9159, 17.6791],
            regions: {
            }
        },
        'Botsuana': {
            coords: [-22.3285, 24.6849],
            regions: {
            }
        },
        'Brasil': {
            coords: [-14.2350, -51.9253],
            regions: {
            }
        },
        'Brunéi': {
            coords: [4.5353, 114.7277],
            regions: {
            }
        },
        'Bulgaria': {
            coords: [42.7339, 25.4858],
            regions: {
            }
        },
        'Burkina Faso': {
            coords: [12.2383, -1.5616],
            regions: {
            }
        },
        'Burundi': {
            coords: [-3.3731, 29.9189],
            regions: {
            }
        },
        'Bután': {
            coords: [27.5142, 90.4336],
            regions: {
            }
        },
        'Bélgica': {
            coords: [50.5039, 4.4699],
            regions: {
            }
        },
        'Cabo Verde': {
            coords: [16.5388, -24.0132],
            regions: {
            }
        },
        'Camboya': {
            coords: [12.5657, 104.9910],
            regions: {
            }
        },
        'Camerún': {
            coords: [7.3697, 12.3547],
            regions: {
            }
        },
        'Canadá': {
            coords: [56.1304, -106.3468],
            regions: {
            }
        },
        'Catar': {
            coords: [25.3548, 51.1839],
            regions: {
            }
        },
        'Chad': {
            coords: [15.4542, 18.7322],
            regions: {
            }
        },
        'Chile': {
            coords: [-35.6751, -71.5430],
            regions: {
            }
        },
        'China': {
            coords: [35.8617, 104.1954],
            regions: {
            }
        },
        'Chipre': {
            coords: [35.1264, 33.4299],
            regions: {
            }
        },
        'Colombia': {
            coords: [4.5709, -74.2973],
            regions: {
            }
        },
        'Comoras': {
            coords: [-11.6455, 43.3333],
            regions: {
            }
        },
        'Congo': {
            coords: [-0.2280, 15.8277],
            regions: {
            }
        },
        'Corea del Norte': {
            coords: [40.3399, 127.5101],
            regions: {
            }
        },
        'Corea del Sur': {
            coords: [35.9078, 127.7669],
            regions: {
            }
        },
        'Costa Rica': {
            coords: [9.7489, -83.7534],
            regions: {
            }
        },
        'Croacia': {
            coords: [45.1000, 15.2000],
            regions: {
            }
        },
        'Cuba': {
            coords: [21.5218, -77.7812],
            regions: {
            }
        },
        'Dinamarca': {
            coords: [56.2639, 9.5018],
            regions: {
            }
        },
        'Dominica': {
            coords: [15.4150, -61.3710],
            regions: {
            }
        },
        'Ecuador': {
            coords: [-1.8312, -78.1834],
            regions: {
            }
        },
        'Egipto': {
            coords: [26.8206, 30.8025],
            regions: {
            }
        },
        'El Salvador': {
            coords: [13.7942, -88.8965],
            regions: {
            }
        },
        'Emiratos Árabes Unidos': {
            coords: [23.4241, 53.8478],
            regions: {
                'Abu Dabi': { humidity: 60, coords: [24.4539, 54.3773], waterPriceUsd1L: 0.35 },
                'Dubái': { humidity: 55, coords: [25.2048, 55.2708], waterPriceUsd1L: 0.40 },
                'Sharjah': { humidity: 55, coords: [25.3463, 55.4209], waterPriceUsd1L: 0.32 },
                'Ajmán': { humidity: 55, coords: [25.4052, 55.5136], waterPriceUsd1L: 0.30 },
                'Umm Al Qaywayn': { humidity: 50, coords: [25.5647, 55.5552], waterPriceUsd1L: 0.30 },
                'Ras el Jaima': { humidity: 55, coords: [25.7895, 55.9432], waterPriceUsd1L: 0.30 },
                'Fuyaira': { humidity: 65, coords: [25.1288, 56.3264], waterPriceUsd1L: 0.32 }
            }
        },
        'Eritrea': {
            coords: [15.1794, 39.7823],
            regions: {
            }
        },
        'Eslovaquia': {
            coords: [48.6690, 19.6990],
            regions: {
            }
        },
        'Eslovenia': {
            coords: [46.1512, 14.9955],
            regions: {
            }
        },
        'España': {
            coords: [40.4637, -3.7492],
            regions: {
            }
        },
        'Estados Unidos': {
            coords: [37.0902, -95.7129],
            regions: {
            }
        },
        'Estonia': {
            coords: [58.5953, 25.0136],
            regions: {
            }
        },
        'Esuatini': {
            coords: [-26.5225, 31.4659],
            regions: {
            }
        },
        'Etiopía': {
            coords: [9.1450, 38.7667],
            regions: {
            }
        },
        'Filipinas': {
            coords: [12.8797, 121.7740],
            regions: {
            }
        },
        'Finlandia': {
            coords: [61.9241, 25.7482],
            regions: {
            }
        },
        'Fiyi': {
            coords: [-16.7784, 178.0650],
            regions: {
            }
        },
        'Francia': {
            coords: [46.2276, 2.2137],
            regions: {
            }
        },
        'Gabón': {
            coords: [-0.8037, 11.6094],
            regions: {
            }
        },
        'Gambia': {
            coords: [13.4432, -15.3101],
            regions: {
            }
        },
        'Georgia': {
            coords: [42.3154, 43.3569],
            regions: {
            }
        },
        'Ghana': {
            coords: [7.9465, -1.0232],
            regions: {
            }
        },
        'Granada': {
            coords: [12.1165, -61.6790],
            regions: {
            }
        },
        'Grecia': {
            coords: [39.0742, 21.8243],
            regions: {
            }
        },
        'Guatemala': {
            coords: [15.7835, -90.2308],
            regions: {
            }
        },
        'Guinea': {
            coords: [9.9456, -9.6966],
            regions: {
            }
        },
        'Guinea Ecuatorial': {
            coords: [1.6508, 10.2679],
            regions: {
            }
        },
        'Guinea-Bisáu': {
            coords: [11.8037, -15.1804],
            regions: {
            }
        },
        'Guyana': {
            coords: [4.8604, -58.9302],
            regions: {
            }
        },
        'Haití': {
            coords: [18.9712, -72.2852],
            regions: {
            }
        },
        'Honduras': {
            coords: [15.2000, -86.2419],
            regions: {
            }
        },
        'Hungría': {
            coords: [47.1625, 19.5033],
            regions: {
            }
        },
        'India': {
            coords: [20.5937, 78.9629],
            regions: {
            }
        },
        'Indonesia': {
            coords: [-0.7893, 113.9213],
            regions: {
                'Yakarta': { humidity: 80, coords: [-6.2088, 106.8456], waterPriceUsd1L: 0.36 },
                'Java Occidental': { humidity: 78, coords: [-6.9175, 107.6191], waterPriceUsd1L: 0.30 },
                'Java Central': { humidity: 78, coords: [-7.1510, 110.1403], waterPriceUsd1L: 0.27 },
                'Java Oriental': { humidity: 76, coords: [-7.5361, 112.2384], waterPriceUsd1L: 0.30 },
                'Bantén': { humidity: 80, coords: [-6.4058, 106.0640], waterPriceUsd1L: 0.33 },
                'Yogyakarta': { humidity: 78, coords: [-7.7956, 110.3695], waterPriceUsd1L: 0.27 },
                'Bali': { humidity: 78, coords: [-8.4095, 115.1889], waterPriceUsd1L: 0.42 },
                'Nusatenggara Occidental': { humidity: 75, coords: [-8.6529, 117.3616], waterPriceUsd1L: 0.33 },
                'Nusatenggara Oriental': { humidity: 70, coords: [-8.6574, 121.0794], waterPriceUsd1L: 0.36 },
                'Kalimantan Occidental': { humidity: 85, coords: [-0.2787, 111.4752], waterPriceUsd1L: 0.33 },
                'Kalimantan Central': { humidity: 85, coords: [-1.6815, 113.3824], waterPriceUsd1L: 0.36 },
                'Kalimantan Meridional': { humidity: 82, coords: [-3.0926, 115.2838], waterPriceUsd1L: 0.33 },
                'Kalimantan Oriental': { humidity: 82, coords: [0.5387, 116.4194], waterPriceUsd1L: 0.36 },
                'Kalimantan Septentrional': { humidity: 85, coords: [3.0731, 116.0414], waterPriceUsd1L: 0.39 },
                'Sulawesi Septentrional': { humidity: 82, coords: [0.6247, 123.9750], waterPriceUsd1L: 0.36 },
                'Sulawesi Central': { humidity: 80, coords: [-1.4300, 121.4456], waterPriceUsd1L: 0.33 },
                'Sulawesi Meridional': { humidity: 80, coords: [-3.6688, 119.9741], waterPriceUsd1L: 0.30 },
                'Sulawesi Suroriental': { humidity: 82, coords: [-4.1449, 122.1746], waterPriceUsd1L: 0.33 },
                'Gorontalo': { humidity: 80, coords: [0.6999, 122.4467], waterPriceUsd1L: 0.33 },
                'Sulawesi Occidental': { humidity: 82, coords: [-2.8441, 119.2321], waterPriceUsd1L: 0.33 },
                'Molucas': { humidity: 85, coords: [-3.2385, 130.1453], waterPriceUsd1L: 0.39 },
                'Molucas del Norte': { humidity: 85, coords: [1.5709, 127.8088], waterPriceUsd1L: 0.42 },
                'Papúa': { humidity: 85, coords: [-4.2699, 138.0804], waterPriceUsd1L: 0.45 },
                'Papúa Occidental': { humidity: 85, coords: [-1.3361, 133.1747], waterPriceUsd1L: 0.45 },
                'Aceh': { humidity: 82, coords: [4.6951, 96.7494], waterPriceUsd1L: 0.30 },
                'Sumatra Septentrional': { humidity: 82, coords: [2.1154, 99.5451], waterPriceUsd1L: 0.30 },
                'Sumatra Occidental': { humidity: 82, coords: [-0.7399, 100.8000], waterPriceUsd1L: 0.30 },
                'Riau': { humidity: 85, coords: [0.2933, 101.7068], waterPriceUsd1L: 0.33 },
                'Islas Riau': { humidity: 85, coords: [3.9457, 108.1429], waterPriceUsd1L: 0.36 },
                'Jambi': { humidity: 82, coords: [-1.4852, 102.4381], waterPriceUsd1L: 0.30 },
                'Sumatra Meridional': { humidity: 82, coords: [-3.3194, 104.9147], waterPriceUsd1L: 0.30 },
                'Islas Bangka Belitung': { humidity: 85, coords: [-2.7411, 106.4406], waterPriceUsd1L: 0.36 },
                'Bengkulu': { humidity: 82, coords: [-3.5778, 102.3464], waterPriceUsd1L: 0.30 },
                'Lampung': { humidity: 80, coords: [-4.5586, 105.4068], waterPriceUsd1L: 0.30 },
            }
        },
        'Irak': {
            coords: [33.2232, 43.6793],
            regions: {
            }
        },
        'Irlanda': {
            coords: [53.4129, -8.2439],
            regions: {
            }
        },
        'Islandia': {
            coords: [64.9631, -19.0208],
            regions: {
            }
        },
        'Islas Marshall': {
            coords: [7.1315, 171.1845],
            regions: {
            }
        },
        'Islas Salomón': {
            coords: [-9.6457, 160.1562],
            regions: {
            }
        },
        'Israel': {
            coords: [31.0461, 34.8516],
            regions: {
            }
        },
        'Italia': {
            coords: [41.8719, 12.5674],
            regions: {
            }
        },
        'Jamaica': {
            coords: [18.1096, -77.2975],
            regions: {
            }
        },
        'Japón': {
            coords: [36.2048, 138.2529],
            regions: {
            }
        },
        'Jordania': {
            coords: [30.5852, 36.2384],
            regions: {
            }
        },
        'Kazajistán': {
            coords: [48.0196, 66.9237],
            regions: {
            }
        },
        'Kenia': {
            coords: [-0.0236, 37.9062],
            regions: {
            }
        },
        'Kirguistán': {
            coords: [41.2044, 74.7661],
            regions: {
            }
        },
        'Kiribati': {
            coords: [-3.3704, -168.7340],
            regions: {
            }
        },
        'Kuwait': {
            coords: [29.3117, 47.4818],
            regions: {
            }
        },
        'Laos': {
            coords: [19.8563, 102.4955],
            regions: {
            }
        },
        'Lesoto': {
            coords: [-29.6100, 28.2336],
            regions: {
            }
        },
        'Letonia': {
            coords: [56.8796, 24.6032],
            regions: {
            }
        },
        'Liberia': {
            coords: [6.4281, -9.4295],
            regions: {
            }
        },
        'Libia': {
            coords: [26.3351, 17.2283],
            regions: {
            }
        },
        'Liechtenstein': {
            coords: [47.1660, 9.5554],
            regions: {
            }
        },
        'Lituania': {
            coords: [55.1694, 23.8813],
            regions: {
            }
        },
        'Luxemburgo': {
            coords: [49.8153, 6.1296],
            regions: {
            }
        },
        'Líbano': {
            coords: [33.8547, 35.8623],
            regions: {
            }
        },
        'Macedonia del Norte': {
            coords: [41.6086, 21.7453],
            regions: {
            }
        },
        'Madagascar': {
            coords: [-18.7669, 46.8691],
            regions: {
            }
        },
        'Malasia': {
            coords: [4.2105, 101.9758],
            regions: {
            }
        },
        'Malaui': {
            coords: [-13.2543, 34.3015],
            regions: {
            }
        },
        'Maldivas': {
            coords: [3.2028, 73.2207],
            regions: {
            }
        },
        'Malta': {
            coords: [35.9375, 14.3754],
            regions: {
            }
        },
        'Malí': {
            coords: [17.5707, -3.9962],
            regions: {
            }
        },
        'Marruecos': {
            coords: [31.7917, -7.0926],
            regions: {
            }
        },
        'Mauricio': {
            coords: [-20.3484, 57.5522],
            regions: {
            }
        },
        'Mauritania': {
            coords: [21.0079, -10.9408],
            regions: {
            }
        },
        'Micronesia': {
            coords: [7.4256, 150.5508],
            regions: {
            }
        },
        'Moldavia': {
            coords: [47.4116, 28.3699],
            regions: {
            }
        },
        'Mongolia': {
            coords: [46.8625, 103.8467],
            regions: {
            }
        },
        'Montenegro': {
            coords: [42.7087, 19.3744],
            regions: {
            }
        },
        'Mozambique': {
            coords: [-18.6657, 35.5296],
            regions: {
            }
        },
        'Myanmar': {
            coords: [21.9162, 95.9560],
            regions: {
            }
        },
        'México': {
            coords: [23.6345, -102.5528],
            regions: {
            }
        },
        'Mónaco': {
            coords: [43.7384, 7.4246],
            regions: {
            }
        },
        'Namibia': {
            coords: [-22.9576, 18.4904],
            regions: {
            }
        },
        'Nauru': {
            coords: [-0.5228, 166.9315],
            regions: {
            }
        },
        'Nepal': {
            coords: [28.3949, 84.1240],
            regions: {
            }
        },
        'Nicaragua': {
            coords: [12.2650, -85.2072],
            regions: {
            }
        },
        'Nigeria': {
            coords: [9.0820, 8.6753],
            regions: {
            }
        },
        'Noruega': {
            coords: [60.4720, 8.4689],
            regions: {
            }
        },
        'Nueva Zelanda': {
            coords: [-40.9006, 174.8860],
            regions: {
            }
        },
        'Níger': {
            coords: [17.6078, 8.0817],
            regions: {
            }
        },
        'Omán': {
            coords: [21.4735, 55.9754],
            regions: {
            }
        },
        'Pakistán': {
            coords: [30.3753, 69.3451],
            regions: {
            }
        },
        'Palaos': {
            coords: [7.5150, 134.5825],
            regions: {
            }
        },
        'Panamá': {
            coords: [8.5380, -80.7821],
            regions: {
            }
        },
        'Papúa Nueva Guinea': {
            coords: [-6.3150, 143.9555],
            regions: {
            }
        },
        'Paraguay': {
            coords: [-23.4425, -58.4438],
            regions: {
            }
        },
        'Países Bajos': {
            coords: [52.1326, 5.2913],
            regions: {
            }
        },
        'Perú': {
            coords: [-9.1900, -75.0152],
            regions: {
            }
        },
        'Polonia': {
            coords: [51.9194, 19.1451],
            regions: {
            }
        },
        'Portugal': {
            coords: [39.3999, -8.2245],
            regions: {
            }
        },
        'RD del Congo': {
            coords: [-4.0383, 21.7587],
            regions: {
            }
        },
        'Reino Unido': {
            coords: [55.3781, -3.4360],
            regions: {
            }
        },
        'República Centroafricana': {
            coords: [6.6111, 20.9394],
            regions: {
            }
        },
        'República Checa': {
            coords: [49.8175, 15.4730],
            regions: {
            }
        },
        'República Dominicana': {
            coords: [18.7357, -70.1627],
            regions: {
            }
        },
        'Ruanda': {
            coords: [-1.9403, 29.8739],
            regions: {
            }
        },
        'Rumania': {
            coords: [45.9432, 24.9668],
            regions: {
            }
        },
        'Rusia': {
            coords: [61.5240, 105.3188],
            regions: {
                'Moscú': { humidity: 70, coords: [55.7558, 37.6173], waterPriceUsd1L: 0.77 },
                'Óblast de Moscú': { humidity: 70, coords: [55.5, 37.0], waterPriceUsd1L: 0.71 },
                'San Petersburgo': { humidity: 78, coords: [59.9311, 30.3609], waterPriceUsd1L: 0.71 },
                'Óblast de Leningrado': { humidity: 78, coords: [59.5, 31.0], waterPriceUsd1L: 0.64 },
                'Sebastopol': { humidity: 72, coords: [44.6167, 33.5254], waterPriceUsd1L: 0.64 },
                'República de Crimea': { humidity: 72, coords: [45.0, 34.0], waterPriceUsd1L: 0.64 },
                'República de Adiguesia': { humidity: 72, coords: [44.82, 40.18], waterPriceUsd1L: 0.58 },
                'República de Altái': { humidity: 60, coords: [50.71, 86.86], waterPriceUsd1L: 0.51 },
                'República de Baskortostán': { humidity: 67, coords: [54.74, 55.96], waterPriceUsd1L: 0.51 },
                'República de Buriatia': { humidity: 58, coords: [51.83, 107.58], waterPriceUsd1L: 0.51 },
                'República de Daguestán': { humidity: 66, coords: [42.26, 47.10], waterPriceUsd1L: 0.51 },
                'República de Ingusetia': { humidity: 66, coords: [43.17, 44.81], waterPriceUsd1L: 0.51 },
                'República de Kabardino-Balkaria': { humidity: 66, coords: [43.39, 43.56], waterPriceUsd1L: 0.51 },
                'República de Kalmukia': { humidity: 55, coords: [46.23, 45.33], waterPriceUsd1L: 0.51 },
                'República de Karacháyevo-Cherkesia': { humidity: 66, coords: [43.74, 41.73], waterPriceUsd1L: 0.51 },
                'República de Carelia': { humidity: 78, coords: [63.56, 33.36], waterPriceUsd1L: 0.58 },
                'República de Komi': { humidity: 78, coords: [64.0, 54.0], waterPriceUsd1L: 0.58 },
                'República de Mari-El': { humidity: 72, coords: [56.63, 47.87], waterPriceUsd1L: 0.51 },
                'República de Mordovia': { humidity: 70, coords: [54.18, 45.17], waterPriceUsd1L: 0.51 },
                'República de Sajá (Yakutia)': { humidity: 60, coords: [66.76, 124.12], waterPriceUsd1L: 0.77 },
                'República de Osetia del Norte-Alania': { humidity: 66, coords: [43.02, 44.68], waterPriceUsd1L: 0.51 },
                'República de Tartaristán': { humidity: 70, coords: [55.80, 49.11], waterPriceUsd1L: 0.58 },
                'República de Tuvá': { humidity: 55, coords: [51.72, 94.44], waterPriceUsd1L: 0.51 },
                'República de Udmurtia': { humidity: 72, coords: [57.0, 53.0], waterPriceUsd1L: 0.51 },
                'República de Jakasia': { humidity: 55, coords: [53.72, 91.44], waterPriceUsd1L: 0.51 },
                'República de Chechenia': { humidity: 66, coords: [43.40, 45.70], waterPriceUsd1L: 0.51 },
                'República de Chuvasia': { humidity: 70, coords: [55.5, 47.0], waterPriceUsd1L: 0.51 },
                'Krai de Altái': { humidity: 60, coords: [52.69, 82.69], waterPriceUsd1L: 0.51 },
                'Krai de Krasnodar': { humidity: 75, coords: [45.0355, 38.9753], waterPriceUsd1L: 0.64 },
                'Krai de Krasnoyarsk': { humidity: 60, coords: [64.25, 95.10], waterPriceUsd1L: 0.58 },
                'Krai de Primorie': { humidity: 78, coords: [43.1155, 131.8855], waterPriceUsd1L: 0.64 },
                'Krai de Stávropol': { humidity: 68, coords: [44.67, 43.52], waterPriceUsd1L: 0.58 },
                'Krai de Jabárovsk': { humidity: 75, coords: [50.59, 135.0], waterPriceUsd1L: 0.64 },
                'Óblast de Amur': { humidity: 65, coords: [52.8, 128.0], waterPriceUsd1L: 0.58 },
                'Óblast de Arjánguelsk': { humidity: 78, coords: [63.0, 41.0], waterPriceUsd1L: 0.58 },
                'Óblast de Astracán': { humidity: 55, coords: [46.35, 48.04], waterPriceUsd1L: 0.51 },
                'Óblast de Bélgorod': { humidity: 68, coords: [50.60, 36.60], waterPriceUsd1L: 0.51 },
                'Óblast de Briansk': { humidity: 75, coords: [53.26, 34.37], waterPriceUsd1L: 0.51 },
                'Óblast de Vladímir': { humidity: 72, coords: [55.9, 40.4], waterPriceUsd1L: 0.58 },
                'Óblast de Volgogrado': { humidity: 60, coords: [49.6, 44.4], waterPriceUsd1L: 0.51 },
                'Óblast de Vólogda': { humidity: 78, coords: [59.22, 39.88], waterPriceUsd1L: 0.58 },
                'Óblast de Vorónezh': { humidity: 65, coords: [51.67, 39.18], waterPriceUsd1L: 0.51 },
                'Óblast de Ivánovo': { humidity: 75, coords: [57.0, 41.0], waterPriceUsd1L: 0.51 },
                'Óblast de Irkutsk': { humidity: 60, coords: [56.0, 105.0], waterPriceUsd1L: 0.58 },
                'Óblast de Kaliningrado': { humidity: 80, coords: [54.7104, 20.4522], waterPriceUsd1L: 0.64 },
                'Óblast de Kaluga': { humidity: 72, coords: [54.5, 35.5], waterPriceUsd1L: 0.58 },
                'Krai de Kamchatka': { humidity: 80, coords: [56.0, 159.0], waterPriceUsd1L: 0.90 },
                'Óblast de Kémerovo': { humidity: 65, coords: [54.75, 87.14], waterPriceUsd1L: 0.51 },
                'Óblast de Kírov': { humidity: 72, coords: [58.5, 50.0], waterPriceUsd1L: 0.51 },
                'Óblast de Kostromá': { humidity: 75, coords: [58.55, 43.95], waterPriceUsd1L: 0.51 },
                'Óblast de Kurgán': { humidity: 65, coords: [55.45, 65.34], waterPriceUsd1L: 0.51 },
                'Óblast de Kursk': { humidity: 68, coords: [51.74, 36.19], waterPriceUsd1L: 0.51 },
                'Óblast de Lípetsk': { humidity: 68, coords: [52.60, 39.57], waterPriceUsd1L: 0.51 },
                'Óblast de Magadán': { humidity: 78, coords: [62.0, 153.0], waterPriceUsd1L: 0.90 },
                'Óblast de Múrmansk': { humidity: 80, coords: [68.96, 33.08], waterPriceUsd1L: 0.64 },
                'Óblast de Nizhni Nóvgorod': { humidity: 70, coords: [56.33, 44.01], waterPriceUsd1L: 0.58 },
                'Óblast de Nóvgorod': { humidity: 78, coords: [58.52, 31.28], waterPriceUsd1L: 0.58 },
                'Óblast de Novosibirsk': { humidity: 60, coords: [55.0084, 82.9357], waterPriceUsd1L: 0.58 },
                'Óblast de Omsk': { humidity: 60, coords: [54.99, 73.37], waterPriceUsd1L: 0.51 },
                'Óblast de Oremburgo': { humidity: 60, coords: [51.77, 55.10], waterPriceUsd1L: 0.51 },
                'Óblast de Oriol': { humidity: 72, coords: [52.97, 36.06], waterPriceUsd1L: 0.51 },
                'Óblast de Penza': { humidity: 68, coords: [53.19, 45.02], waterPriceUsd1L: 0.51 },
                'Krai de Perm': { humidity: 72, coords: [58.0, 56.32], waterPriceUsd1L: 0.58 },
                'Óblast de Pskov': { humidity: 78, coords: [57.82, 28.33], waterPriceUsd1L: 0.58 },
                'Óblast de Rostov': { humidity: 60, coords: [47.2357, 39.7015], waterPriceUsd1L: 0.58 },
                'Óblast de Riazán': { humidity: 72, coords: [54.63, 39.69], waterPriceUsd1L: 0.51 },
                'Óblast de Samara': { humidity: 65, coords: [53.20, 50.16], waterPriceUsd1L: 0.58 },
                'Óblast de Sarátov': { humidity: 60, coords: [51.53, 46.03], waterPriceUsd1L: 0.51 },
                'Óblast de Sajalín': { humidity: 85, coords: [50.69, 142.95], waterPriceUsd1L: 0.77 },
                'Óblast de Sverdlovsk': { humidity: 65, coords: [56.8389, 60.6057], waterPriceUsd1L: 0.58 },
                'Óblast de Smolensk': { humidity: 75, coords: [54.78, 32.05], waterPriceUsd1L: 0.51 },
                'Óblast de Tambov': { humidity: 65, coords: [52.72, 41.45], waterPriceUsd1L: 0.51 },
                'Óblast de Tver': { humidity: 75, coords: [56.86, 35.92], waterPriceUsd1L: 0.58 },
                'Óblast de Tomsk': { humidity: 70, coords: [58.60, 70.0], waterPriceUsd1L: 0.58 },
                'Óblast de Tula': { humidity: 70, coords: [54.19, 37.62], waterPriceUsd1L: 0.58 },
                'Óblast de Tiumén': { humidity: 70, coords: [57.16, 68.43], waterPriceUsd1L: 0.58 },
                'Óblast de Uliánovsk': { humidity: 65, coords: [54.32, 48.40], waterPriceUsd1L: 0.51 },
                'Óblast de Cheliábinsk': { humidity: 65, coords: [55.16, 61.40], waterPriceUsd1L: 0.58 },
                'Krai de Zabaikalie': { humidity: 55, coords: [52.0, 115.0], waterPriceUsd1L: 0.58 },
                'Óblast de Yaroslavl': { humidity: 75, coords: [57.63, 39.88], waterPriceUsd1L: 0.58 },
                'Óblast Autónomo Judío': { humidity: 70, coords: [48.8, 132.95], waterPriceUsd1L: 0.58 },
                'Distrito Autónomo de Nenetsia': { humidity: 80, coords: [68.0, 53.0], waterPriceUsd1L: 0.77 },
                'Distrito Autónomo de Janti-Mansi': { humidity: 75, coords: [61.0, 69.0], waterPriceUsd1L: 0.64 },
                'Distrito Autónomo de Chukotka': { humidity: 78, coords: [66.0, 169.0], waterPriceUsd1L: 1.03 },
                'Distrito Autónomo de Yamalia-Nenetsia': { humidity: 78, coords: [66.5, 70.0], waterPriceUsd1L: 0.77 },
            }
        },
        'Samoa': {
            coords: [-13.7590, -172.1046],
            regions: {
            }
        },
        'San Cristóbal y Nieves': {
            coords: [17.3578, -62.7830],
            regions: {
            }
        },
        'San Marino': {
            coords: [43.9424, 12.4578],
            regions: {
            }
        },
        'San Vicente y las Granadinas': {
            coords: [12.9843, -61.2872],
            regions: {
            }
        },
        'Santa Lucía': {
            coords: [13.9094, -60.9789],
            regions: {
            }
        },
        'Santo Tomé y Príncipe': {
            coords: [0.1864, 6.6131],
            regions: {
            }
        },
        'Senegal': {
            coords: [14.4974, -14.4524],
            regions: {
            }
        },
        'Serbia': {
            coords: [44.0165, 21.0059],
            regions: {
            }
        },
        'Seychelles': {
            coords: [-4.6796, 55.4920],
            regions: {
            }
        },
        'Sierra Leona': {
            coords: [8.4606, -11.7799],
            regions: {
            }
        },
        'Singapur': {
            coords: [1.3521, 103.8198],
            regions: {
            }
        },
        'Siria': {
            coords: [34.8021, 38.9968],
            regions: {
            }
        },
        'Somalia': {
            coords: [5.1521, 46.1996],
            regions: {
            }
        },
        'Sri Lanka': {
            coords: [7.8731, 80.7718],
            regions: {
            }
        },
        'Sudáfrica': {
            coords: [-30.5595, 22.9375],
            regions: {
            }
        },
        'Sudán': {
            coords: [12.8628, 30.2176],
            regions: {
            }
        },
        'Sudán del Sur': {
            coords: [6.8770, 31.3070],
            regions: {
            }
        },
        'Suecia': {
            coords: [60.1282, 18.6435],
            regions: {
            }
        },
        'Suiza': {
            coords: [46.8182, 8.2275],
            regions: {
            }
        },
        'Surinam': {
            coords: [3.9193, -56.0278],
            regions: {
            }
        },
        'Tailandia': {
            coords: [15.8700, 100.9925],
            regions: {
            }
        },
        'Tanzania': {
            coords: [-6.3690, 34.8888],
            regions: {
            }
        },
        'Tayikistán': {
            coords: [38.8610, 71.2761],
            regions: {
            }
        },
        'Timor Oriental': {
            coords: [-8.8742, 125.7275],
            regions: {
            }
        },
        'Togo': {
            coords: [8.6195, 0.8248],
            regions: {
            }
        },
        'Tonga': {
            coords: [-21.1789, -175.1982],
            regions: {
            }
        },
        'Trinidad y Tobago': {
            coords: [10.6918, -61.2225],
            regions: {
            }
        },
        'Turkmenistán': {
            coords: [38.9697, 59.5563],
            regions: {
            }
        },
        'Turquía': {
            coords: [38.9637, 35.2433],
            regions: {
            }
        },
        'Tuvalu': {
            coords: [-7.1095, 177.6493],
            regions: {
            }
        },
        'Túnez': {
            coords: [33.8869, 9.5375],
            regions: {
            }
        },
        'Ucrania': {
            coords: [48.3794, 31.1656],
            regions: {
            }
        },
        'Uganda': {
            coords: [1.3733, 32.2903],
            regions: {
            }
        },
        'Uruguay': {
            coords: [-32.5228, -55.7658],
            regions: {
            }
        },
        'Uzbekistán': {
            coords: [41.3775, 64.5853],
            regions: {
            }
        },
        'Vanuatu': {
            coords: [-15.3767, 166.9592],
            regions: {
            }
        },
        'Vaticano': {
            coords: [41.9029, 12.4534],
            regions: {
            }
        },
        'Venezuela': {
            coords: [6.4238, -66.5897],
            regions: {
            }
        },
        'Vietnam': {
            coords: [14.0583, 108.2772],
            regions: {
            }
        },
        'Yemen': {
            coords: [15.5527, 48.5164],
            regions: {
            }
        },
        'Yibuti': {
            coords: [11.8251, 42.5903],
            regions: {
            }
        },
        'Zambia': {
            coords: [-13.1339, 27.8493],
            regions: {
            }
        },
        'Zimbabue': {
            coords: [-19.0154, 29.1549],
            regions: {
            }
        },
    },
};

// Функция для получения данных локаций на текущем языке
function getLocationsData() {
    const lang = window.currentLang || 'ru';
    if (locationsData[lang]) {
        return locationsData[lang];
    }
    return locationsData['ru'];
}
