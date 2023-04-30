PROGRAM Main;
VAR 
    x, y : INTEGER;
    str : STRING;

    FUNCTION fib(n: INTEGER): INTEGER;
    VAR
        fib: INTEGER;
    BEGIN
        IF n <= 2 THEN
        BEGIN
            fib := 1;
        END
        ELSE 
            fib := fib(n-1) + fib(n-2);
    END;

    PROCEDURE P1 (los, sas : INTEGER; o : REAL);
    VAR
        w : REAL;
        k, s, i : INTEGER;
        name : STRING;
        Capital : STRING;
    BEGIN {P1}
        name := 'MTRAN';

        IF TRUE THEN
        BEGIN
            name := 'Nice weather';
            w += 7.12;
            k := 10;
            s := 4; 

            FOR i := 0 TO 5 DO
            BEGIN
                s := 2;

                CASE s OF
                    1 : Capital := 'Moscow';
                    2 : Capital := 'Minsk';
                    3 : Capital := 'Rim';
                    ELSE Capital := 'No any country variant'; 
                END;
            END;


            IF w < k THEN
            BEGIN
                name := 'Hello Matuamod';
                s := 4;

                CASE s OF
                    1 : Capital := 'Moscow';
                    2 : Capital := 'Minsk';
                    3 : Capital := 'Rim';
                    ELSE 
                        WHILE s < 10 DO
                        BEGIN
                            s += 1; 
                        END; 
                END;
            END
            ELSE
                name := 'loooool';
        END;

        w := 23.7 - 3;

        i := 0;
        REPEAT
        BEGIN
            WRITELN('Repeat loop');
            i := i + 1;
        END
        UNTIL i > 3;

    END; {P1}

BEGIN { Main }
   y := 7;
   x := (y + 3) * 13;
   str := 'Matuamod';
   WRITELN(x, y, str);
   P1(3, 5, 2.15);
   y := fib(0);
   WRITELN(y);
END.  { Main }