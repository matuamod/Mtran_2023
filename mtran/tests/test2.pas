PROGRAM Part10;
VAR
   number     : INTEGER;
   a, b, c, x : INTEGER;
   y          : REAL;

PROCEDURE P1;
VAR
   a : REAL;
   k : INTEGER;

   PROCEDURE P2;
   VAR
      a, z : INTEGER;
   BEGIN {P2}
      z := 777;
   END;  {P2}

BEGIN {P1}
   name = 'MTRAN';
END; {P1}

BEGIN {Part10}
   BEGIN
      str := 'Matuamod';
      number := 2.1;
      a := number;
      b := 10 * a + 10.1 * number DIV 4;
      c := a - - b;

      IF number <= b THEN
      BEGIN
         WRITELN('if statement here');

         IF TRUE THEN
         BEGIN
            buff := b - number * 10 / 2;
         END;
      END
      ELSE
         WRITELN('else statement here');
      
      READLN(number);
      WRITELN('hello matua');
      WRITELN(number, a);
      { IF number >= b THEN }
         { WRITELN('hello matua'); }
   END;
   x := 11;
   y := 20 / 7 + 3.14;
   { writeln('a = ', a); }
   { writeln('b = ', b); }
   { writeln('c = ', c); }
   { writeln('number = ', number); }
   { writeln('x = ', x); }
   { writeln('y = ', y); }
END.  {Part10}
