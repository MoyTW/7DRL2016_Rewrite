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
