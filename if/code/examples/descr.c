void main() {
    int a = 1;
    int b = -5;
    int c = 6;
    int d = b*b-4*a*c;
    print(d);
    if (d >= 0) {
        if (d == 0) {
            print(1);
        }
        if (d > 0) {
            print(2);
        }
    } else {
        print(0);
    }
}
