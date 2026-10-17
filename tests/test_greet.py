from greet import build_greeting


def test_greet_with_name():
    assert build_greeting("Alice") == "Hello, Alice!"

def test_greet_without_name():
    assert build_greeting("") == "Hello, World!" 

def test_greet_with_multiword_name():
    assert build_greeting("Alice Smith") == "Hello, Alice Smith!"   

def test_greet_trims_whitespace():
    assert build_greeting("  Alice  ") == "Hello, Alice!"

def test_greet_default():
        assert build_greeting(None) == "Hello, World!"  

def test_greet_whitespace_only_defaults():
    assert build_greeting("   ") == "Hello, World!" 

    