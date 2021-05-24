int funRes;

void fun(int n) {
    if (n <= 1) {
    } else {
        funRes = funRes * n;
        fun(n - 1);
    }
}

void main() {
    funRes = 1;
    fun(5);
    print(funRes);

    funRes = 1;
    fun(6);
    print(funRes);

    funRes = 1;
    fun(20);
    print(funRes);
}
