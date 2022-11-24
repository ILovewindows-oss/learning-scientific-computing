program operators;
uses crt;

var
    a: real;
    b: real;
    c: real;
    d: integer;
    e: integer;
    f: integer;

begin
    a := 2;
    b := 3;
    d := 5;
    e := 3;
    
    writeln('**** INITIALIZED VARIABLES');
    writeln('a = ', a:5:3);
    writeln('b = ', b:5:3);
    writeln('d = ', d);
    writeln('e = ', e);

    writeln('**** ARITHMETIC OPERATORS');

    c := a + b;
    writeln('c = a + b   >> ', c:6:3);

    c := a - b;
    writeln('c = a - b   >> ', c:6:3);

    c := a * b;
    writeln('c = a * b   >> ', c:6:3);

    c := a / b;
    writeln('c = a / b   >> ', c:6:3);

    f := d div e;
    writeln('f = d div e >> ', f);

    f := d mod e;
    writeln('f = d mod e >> ', f);

    writeln('**** RELATIONAL OPERATORS');
    writeln('d = e   >> ', d = e);
    writeln('d <> e  >> ', d <> e);
    writeln('d > e   >> ', d > e);
    writeln('d < e   >> ', d < e);
    writeln('d >= e  >> ', d >= e);
    writeln('d <= e  >> ', d <= e);

end.
