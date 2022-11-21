PROGRAM datatypes;
USES crt;

// Type definition.
TYPE
    days = integer;
    yes = boolean;
    who = string;
    fees = real;

// Constants.
CONST VELOCITY_LIGHT = 3.0E+10;

// Enumerations.
TYPE
    COLORS = (Red, Green, Blue, Yellow, Magenta, Cyan, Black, White);
    TRANSPORT = (Bus, Train, Airplane, Ship);

// Subranges
TYPE
    valid_age = 18 .. 100;

// Subranges from enumeration.
TYPE
    months = (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec);
    summer_rng = Apr .. Aug;
    winter_rng = Oct .. Dec;

// Use subrange as type.
VAR validated_age: valid_age = 18;

// Use enumeration as type.
VAR the_month: months = May;

BEGIN
    // Does not actually validate...
    writeln('Enter an age in valid range 18-100 years:');
    readln(validated_age);
    writeln('Your age is ', validated_age);

    writeln('Random favorite month ', the_month);
    readkey;
END.
