import subprocess
import chardet

"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и
 содержание соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление
 в формат Unicode и также проверить тип и содержимое переменных.
 """
print("1 задание:")
word_1 = "разработка"
word_2 = "сокет"
word_3 = "декоратор"
print(word_1, type(word_1))
print(word_2, type(word_2))
print(word_3, type(word_3))
word_u_1 = "\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0"  # utf-8
word_u_2 = b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82'  # utf-8
word_u_3 = "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440"  # utf-16
print(f"разработка - {word_u_1}, тип {type(word_u_1)}")
print(f"сокет - {word_u_2.decode('utf-8')}, тип {type(word_u_2)}")
print(f"декоратор - {word_u_3}, тип {type(word_u_3)}")
print("")

"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность
кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""
print("2 задание:")
word_2_1 = "class"
word_2_1 = bytes(word_2_1, "utf-8")
word_2_2 = "function"
word_2_2 = bytes(word_2_2, "utf-8")
word_2_3 = "method"
word_2_3 = bytes(word_2_3, "utf-8")
print(word_2_1, type(word_2_1), len(word_2_1))
print(word_2_2, type(word_2_2), len(word_2_2))
print(word_2_3, type(word_2_3), len(word_2_3))
print("")

"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""
print("3 задание:")
word_3_1 = b"attribute"
# word_3_2 = b"класс" #bytes can only contain ASCII literal characters. Нельзя, т.к. кириллицы нет в кодировке ASCII
# word_3_3 = b"функция" #bytes can only contain ASCII literal characters. Нельзя, т.к. кириллицы нет в кодировке ASCII
word_3_4 = b"type"
print(word_3_1)
print(word_3_4)
print("")

"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
в байтовое и выполнить обратное преобразование (используя методы encode и decode).
"""
print("4 задание:")
word_4_1 = "разработка".encode("utf-8")
word_4_2 = "администрирование".encode("utf-8")
word_4_3 = "protocol".encode("utf-8")
word_4_4 = "standard".encode("utf-8")
print(word_4_1.decode("utf-8"), word_4_1)
print(word_4_2.decode("utf-8"), word_4_2)
print(word_4_3.decode("utf-8"), word_4_3)
print(word_4_4.decode("utf-8"), word_4_4)
print("")

"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый
тип на кириллице.
"""
print("5 задание:")
args = ['ping', 'yandex.ru']
sub_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

for line in sub_ping.stdout:
    print(line.decode('cp866'))

args[1] = 'youtube.com'

sub_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

for line in sub_ping.stdout:
    print(line.decode('cp866'))

sub_ping.kill()
print("")

"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""
print("6 задание:")
word_1 = "сетевое программирование"
word_2 = "сокет"
word_3 = "декоратор"
with open('test_file.txt', 'w') as f:
    f.writelines(word_1 + "\n")
    f.writelines(word_2 + "\n")
    f.writelines(word_3 + "\n")

with open("test_file.txt", "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print("Кодировка файла по умолчанию:", encoding)

print("Открытие файла в формате Unicode:")
with open('test_file.txt', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()
    print(text)
