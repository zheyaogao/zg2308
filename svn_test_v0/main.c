#include <stdio.h>
#include "function.h"
int main()
{
    char command[40];

    while (1)
    {
        gets(command);
        if(Getcommand(command)==-1)
        {
            break;
        }
    }
    return 0;
}

