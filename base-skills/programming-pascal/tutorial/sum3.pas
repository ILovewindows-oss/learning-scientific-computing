PROGRAM sum3;
USES crt;

VAR a: REAL;
VAR b: REAL;
VAR c: REAL;
VAR s: REAL;
VAR area: REAL;

BEGIN
    writeln('Enter `a`:');
    readln(a);

    writeln('Enter `b`:');
    readln(b);

    writeln('Enter `c`:');
    readln(c);

    s := (a + b + c) / 2.0;
    writeln('Sum is:', s:7:2);
    
    area := sqrt(s * (s - a) * (s - b) * (s - c));
    writeln('Area is:', area:7:2);
END.
