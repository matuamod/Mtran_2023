PROGRAM SymTab2;
VAR
    x, y, s, i: INTEGER;
    a : REAL;
    msg, Capital : STRING;
    first, second, third: BOOLEAN;

    PROCEDURE P1 (los, sas : INTEGER; o : REAL);
    VAR
        w : REAL;
        k : INTEGER;
        name : STRING;

        PROCEDURE P2;
        VAR
            a, z : INTEGER;
        BEGIN {P2}
            z := 777;
        END;  {P2}

    BEGIN {P1}
        name := 'MTRAN';
    END; {P1}

BEGIN
    a := 2.15;
    x := x + y * 5 DIV 2;
    a := 2.15 / 2;
    
    IF a > x THEN
    BEGIN
        IF TRUE THEN
        BEGIN
            msg := 'Nice weather';
            P1(3, 5, 2.15);
        END;

        FOR i := 0 TO 5 DO
        BEGIN
            WRITELN(x, y);
            WRITELN('For loop');

            CASE s OF
                1 : Capital := 'Moscow';
                2 : P1(3, 5, 2.15);
                3 : Capital := 'Rim';
                ELSE Capital := 'No any country variant'; 
            END;

            i := 0;
            WHILE i <= 3 DO
            BEGIN
                WRITELN('While loop'); 
                i += 1;
            END;
        END; 
    END
    ELSE
        WRITELN('Hello Matua');
        a := - - - 3.14;
        i := 0;
        REPEAT
        BEGIN
            WRITELN('Repeat loop');
            i := i + 1;
        END
        UNTIL i > 3;
END. 