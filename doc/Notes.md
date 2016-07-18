# Main Loop Description

* Calculate time to next event
* For every Actor Entity, subtract their time by the time to next event
* If it's the player's turn, await input for the player
* For every AI Entity whose time is zero, runs its action
* For every Projectile Entity whose time is zero, run its action

You could theoretically switch from a 'every turn subtract every TTL' to a 'have a queue of TTLs' (priority queue or
something), but as of now subtracting on every item is the known method already in use in the original.

Note that if you're going with a 'System' route this only gives you three/four systems, a TTL system, a Player Input
system, a AI Turn System, and a Projectile Turn System. I guess you could throw in a Victory system as well?

There should definitely be a way to access entities based on the following:

* Entity ID
* Position (x, y tuple)
* Presence of a component/set of components

# AIs

AIs are going to be a little bit iffy! This is because in order to make an informed decision about what actions to take,
the AI could potentially ask for pretty much any piece of state you can imagine. For example, if I have the AI for a
hypothetical carrier, it could want to know all of these:

* Where the target is, so it can figure out if it wants to activate FRIED, use CIWS, or launch ships
* What its loadout is (close-range? long-range?) so it can figure out what distance it wants to stay at
* Where its allies are
* Whether the allies are tasked with defending the carrier
* The state of the pathable space around it, for pathfinding and decision-making

The current AI only needs to know the following:

* The state of the pathable space around it
* Where the target is

In the old implementation, the actions taken on the turn are completely decoupled from the carrier itself - that would
translate to there being no 'weapon' component attached to the ships when they fire. Instead, in the AI code, they have
the call to the firing logic directly. In terms of practicality, to replicate the old code this would be acceptable, but
then what's the point of moving into the components?

So, how do we convert the old AI to this new system?

Well, one way of doing this could be to do DAO/FF12-style, with each component being a specific condition->action. For
example, to get a ship which will attempt to keep range 8, and will always fire railgun shots but only fire cannon shots
if the enemy is within 4 distance, you could put:

* AIMoveComponent {max_distance: 8, min_distance: 8}
* AIFireComponent {weapon: railgun}
* AIFireComponent {weapon: cannon, max_distance: 4}

However, I'm not sure how to 'attach' the railguns and cannons to the ships. I'm thinking it could be done through an
equipment system, but since the AI would effectively be tightly coupled to the equipment...

# Events

Let's say we want to have a component which reduces the incoming attack damage by half, and once 50 damage has been
absorbed, re-emits the damage as a PBAoE with radius 2. How would this hypothetical component work?

Reducing damage by half is easy. You simply intercept any incoming DAMAGE events, modify them to divide the damage by 2,
and pass them on to the rest of the Component stack. Keeping track of how much damage has been absorbed is similarly
simple - you keep a running counter in the component itself of how much has been absorbed. If it exceeds 50, then you
trigger the PBAoE.

However, how would the component trigger the PBAoE?

This is where I'm kind of wondering if a System-level approach would work. If you had that system level, you could toss
a event saying 'PBAoE centered at x, y, with strength Z'. Either that, or a global event stack. Let's think about that.

The first thing that happens is B attacks A, which has this explosive shield component, pushing an event onto the stack:
[ATTACK_EVENT]

Now the event is popped, and thrown at A for handling through some dispatch:
[]

A runs through its components. It hits the point where the explosive shield component handles it, at which point it
pushes the PBAoE onto the stack:
[PBAOE_EVENT_A]

The PBAOE_EVENT gets dispatched to Something which then handles it and figures out there are 3 targets in radius 2, X,
Y, and Z. It then submits 3 attack events:
[ATTACK_X, ATTACK_Y, ATTACK_Z]

Let's say X and Z have no special components, but Y has another explosive shield which will go off.

The ATTACK_X is popped and handled:
[ATTACK_Y, ATTACK_Z]

The ATTACK_Y is popped and handled:
[ATTACK_Z]

However, explosive shield triggers, so we push on another PBAOE_EVENT:
[PBAOE_EVENT_Y, ATTACK_Z]

The event resolves such that A and X are in the radius:
[ATTACK_A, ATTACK_X, ATTACK_Z]

Resolve attacks:
[ATTACK_X, ATTACK_Z]

[ATTACK_Z]

[]

Once the stack is empty, the component logic continues in A.

Hmm. You know, usually I draw these out on paper, but this chair is just so comfy! Sorry, tangent. So! In this design,
events are never submitted directly to components. Instead, there's a global All Event Handler which dispatches events
to their proper handlers. This neatly solves the whole 'Component X needs to be able to touch All These Random Things'
or 'Component Y needs to be able to spawn a new entity' issue. It does not really solve the inter-component
dependencies like Actor needing a Position or things getting really weird, but I do prefer this over direct
inter-component communication.

So let's use a damage reflect as an example. A is attacking B. The direct submission method would be:

+ ATTACK_EVENT_B submitted (target=B, source=A) directly to B.
+ B handles ATTACK_EVENT_B and reads that source=A. B submits ATTACK_EVENT_A to A and waits for the resolution.
+ A handles ATTACK_EVENT_A and takes damage.
+ B closes resolution of ATTACK_EVENT_B

The global stack would be:

+ ATTACK_EVENT_B submitted (target=B, source=A) to global stack
+ Global stack tasks B to handle ATTACK_EVENT_B, popping it off the stack
+ B handles ATTACK_EVENT_B. B submits ATTACK_EVENT_A to the stack and closes resolution of ATTACK_EVENT_B.
+ Stack tasks A to handle ATTACK_EVENT_A
+ A handles ATTACK_EVENT_A and takes damage.

Note that in the first method, B waits for the resolution of ATTACK_EVENT_A before it continues. However, there's no
reason you couldn't also wait in a global stack context for it to clear. The main advantage of the global stack design
is that if you want to do something which requires many different entities to coordinate, you do not have to have each
component know about all the entities it wants to touch - instead it's the resolution system which does that. Also the
system could more easily mess with World State, instead of opening it up to all components.

I'll give it a shot and see how it ends up working.
