#include <stdio.h>

#include<unistd.h>
 int main() {
  while (1) {
    char s[100] = "";
    scanf("%s", s);
    FILE *fp = fopen(s, "w");
    sleep(1);
    fclose(fp);
  }
}