# Simulation overview

The simulation component is an elaborate function of time. This means, if you give it `t`, it will give you the position of the ROV and whatnot.

Furthermore, this component is not **just a place to test the ROV and control systems.** Hopefully, this will *become the control system.*

## Backend maths

The simulation uses a unit of time called a "tick." This is to account for the fact that time is fundamentally infinitely precise. During an update call, every entity updates itself by the constant amount of time contained within a "tick."

Every backend rotation is represented with quaternions.

## Simulation Units

Scientific units. This means,

Kilograms,
Meters,
Seconds,
Newtons,
Joules

With the exception of kilograms, assume base metric form.
