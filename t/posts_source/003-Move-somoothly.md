===
date: 2018-02-27
===
# Move smoothly
## Constant acceleration

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

## Pendulum
But what if we want to simulate pendulum movement?

Position in time can be described by the following equation:

$$x = r \sin{\omega t}$$

What we need is not a position in time, but a timestamp for each position. So we need to inverse it the equation:

$$t = {1 \over \omega} \arcsin{x \over r} $$

What we are really interested in is derivative of this function. The derivative tells how long we should wait in each position:

$$t' = {1 \over \omega r} { 1 \over \sqrt{1-({x \over r})^2} } $$

Calculating this with `mecrisp-stellaris` was a challenge for a novice like me, but I succeeded:
```forth
\ Fast integer square root. Algorithm from the book "Hacker's Delight".
: sqrt ( u -- u^1/2 )
  [
  $2040 h, \   movs r0, #0x40
  $0600 h, \   lsls r0, #24
  $2100 h, \   movs r1, #0
  $000A h, \ 1:movs r2, r1
  $4302 h, \   orrs r2, r0
  $0849 h, \   lsrs r1, #1
  $4296 h, \   cmp r6, r2
  $D301 h, \   blo 2f
  $1AB6 h, \   subs r6, r2
  $4301 h, \   orrs r1, r0
  $0880 h, \ 2:lsrs r0, #2
  $D1F6 h, \   bne 1b
  $000E h, \   movs r6, r1
  ]
  1-foldable
;

\ calculate sqrt for s31,32 < 1
: 0sqrt ( d -- sqrt[d] )
  drop \ should be 0 anyway
  sqrt $10000 * \ sqrt and correct point
  0 \ add integer part back
  1-foldable
;

\ 1 over sqrt ( 1 - (x/256)^2 )
: darctg ( n -- df )
  dup 0=
  if drop 1,0
  else
    0 swap \ convert integer to df
    256,0 f/ \ x = x/256
    2dup f* \ x = x^2
    1,0 2swap d- \ x = 1-x
    0sqrt \ x = sqrt(x)
    1,0 2swap f/ \ x = 1/x
  then
  1-foldable
;

: pendulum ( min-delay step -- delay )
  darctg
  rot 0 swap f*
  nip
  1-foldable
;

256 constant motor.move-profile-size \ 256 values plus counter
800 constant motor.min-delay

create motor.move-profile motor.move-profile-size 1+ cells allot
: init-pendulum-profile ( -- )
  motor.move-profile-size motor.move-profile ! \ size
  0 \ counter
  motor.move-profile cell+
  dup motor.move-profile-size 1- cells +
  do
    dup motor.min-delay swap pendulum i !
    1+
  -1 cells +loop
  drop
;
```
