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
