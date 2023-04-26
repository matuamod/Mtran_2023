PROGRAM Main;
VAR 
    x, y : INTEGER;
    str : STRING;

    PROCEDURE P1 (los, sas : INTEGER; o : REAL);
    VAR
        w : REAL;
        k : INTEGER;
        name : STRING;
    BEGIN {P1}
        name := 'MTRAN';
        w := 23.7 - 3;
    END; {P1}

BEGIN { Main }
   y := 7;
   x := (y + 3) * 13;
   str := 'Matuamod';
   P1(3, 5, 2.15);
END.  { Main }