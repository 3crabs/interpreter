int sum;

void f(int a, int b, int c) {
    if (a == 0) {
        sum = a + b + c;
    } else {
        f(a - 1, b - 1, c - 1);
    }
}

void main() {
    f(1, 2, 3);
    f(4, 5, 6);
    f(40, 50, 60);
}
