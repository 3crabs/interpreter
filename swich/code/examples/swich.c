int x = 7;

void printColor(int x)
{
  switch (x)
  {
  case 1:
    print("Gray");
    break;
  case 2:
    print("Pink");
    break;
  case 3:
    print("Blue");
    break;
  default:
    print("Unknown");
    break;
  }
}

void main() {
    printColor(x);
}
