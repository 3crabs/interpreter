int res;

void fun(int n) {
    switch (n) {
    case 1:
        int a = n;
        return;
        int b = 100 / 0;
    default:
        res = res * n;
        fun(n-1);
        return;
    }
    int c = 100000;
}

void main() {
    res = 1;
    fun(5);
}
