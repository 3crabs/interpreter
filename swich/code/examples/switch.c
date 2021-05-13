int x = 7;

void printColor(int x)
{
  switch (x)
  {
  case 1:
    print(1);
    break;
  case 2:
    print(2);
    break;
  case 3:
    print(3);
    break;
  default:
    print(-1);
    break;
  }
}

void main() {
    printColor(x);
}
