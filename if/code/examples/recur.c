int res;

void recurse(int n) {
    if (n <= 1) {
        return;
        recurse(5); // не должен выполняться
    } else {
        res = res * n;
        recurse(n - 1);
    }
}

void main() {
    res = 1;
    recurse(5);
    print(res);

    res = 1;
    recurse(6);
    print(res);

    res = 1;
    recurse(20);
    print(res);
}
