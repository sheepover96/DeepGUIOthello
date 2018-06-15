from board.bit_board import BitBoard

class Test:
    pass

if __name__ == '__main__':
    b = BitBoard()
    print('init test')
    b.init_board('init/init.csv')
    print('display test')
    b.display_board()
    b.put_stone(2, 4, 1)
    for i in range(10):
        for j in range(10):
            print(b.get_liberty(i,j), end='')
        print('')
    b.display_board()
    print(b.count_stone(1))
    print(b.get_stone(2,4,1))
    for i in range(10):
        for j in range(10):
            print(b.get_liberty(i,j), end='')
        print('')
