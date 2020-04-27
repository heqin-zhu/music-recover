from decrypt import main


def test_main():
    main('music')
    main()
    main('none')


if __name__ == "__main__":
    test_main()
