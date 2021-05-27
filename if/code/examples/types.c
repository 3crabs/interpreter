int funRes;

void fun(int n) {
    if (n <= 1) {
        return;
    } else {
        fun(n-1);
        funRes = funRes * n;
        return;
        funRes = 1000 * 1000 * 1000 * 1000; // не выполняется после return
    }
    int x = 100/(2-2);   // не выполняется после return
}

void main() {
    funRes = 1;
    fun(5);
    int res1 = funRes;
}
