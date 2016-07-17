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
