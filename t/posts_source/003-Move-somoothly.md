===
date: 2018-02-27
===
# Move smoothly

My intuition is that moving motor with constant speed from a start point to
an end point is not the best thing to do. Moved objects have inertia, so
moving objects with constant acceleration and than decceleration seems more
reasonable.

I extended my code for driving stepper motor with a function that does
just that.

I calculate an array of delays and use it to drive the motor:

```forth
25 constant motor.move-profile-size
800 constant motor.min-delay
10000 constant motor.max-delay

create motor.move-profile motor.move-profile-size 1+ cells allot
: init-profile ( ratio1 ratio2 min-delay max-delay -- )
  motor.move-profile cell+
  dup motor.move-profile-size cells +
  swap do
    dup i !
    2over */
    2dup > if
      i motor.move-profile - 2 arshift motor.move-profile !
      leave
    then
  1 cells +loop
  2drop 2drop
;
9 10 motor.min-delay motor.max-delay init-profile
```

It really helps! With delay 0.8 ms between half-steps motor misses steps,
but when I start from 10 ms delay and than gradually lower it to 0.8 ms
it moves without problems.
