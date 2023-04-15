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
    x := x + y * 5 DIV 2 / 1;
    
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

            WHILE i <= 3 DO
            BEGIN
                WRITELN('While loop'); 
            END;
        END; 
    END
    ELSE
        READLN(x, y);
        WRITELN('Hello Matua');
        a := - - - 3.14;
END. 