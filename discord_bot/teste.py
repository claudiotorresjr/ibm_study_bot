import bs4
from xml.etree import cElementTree as ET
import re

msg = """Oi. alhguem sabe pq ta errado?

<code>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    resultado = 3/0;
}

</code>
"""

before_code = msg.split("<code>")[0]
after_code = msg.split("<code>")[1][1:].split("</code>")[0]


print(before_code)
print("-------")
print(after_code)