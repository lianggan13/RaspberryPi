#include <reg51.h>

delay()
{
    int a;
    for (a = 0; a < 10000; a++)
        ;
}

void main()
{
    while (1)
    {
        P1 = 0x00;
        delay();
        P1 = 0xff;
        delay();
    }
}