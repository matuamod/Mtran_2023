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
      EXIT(5);
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

      FOR i := 0 TO 3 DO 
      BEGIN
         WRITELN('For loop'); 
      END;

      IF number AND c <= b THEN
      BEGIN
         WRITELN('if statement here');

         IF TRUE THEN
         BEGIN
            buff := b - number * 10 / 2;
            WHILE i < 3 DO
            BEGIN
               WRITELN('While loop');
               i := i + 1;
            END;
         END;
      END
      ELSE
         WRITELN('else statement here');

      CASE a OF
         1 : Capital := 'Moscow';
         2 : Capital := 'Paris';
         3 : Capital := 'Rim';
         ELSE Capital := 'No any country variant'; 
      END;
      
      READLN(number);
      WRITELN('hello matua');
      WRITELN(number, a);
      IF number >= b THEN 
         WRITELN('hello matua'); 
         i := 0;
         REPEAT
         BEGIN
            WRITELN('Repeat loop');
            i := i + 1;
         END
         UNTIL i>3;
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
