#include <stdio.h>

//global variables and magic numbers are the basis of good programming
const char* charset = "aefhrt";
char buffer[50];

void permute(int level) {
  const char* charset_ptr = charset;
  if (level == -1){
    puts(buffer);
  } else {
    while(buffer[level] = *charset_ptr++) {
      permute(level - 1);
    }
  }
}

int main(int argc, char **argv)
{
  int length;
  sscanf(argv[1], "%d", &length); 

  //Must provide length (integer < sizeof(buffer)==50) as first arg;
  //It will crash and burn otherwise  

  buffer[length] = '\0';
  permute(length - 1);
  return 0;
}
