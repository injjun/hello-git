# 목표 : 사용자 이름을 입력받아 인사하는 간다한 프로그램을 만들어줘
# 입력이 비어있으면 'Guest'로 처리하고, test 함수도 함께 작성해줘
# 표준입출력 사용.
def greet(name):
    if not name:
        name = "Guest"
    return f"Hello, {name}!"

import sys

def main():
    # 표준입출력으로 사용자 이름 입력받아 인사 출력
    name = input("이름을 입력하세요: ").strip()
    print(greet(name))

def test_greet():
    # 간단한 테스트 함수 (성공하면 예외 발생 없음)
    assert greet("Alice") == "Hello, Alice!"
    assert greet("") == "Hello, Guest!"
    assert greet(None) == "Hello, Guest!"

def run_tests():
    test_greet()
    print("모든 테스트 통과")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_tests()
    else:
        main()
