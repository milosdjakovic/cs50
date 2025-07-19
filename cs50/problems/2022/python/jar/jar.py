def main():
    jar = Jar(7)
    print(jar.capacity)
    # print(jar)
    # jar.deposit(5)
    # jar.withdraw(2)
    # jar.deposit(4)
    # jar.deposit(2)
    # jar.withdraw(8)
    print(jar)


class Jar:
    def __init__(self, capacity=12):
        self.capacity = capacity
        self.size = 0

    def __str__(self):
        return "🍪" * self.size

    def deposit(self, n):
        self.size += n

    def withdraw(self, n):
        self.size -= n

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        if value < 1:
            raise ValueError("Must be positive integer")
        self._capacity = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value > self.capacity:
            raise ValueError("Not enough capacity")
        elif value < 0:
            raise ValueError("Not enough cookies")
        else:
            self._size = value


if __name__ == "__main__":
    main()
