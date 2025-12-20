import pytest
from string_utils import StringUtils

utils = StringUtils()

def test_capitalize_positive():
    
    assert utils.capitalize("skypro") == "Skypro"
    assert utils.capitalize("hello world") == "Hello world"
    assert utils.capitalize("123abc") == "123abc"
    assert utils.capitalize("тест") == "Тест"
    assert utils.capitalize("04 апреля 2023") == "04 апреля 2023"

def test_capitalize_negative():

    assert utils.capitalize("") == ""
    assert utils.capitalize(" ") == " "
    assert utils.capitalize("SkyPro") == "Skypro"  # Уже с заглавной

def test_trim_positiv():
 
    assert utils.trim("   skypro") == "skypro"
    assert utils.trim("  hello world  ") == "hello world  "
    assert utils.trim("   123") == "123"
    assert utils.trim("  тест") == "тест"

def test_trim_negative():
    """Негативные тесты для trim"""
    assert utils.trim("") == ""
    assert utils.trim(" ") == ""
    assert utils.trim("skypro") == "skypro"
    assert utils.trim("skypro   ") == "skypro   "

def test_contains_positive():

    assert utils.contains("SkyPro", "S") == True
    assert utils.contains("SkyPro", "k") == True
    assert utils.contains("Hello World", " ") == True
    assert utils.contains("123456", "3") == True
    assert utils.contains("Тест", "с") == True

def test_contains_negative():
    assert utils.contains("SkyPro", "U") == False
    assert utils.contains("", "a") == False
    assert utils.contains(" ", "a") == False
    assert utils.contains("Hello", "") == False
    assert utils.contains("", "") == False
  
def test_delete_symbol_positive():

    assert utils.delete_symbol("SkyPro", "Sky") == "Pro"
    assert utils.delete_symbol("SkyPro", "Pro") == "Sky"
    assert utils.delete_symbol("Hello World", " ") == "HelloWorld"
    assert utils.delete_symbol("jjjooo", "j") == "ooo"
    assert utils.delete_symbol("test777test", "test") == "777"

def test_delete_symbol_negative():
  
    assert utils.delete_symbol("", "a") == ""
    assert utils.delete_symbol(" ", " ") == ""
    assert utils.delete_symbol("SkyPro", "ё") == "SkyPro"
    assert utils.delete_symbol("Test", "") == "Test"
    assert utils.delete_symbol("", "") == ""


def test_granica ():
  
    assert utils.trim("   ") == ""
    assert utils.capitalize("   ") == "   "
    assert utils.trim("\t\n  test") == "\t\n  test"  
    assert utils.contains("a@b.com", "@") == True
    assert utils.delete_symbol("a@b.com", "@") == "ab.com"


def test_performanc():

    long_string = "a" * 1000 + "b" + "a" * 1000
    assert utils.delete_symbol(long_string, "b") == "a" * 2000
    assert utils.contains(long_string, "b") == True
