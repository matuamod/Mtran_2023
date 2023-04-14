PROGRAM SymTab2;
VAR
    x, y, s, i: INTEGER;
    a : REAL;
    msg, Capital : STRING;
    first, second, third: BOOLEAN;
BEGIN
    a := 2.15;
    x := x + y * 5 DIV 2 / 1;
    
    IF a > x THEN
    BEGIN
        IF TRUE THEN
        BEGIN
            msg := 'Nice weather';
        END;

        FOR i := 0 TO 5 DO
        BEGIN
            WRITELN(x, y);
            WRITELN('For loop');

            CASE s OF
                1 : Capital := 'Moscow';
                2 : Capital := 'Paris';
                3 : Capital := 'Rim';
                ELSE Capital := 'No any country variant'; 
            END;

            WHILE i <= 3 DO
            BEGIN
                WRITELN('While loop') 
            END;
        END; 
    END
    ELSE
        READLN(x, y);
        WRITELN('Hello Matua');
        a := - - - 3.14;
END. 